""""
background task for handling power button events
"""

from trezor import io, log, loop, utils
from trezor.ui.screen.power import PowerOff, ShutingDown

async def handle_power():
    pressing = False
    source = utils.power_source()
    by_battery = source == utils.POWER_SOURCE_BATTERY
    log.debug(__name__, f"powered by {'battery' if by_battery else 'USB'}")

    # powered by USB, can't power off
    while True:
        if pressing:
            wait_button = loop.wait(io.BUTTON)
            long_time = loop.sleep(2000)
            racer = loop.race(wait_button, long_time)
            await racer
            if wait_button in racer.finished:
                log.debug(__name__, "Power key released in 2 seconds")
                log.debug(__name__, "toggle screen state")
                utils.toggle_lcd()
                # wait a short time, avoid button shake
                await loop.sleep(50)
                pressing = False
            elif long_time in racer.finished:
                if not by_battery or utils.is_usb_connected():
                    continue
                pressing = False
                log.debug(__name__, "Long time press power key detected")
                log.debug(__name__, "power off ...")
                utils.lcd_resume()
                screen = PowerOff()
                await screen.show()
                await screen
                await screen.wait_unloaded()
        else :
            evt, btn = await loop.wait(io.BUTTON)
            name = "Power key" if btn == io.BUTTON_POWER else "Unknown key"
            event = "Pressed" if evt == io.BUTTON_PRESSED else "Released" if evt == io.BUTTON_RELEASED else "Unknown event"
            log.debug(__name__, f"{name} {event}")
            pressing = True if evt == io.BUTTON_PRESSED else False
