from typing import TYPE_CHECKING

import storage
import storage.recovery

from . import layout, recover
from trezor import config, loop, utils, wire
from trezor.ui import i18n, NavigationBack
from trezor.messages import Success
from trezor.enums import MessageType, BackupType
from trezor.errors import MnemonicError
from trezor.crypto.hashlib import sha256
from apps.common import mnemonic

from trezor.ui.layouts import (
    confirm_reset_device,
    confirm_pin_security,
    confirm_check_recovery_mnemonic,
    show_popup,
    load_popup,
    show_success,
    wallet_import_tip,
    wallet_download_tip
)

from trezor.ui.layouts import request_word_count

from apps.common.request_pin import (
    error_pin_invalid,
    request_pin_and_sd_salt,
    request_pin_confirm,
)

# from ..recovery_device2.homescreen import _request_share_first_screen
if TYPE_CHECKING:
    from trezor.messages import RecoveryDevice

    pass


# List of RecoveryDevice fields that can be set when doing dry-run recovery.
# All except `dry_run` are allowed for T1 compatibility, but their values are ignored.
# If set, `enforce_wordlist` must be True, because we do not support non-enforcing.
DRY_RUN_ALLOWED_FIELDS = ("dry_run", "word_count", "enforce_wordlist", "type")


async def recovery_device(ctx: wire.Context, msg: RecoveryDevice) -> Success:
    """
    Recover BIP39/SLIP39 seed into empty device.
    Recovery is also possible with replugged Trezor. We call this process Persistence.
    User starts the process here using the RecoveryDevice msg and then they can unplug
    the device anytime and continue without a computer.
    """
    _validate(msg)

    if isinstance(ctx, wire.DummyContext):
        utils.play_dead()

    try:
        if not msg.dry_run:
            if msg.language is not None:
                i18n.change_language(msg.language)
            await load_popup(
                i18n.Text.wiping_device, timeout_ms=1000
            )
            # from trezor.ui.screen.bluetooth import BluetoothPairing
            # await BluetoothPairing("56778").show()
            # await wallet_download_tip(ctx,i18n.Title.download_digital,i18n.Text.download_digital_tips.format("https://ds.pro/download"))
            # wipe storage to make sure the device is in a clear state
            storage.reset()
            if msg.language is not None:
                storage.device.set_language(msg.language)
            # await _continue_dialog(ctx, msg)#旧的已经去除
            # set up pin if requested
            if msg.pin_protection :
                await confirm_pin_security(ctx, "", recovery=True)
                newpin = await request_pin_confirm(ctx)
                config.change_pin("", newpin, None, None)
            storage.device.set_passphrase_enabled(bool(msg.passphrase_protection))
            if msg.u2f_counter is not None:
                storage.device.set_u2f_counter(msg.u2f_counter)
            if msg.label is not None:
                storage.device.set_label(msg.label)
        
        storage.recovery.set_in_progress(True)
        storage.recovery.set_dry_run(bool(msg.dry_run))
        result = await recovery_process(ctx)
    except BaseException as e:
        raise e
    else:
        if msg.enforce_wordlist:
            if isinstance(ctx, wire.DummyContext):
                loop.clear()
            return result
    finally:
        if isinstance(ctx, wire.DummyContext):
            if msg.dry_run:
                utils.set_up()


async def recovery_process(ctx: wire.GenericContext) -> Success:
    wire.AVOID_RESTARTING_FOR = (MessageType.Initialize, MessageType.GetFeatures)
    try:
        return await _continue_recovery_process(ctx)
    except recover.RecoveryAborted:
        dry_run = storage.recovery.is_dry_run()
        if dry_run:
            storage.recovery.end_progress()
        # else:
        #     await show_popup(i18n.Text.please_wait)
        #     storage.wipe()
        raise wire.ActionCancelled

def _validate(msg: RecoveryDevice) -> None:
    if not msg.dry_run and storage.device.is_initialized():
        raise wire.UnexpectedMessage("Already initialized")
    if msg.dry_run and not storage.device.is_initialized():
        raise wire.NotInitialized("Device is not initialized")

    if msg.enforce_wordlist is False:
        raise wire.ProcessError(
            "Value enforce_wordlist must be True, Trezor Core enforces words automatically."
        )

    if msg.dry_run:
        # check that only allowed fields are set
        for key, value in msg.__dict__.items():
            if key not in DRY_RUN_ALLOWED_FIELDS and value is not None:
                raise wire.ProcessError(f"Forbidden field set in dry-run: {key}")


async def _continue_dialog(ctx: wire.Context, msg: RecoveryDevice) -> None:
    if not msg.dry_run:
        await confirm_reset_device(ctx, i18n.Text.restore_wallet, recovery=True)
    else:
        await confirm_check_recovery_mnemonic(ctx)


async def _continue_recovery_process(ctx: wire.GenericContext) -> Success:
    # gather the current recovery state from storage
    dry_run = storage.recovery.is_dry_run()
    from trezor.ui import NavigationBack

    secret = None
    while secret is None:
        r = await _request_word_count(ctx, dry_run)
        if isinstance(r, NavigationBack):  
            raise recover.RecoveryAborted
        word_count = r
        
        r = await wallet_import_tip(ctx,i18n.Title.input_words,i18n.Text.input_words,"",False)
        if isinstance(r, NavigationBack):
            print("Cancelled")
            continue
        
        r = await layout.request_mnemonic(ctx, word_count, None)
        if isinstance(r, NavigationBack):
            continue
        words = r
        print("words--",words)
        # if they were invalid or some checks failed we continue and request them again
        if not words:
            continue

        try:
            # await show_popup(i18n.Text.please_wait)
            secret, backup_type = await _process_words(ctx, words)
        except MnemonicError:
            await layout.show_invalid_mnemonic(ctx, words)

    assert backup_type is not None
    if dry_run:
        result = await _finish_recovery_dry_run(ctx, secret, backup_type)
    else:
        result = await _finish_recovery(ctx, secret, backup_type)

    return result


async def _finish_recovery_dry_run(
    ctx: wire.GenericContext, secret: bytes, backup_type: BackupType
) -> Success:
    if backup_type is None:
        raise RuntimeError

    digest_input = sha256(secret).digest()
    stored = mnemonic.get_secret()
    digest_stored = sha256(stored).digest()
    result = utils.consteq(digest_stored, digest_input)

    storage.recovery.end_progress()
    try:
        await layout.show_dry_run_result(ctx, result)
    except Exception as e:
        print(f"Show error: {e}")
    print("result--",result)
    if result:
        return Success(message="The seed is valid and matches the one in the device")
    else:
        raise wire.ProcessError("The seed does not match the one in the device")


async def _finish_recovery(
    ctx: wire.GenericContext, secret: bytes, backup_type: BackupType
) -> Success:
    if backup_type is None:
        raise RuntimeError

    storage.device.store_mnemonic_secret(
        secret, backup_type, needs_backup=False, no_backup=False
    )

    storage.recovery.end_progress()

    await show_success(
        ctx,
        i18n.Text.restore_success,
        title=i18n.Title.wallet_is_ready,
        button=i18n.Button.continue_,
    )
    return Success(message="Device recovered")


async def _request_word_count(ctx: wire.GenericContext, dry_run: bool):
    # ask for the number of words
    return await request_word_count(ctx, dry_run)


async def _process_words(
    ctx: wire.GenericContext, words: str
) -> tuple[bytes | None, BackupType]:
    secret: bytes | None = recover.process_bip39(words)
    return secret, BackupType.Bip39
