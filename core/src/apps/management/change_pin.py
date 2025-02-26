from typing import TYPE_CHECKING

from storage.device import is_initialized
from trezor import config, wire
from trezor.messages import Success
from trezor.ui import i18n
from trezor.ui.layouts import confirm_change_pin, show_success

from apps.common.request_pin import (
    error_pin_invalid,
    error_pin_matches_wipe_code,
    request_pin_and_sd_salt,
    request_pin_confirm,
)

if TYPE_CHECKING:
    from typing import Awaitable

    from trezor.messages import ChangePin


async def change_pin(ctx: wire.Context, msg: ChangePin) -> Success:
    if not is_initialized():
        raise wire.NotInitialized("Device is not initialized")

    # confirm that user wants to change the pin
    await require_confirm_change_pin(ctx)

    # get old pin
    curpin, salt = await request_pin_and_sd_salt(ctx, i18n.Title.enter_old_pin)

    # if changing pin, pre-check the entered pin before getting new pin
    if curpin and not msg.remove:
        if not config.check_pin(curpin, salt):
            await error_pin_invalid(ctx)

    # get new pin
    if not msg.remove:
        newpin = await request_pin_confirm(ctx, show_tip=(not bool(curpin)))
    else:
        newpin = ""

    # write into storage
    if not config.change_pin(curpin, newpin, salt, salt):
        if newpin:
            await error_pin_matches_wipe_code(ctx)
        else:
            await error_pin_invalid(ctx)

    if newpin:
        if curpin:
            msg_screen = i18n.Text.pin_change_success
            msg_wire = i18n.Title.pin_changed
        else:
            msg_screen = i18n.Text.pin_enable_success
            msg_wire = i18n.Title.pin_enabled
    else:
        msg_screen = i18n.Text.pin_disable_success
        msg_wire = i18n.Title.pin_disabled

    await show_success(
        ctx,
        msg_screen,
        title=msg_wire,
        button=i18n.Button.done,
    )
    return Success(message=msg_wire)


def require_confirm_change_pin(ctx: wire.Context) -> Awaitable[None]:
    return confirm_change_pin(ctx)
