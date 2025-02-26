from typing import TYPE_CHECKING

import storage.recovery
from trezor import ui, wire
from trezor.ui import i18n
from trezor.enums import ButtonRequestType
from trezor.ui.layouts import (
    show_success,
    show_warning,
)

if TYPE_CHECKING:
    from trezor.enums import BackupType
    pass


async def request_mnemonic(
    ctx: wire.GenericContext, word_count: int, backup_type: BackupType | None
) -> str | None:
    from trezor.ui.screen.initialize.mnemonic import MnemonicInput
    from trezor.ui import NavigationBack
    screen = MnemonicInput(word_count)
    await screen.show()
    r = await screen
    if isinstance(r, NavigationBack):
        raise wire.ActionCancelled()
    words = screen.mnemonics
    return ' '.join(words)

async def show_dry_run_result(
    ctx: wire.GenericContext, result: bool
) -> None:
    if result:
        await show_success(
            ctx,
            i18n.Text.backup_verified,
            title= i18n.Title.verified,
        )
    else:
        text = i18n.Text.check_recovery_not_match
        await show_warning(
            ctx,
            text,
            button=i18n.Button.try_again,
            title=i18n.Title.mnemonic_not_match,
        )


async def show_dry_run_different_type(ctx: wire.GenericContext) -> None:
    await show_warning(
        ctx,
        title="Dry run failure",
        msg="Seed in the device was\ncreated using another\nbackup mechanism.",
    )


async def show_invalid_mnemonic(ctx: wire.GenericContext) -> None:
    title = i18n.Title.invalid_mnemonic
    text = i18n.Text.invalid_recovery_mnemonic
    await show_warning(
        ctx,
        text,
        title= title,
        button=i18n.Button.try_again,
    )


async def show_share_already_added(ctx: wire.GenericContext) -> None:
    await show_warning(
        ctx,
        "Share already entered,\nplease enter\na different share.",
    )


async def show_identifier_mismatch(ctx: wire.GenericContext) -> None:
    await show_warning(
        ctx,
        "You have entered\na share from another\nShamir Backup.",
    )


async def show_group_threshold_reached(ctx: wire.GenericContext) -> None:
    await show_warning(
        ctx,
        "Threshold of this\ngroup has been reached.\nInput share from\ndifferent group.",
    )
