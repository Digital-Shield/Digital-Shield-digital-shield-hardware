from typing import TYPE_CHECKING

import storage
from trezor import wire
from trezor.messages import Success

from ..common.request_pin import verify_user_pin
from apps.base import reload_settings_from_storage

from trezor.ui.layouts import confirm_wipe_device, confirm_wipe_device_tips, confirm_wipe_device_success

if TYPE_CHECKING:
    from trezor.messages import WipeDevice
    pass


async def wipe_device(ctx: wire.GenericContext, msg: WipeDevice) -> Success:
    await confirm_wipe_device(ctx)
    # verify user pin
    await verify_user_pin(ctx)
    # show tips
    await confirm_wipe_device_tips(ctx)
    storage.wipe()
    reload_settings_from_storage()
    await confirm_wipe_device_success(ctx)
    if ctx == wire.DUMMY_CONTEXT:
        # if a dummy context which means a operation on device , we should restart the device
        from trezor import utils

        utils.reset()
    return Success(message="Device wiped")
