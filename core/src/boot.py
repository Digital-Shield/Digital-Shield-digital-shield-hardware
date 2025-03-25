import storage
from trezor import config, io, log, loop, ui, utils
from trezor.ui import lvgl_tick

lvgl_task = lvgl_tick()


log.info("boot", "lvgl_task successfully")


def clear() -> None:
    """if device is not initialized, pin is needless, so clear it"""
    if not storage.device.is_initialized() and config.has_pin():
        storage.wipe()
    if config.has_pin() and config.get_pin_rem() == 0:
        storage.wipe()
    # if not utils.EMULATOR:
    #     if storage.device.get_wp_cnts() == 0:
    #         for _size, _attrs, name in io.fatfs.listdir("1:/res/wallpapers"):
    #             io.fatfs.unlink(f"1:/res/wallpapers/{name}")

async def boot() -> None:
    from apps.common.request_pin import can_lock_device, verify_user_pin
    from trezor.ui.screen.bootscreen import BootScreen
    screen = BootScreen()
    await screen.show()
    await screen

    if not can_lock_device():
        await verify_user_pin()
        storage.init_unlocked()

    loop.close(lvgl_task)


loop.schedule(lvgl_task)
config.init(None)
ui.display.backlight(storage.device.get_brightness())
clear()
loop.schedule(boot())
loop.run()
