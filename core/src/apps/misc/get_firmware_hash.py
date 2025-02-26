from typing import TYPE_CHECKING

from trezor import ui, wire, workflow
from trezor.messages import FirmwareHash, GetFirmwareHash
from trezor.ui.layouts import show_popup
from trezor.utils import DISABLE_ANIMATION, firmware_hash

if TYPE_CHECKING:
    from trezor.wire import Context


async def get_firmware_hash(ctx: Context, msg: GetFirmwareHash) -> FirmwareHash:
    from trezor.ui import i18n

    await show_popup(i18n.Text.please_wait)

    try:
        hash = firmware_hash(msg.challenge, _render_progress)
    except ValueError as e:
        raise wire.DataError(str(e))

    return FirmwareHash(hash=hash)


def _render_progress(progress: int, total: int) -> None:
    if not DISABLE_ANIMATION:
        p = 1000 * progress // total
        ui.display.loader(p, False, 18, ui.WHITE, ui.BG)
        ui.refresh()
