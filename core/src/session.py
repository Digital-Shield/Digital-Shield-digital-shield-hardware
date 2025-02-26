from trezor import log, loop, utils
from trezor.ui import lvgl_tick
from trezor.ui.screen.manager import monitor_task
from trezor.uart import handle_ble_info, handle_uart, handle_usb_state

# register background tasks
from trezor import tasks as _

import apps.base

apps.base.boot()

if __debug__:
    import apps.debug

    apps.debug.boot()

# run main event loop and specify which screen is the default
loop.schedule(apps.base.set_homescreen())

loop.schedule(handle_uart())

loop.schedule(handle_ble_info())

loop.schedule(handle_usb_state())

loop.schedule(lvgl_tick())

loop.schedule(monitor_task())

utils.set_up()
if utils.show_app_guide():
    from trezor.ui.layouts import show_app_guide

    loop.schedule(show_app_guide())

loop.run()

if __debug__:
    log.debug(__name__, "Restarting main loop")
