# from trezor import utils

from typing import TYPE_CHECKING

from trezor import log, wire, workflow, loop
from trezor.enums import ButtonRequestType
from trezor.messages import ButtonAck, ButtonRequest
from trezor.ui import i18n, colors
from trezor.ui import NavigationBack

if TYPE_CHECKING:
    from typing import Any, Awaitable, TypeVar, Sequence

    T = TypeVar("T")
    LayoutType = Awaitable[Any]

from .helper import *

# import `show` function for easy use
from .bitcoin import show_xpub, show_pubkey


# messages functions
async def show_popup(
    operation: str,
    timeout_ms: int = 3000,
    icon: str | None = None,
) -> None:
    from trezor.ui.screen.popup import Popup

    screen = Popup(operation, icon)
    await screen.show()
    screen.auto_close_timeout = timeout_ms
    await screen


async def show_pairing_error() -> None:
    await show_popup(
        i18n.Text.bluetooth_pair_failed,
        timeout_ms=2000,
        icon="A:/res/error.png",
    )


async def show_app_guide() -> None:
    # TODO: implement
    pass


async def show_airgap_signature(sig: str):
    from trezor.ui.screen.airgap import EthSignature

    screen = EthSignature(sig)
    await screen.show()
    await screen


async def show_success(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Success",
    button: str = i18n.Button.done,
) -> Awaitable[None]:
    from trezor.ui.screen.message import Success

    screen = Success(title, msg)
    screen.button_text(button)
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Success))


async def show_warning(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Warning",
    button: str = i18n.Button.try_again,
) -> Awaitable[None]:
    from trezor.ui.screen.message import Warning

    screen = Warning(title, msg)
    screen.button_text(button)
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Warning))


async def show_error(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Error",
    button: str = i18n.Button.try_again,
) -> Awaitable[None]:
    from trezor.ui.screen.message import Error

    screen = Error(title, msg)
    screen.button_text(button)
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Warning))


async def show_address(
    ctx: wire.GenericContext,
    address: str,
    path: str,
    network: str,
    chain_id: int | None = None,
):
    from trezor.ui.screen.template import Address

    screen = Address(address, path, network, chain_id)
    await screen.show()
    return await interact(ctx, screen, ButtonRequestType.Address)


# confirm functions
async def hold_confirm_action(
    ctx: wire.GenericContext, title: str, msg: str, br_code=ButtonRequestType.Other
):
    from trezor.ui.screen.template import HoldConfirmAction

    screen = HoldConfirmAction(msg)
    icon = None
    if hasattr(ctx, "icon_path"):
        icon = ctx.icon_path
    screen.set_title(title, icon)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, br_code))


async def confirm_action(
    ctx: wire.GenericContext, title: str, msg: str, br_code=ButtonRequestType.Other
):
    from trezor.ui.screen.confirm import SimpleConfirm

    screen = SimpleConfirm(msg)
    screen.title.set_text(title)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, br_code))


async def confirm_final(ctx: wire.GenericContext, chain_name: str) -> None:
    # confirm
    await hold_confirm_action(
        ctx,
        i18n.Title.confirm_transaction,
        i18n.Text.do_sign_this_transaction.format(chain_name),
        ButtonRequestType.SignTx,
    )
    # show success
    await show_popup(
        i18n.Text.transaction_signed, timeout_ms=3000, icon="A:/res/success.png"
    )


async def confirm_set_homescreen(ctx, replace: bool = False):
    msg = i18n.Text.set_as_homescreen
    if replace:
        msg = i18n.Text.replace_homescreen
    await confirm_action(
        ctx,
        i18n.Title.set_as_homescreen,
        msg,
    )

## wipe device
async def confirm_wipe_device(ctx: wire.GenericContext):
    from trezor.ui.screen.confirm import SimpleConfirm

    screen = SimpleConfirm(i18n.Text.wipe_device)
    screen.btn_confirm.color(colors.DS.DANGER)
    screen.btn_confirm.set_text(i18n.Button.continue_)
    screen.text_color(colors.DS.DANGER)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.WipeDevice))


