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
    if not by_battery:
        return
    while True:
        if pressing:
            wait_button = loop.wait(io.BUTTON)
            long_time = loop.sleep(2000)
            racer = loop.race(wait_button, long_time)
            await racer
            pressing = False
            if wait_button in racer.finished:
                log.debug(__name__, "Power key released in 2 seconds")
                screen = PowerOff()
                await screen.show()
                # wait done
                await screen
            elif long_time in racer.finished:
                log.debug(__name__, "Long time press power key detected")
                log.debug(__name__, "force power off ...")
                screen = ShutingDown()
                await screen.show()
                await screen
                break
        else :
            evt, btn = await loop.wait(io.BUTTON)
            name = "Power key" if btn == io.BUTTON_POWER else "Unknown key"
            event = "Pressed" if evt == io.BUTTON_PRESSED else "Released" if evt == io.BUTTON_RELEASED else "Unknown event"
            log.debug(__name__, f"{name} {event}")
            pressing = True if evt == io.BUTTON_PRESSED else False
            # pop up power off dialog
            utils.lcd_resume()
