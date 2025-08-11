from trezor import ui, wire
from trezor.ui import i18n
from trezor.ui.layouts import show_success, show_success_create, show_warning
from trezor.ui.layouts import (  # noqa: F401
    confirm_words,
    show_words,
)

async def show_internal_entropy(ctx: wire.GenericContext, entropy: bytes) -> None:
    return


async def _show_confirmation_success(
    ctx: wire.GenericContext,
) -> None:
    title = i18n.Title.verified
    text = i18n.Text.backup_verified
    return await show_success_create(
        ctx,
        text,
        title,
        button=i18n.Button.continue_,
    )


async def _show_confirmation_failure(ctx: wire.GenericContext) -> None:
    title = i18n.Title.invalid_mnemonic
    text = i18n.Text.backup_invalid

    await show_warning(
        ctx,
        text,
        title,
        button=i18n.Button.try_again,
    )


async def show_backup_success(ctx: wire.GenericContext) -> None:

    title = i18n.Title.wallet_is_ready
    text = i18n.Text.create_success
    await show_success_create(
        ctx, text, title, button=i18n.Button.continue_
    )


# BIP39
# ===


async def bip39_show_and_confirm_mnemonic(
    ctx: wire.GenericContext, mnemonic: str
):
    # warn user about mnemonic safety
    # await show_backup_warning(ctx)
    words = mnemonic.split()
    while True:
        # display paginated mnemonic on the screen
        r = await show_words(ctx, share_words=words)
        if isinstance(r, ui.Redo):
            return r
        while True:
            try:
                r = await confirm_words(ctx, words)
            except wire.ActionCancelled:
                # user navigation back, do `show` again
                break
            if r:
                await _show_confirmation_success(ctx)
                return
            else:
                await _show_confirmation_failure(ctx)