async def confirm_wipe_device_tips(ctx: wire.GenericContext):
    from trezor.ui.screen.management.wipe_device import WipeDeviceTips

    screen = WipeDeviceTips()
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.WipeDevice))


async def confirm_wipe_device_success(ctx: wire.GenericContext):
    from trezor.ui.screen.message import Info

    screen = Info(None, i18n.Text.wipe_device_success)
    screen.button_text(i18n.Button.continue_)
    await screen.show()
    return await interact(ctx, screen, ButtonRequestType.WipeDevice)


async def mnemonic_security_tip(ctx: wire.GenericContext) -> bool:
    from trezor.ui.screen.initialize.xsecurity import MnemonicSecurity

    screen = MnemonicSecurity()
    await screen.show()
    await interact(
        ctx,
        screen,
        ButtonRequestType.ResetDevice,
    )

async def request_pin_on_device(
    ctx: wire.GenericContext,
    prompt: str,
    attempts_remaining: int | None,
    allow_cancel: bool,
) -> str:
    await button_request(ctx, code=ButtonRequestType.PinEntry)
    from storage import device

    if attempts_remaining is None or attempts_remaining == device.PIN_MAX_ATTEMPTS:
        subprompt = ""
    elif attempts_remaining == 1:
        subprompt = i18n.Text.incorrect_pin_last_time
    else:
        subprompt = i18n.Text.incorrect_pin_times_left.format(attempts_remaining)
    from trezor.ui.screen.pin import InputPinScreen

    screen = InputPinScreen(prompt)
    screen.warning(subprompt)
    await screen.show()
    result = await ctx.wait(screen)
    if not result:
        if not allow_cancel:
            loop.clear()
        raise wire.PinCancelled
    assert isinstance(result, str)
    return result

async def request_word_count(ctx: wire.GenericContext, dry_run: bool) -> int | NavigationBack:
    from trezor.ui.screen.initialize.wordcount import WordcountScreen
    from trezor.ui.screen import manager
    screen = manager.try_switch_to(WordcountScreen)
    if not screen:
        screen = WordcountScreen()
        await screen.show()

    r = await interact(ctx, screen, ButtonRequestType.MnemonicWordCount)
    if isinstance(r, NavigationBack):
        return r
    return int(r)

async def request_mnemonic(ctx, word_count: int) -> str | NavigationBack:
    from trezor.ui.screen.initialize.mnemonic import MnemonicInput
    screen = MnemonicInput(word_count)
    await screen.show()
    r = await interact(ctx, screen, ButtonRequestType.MnemonicInput)
    if isinstance(r, NavigationBack):
        await screen.wait_unloaded()
        return r
    words = screen.mnemonics
    return ' '.join(words)

async def request_strength(ctx) -> int:
    word_cnt_strength_map = {
        12: 128,
        18: 192,
        24: 256,
    }

    from trezor.ui.screen.initialize.wordcount import WordcountScreen

    screen = WordcountScreen()
    await screen.show()
    count = await interact(ctx, screen, ButtonRequestType.MnemonicWordCount)
    if not isinstance(count, int):
        raise wire.ActionCancelled()
    return word_cnt_strength_map[count]


async def confirm_reset_device(
    ctx: wire.GenericContext, prompt: str, recovery: bool = False
) -> None:
    from trezor.ui.screen.message import Info

    title = i18n.Title.restore_wallet if recovery else i18n.Title.create_wallet
    screen = Info(title, prompt)
    await screen.show()
    await raise_if_cancelled(
        interact(
            ctx,
            screen,
            (
                ButtonRequestType.ProtectCall
                if recovery
                else ButtonRequestType.ResetDevice
            ),
        )
    )


async def confirm_check_recovery_mnemonic(ctx: wire.GenericContext):
    from trezor.ui.screen.message import Info

    title = i18n.Title.check_recovery_mnemonic
    text = i18n.Text.check_recovery_mnemonic
    screen = Info(title, text)
    screen.button_text(i18n.Button.continue_)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.ProtectCall))


