from trezor import utils
from trezor import log, loop
from trezor.ui import lvgl_tick

def check_se_version():
    import thd89
    v = thd89.get_version()
    log.debug(__name__, f"the se version is : {v}")
    itmes = v.split('.')
    if len(itmes) != 3:
        return False

    major = int(itmes[0])
    minor = int(itmes[1])

    # make sure version >= 1.1.x
    if major < 1 or (major == 1 and minor < 1):
        return False
    return True

async def invalid_se_version():
    from trezor.ui.screen.message import Message
    screen = Message("Invalid SE version", "Unsupported SE version was detected, please upgrade the SE firmware.", "A:/res/warning.png")
    await screen.show()
    await screen
    utils.reboot_to_bootloader()


if not utils.EMULATOR and not check_se_version():
    loop.schedule(lvgl_tick())
    loop.schedule(invalid_se_version())
    loop.run()