async def confirm_pin_security(
    ctx: wire.GenericContext, prompt: str, recovery: bool = False
) -> None:
    from trezor.ui.screen.initialize.xsecurity import PinSecurity

    screen = PinSecurity()
    await screen.show()
    await raise_if_cancelled(
        interact(
            ctx,
            screen,
            (
                ButtonRequestType.ProtectCall
                if recovery
                else ButtonRequestType.ResetDevice
            ),
        )
    )


async def confirm_change_pin(ctx: wire.GenericContext):
    from trezor.ui.screen.message import Info

    title = i18n.Security.change_pin
    text = i18n.Text.change_pin
    screen = Info(title, text)
    screen.button_text(i18n.Button.continue_)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Other))


__show_screen = None


async def show_words(
    ctx: wire.GenericContext,
    share_words: Sequence[str],
) -> None:
    from trezor.ui.screen.initialize.mnemonic import MnemonicDisplay

    if __debug__:
        from apps import debug

        def export_displayed_words() -> None:
            # export currently displayed mnemonic words into debuglink
            debug.reset_current_words.publish(share_words)

        export_displayed_words()
    log.debug(__name__, f"words: {share_words}")
    global __show_screen
    if not __show_screen:
        __show_screen = MnemonicDisplay()
        __show_screen.update_mnemonics(share_words)
        await __show_screen.show()
    else:
        __show_screen.update_mnemonics(share_words)

    # confirm the share
    return await raise_if_cancelled(
        interact(
            ctx,
            __show_screen,
            ButtonRequestType.ResetDevice,
        )
    )


async def confirm_words(ctx: wire.GenericContext, share_words: Sequence[str]) -> bool:
    from trezor.ui.screen.initialize.mnemonic import MnemonicDisplay, MnemonicCheck
    from trezor.crypto import random

    rnd_words = [x for x in share_words]
    random.shuffle(rnd_words)
    # log.debug(__name__, f"original words: {share_words}")
    # log.debug(__name__, f"random words: {rnd_words}")
    screen = MnemonicCheck()
    screen.update_mnemonics(rnd_words)
    await screen.show()

    r = await interact(ctx, screen, ButtonRequestType.Other)
    if not r:
        raise wire.ActionCancelled()
    log.debug(__name__, f"checked words: {r}")

    return r == share_words


async def confirm_sign_message(
    ctx: wire.GenericContext,
    coin: str,
    message: str,
    *,
    address: str,
    chain_id: int | None = None,
):
    from trezor.ui.screen.template import SignMessage

    title = i18n.Title.sign_message.format(coin)
    screen = SignMessage(title, message, address=address, chain_id=chain_id)
    screen.set_mode("sign")
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen))
    # show success
    await show_popup(
        i18n.Text.transaction_signed, timeout_ms=3000, icon="A:/res/success.png"
    )


async def confirm_verify_message(
    ctx: wire.GenericContext,
    coin: str,
    message: str,
    *,
    address: str,
    chain_id: int | None = None,
):
    from trezor.ui.screen.template import SignMessage

    title = i18n.Title.verify_message.format(coin)
    screen = SignMessage(title, message, address=address, chain_id=chain_id)
    screen.set_mode("verify")
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen))


async def confirm_blob(
    ctx: wire.GenericContext,
    title: str,
    message: str,
    *,
    description: str,
    blob: bytes,
    br_code=ButtonRequestType.Other,
):
    from trezor.ui.screen.template import Blob

    screen = Blob(title, message, label=description, blob=blob)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, br_code=br_code))

async def confirm_metadata(
    ctx: wire.GenericContext,
    title: str,
    message: str,
    *,
    description: str,
    data: bytes,
    br_code=ButtonRequestType.Other,
):
    return await confirm_blob(
        ctx, title, message, blob=data, description=description, br_code=br_code
    )

async def confirm_data(
    ctx: wire.GenericContext,
    title: str,
    data: bytes,
    *,
    description: str,
    br_code: ButtonRequestType,
):
    return await confirm_blob(
        ctx, title, "", blob=data, description=description, br_code=br_code
    )


async def confirm_text(
    ctx: wire.GenericContext, title: str, text: str, *, description: str
):
    return await confirm_blob(ctx, title, "", blob=text, description=description)
