"""
background task for updating battery
"""
from trezor import io, utils, loop, log
from trezor.ui.screen.statusbar import StatusBar
battery = io.Battery()

async def updating_battery_state():
    prev_charging = None
    while True:
        state_of_charge = battery.state_of_charge()
        # log.debug(__name__, f"state of battery: {state_of_charge}")
        state_of_current = battery.state_of_current()
        # log.debug(__name__, f"state of current: {state_of_current}")

        charging = state_of_current >= 0

        if state_of_charge is None:
            StatusBar.instance().show_battery_none()
        else:
            StatusBar.instance().show_battery_img(state_of_charge, charging)
            
            # cache charging state
            if prev_charging != charging:
                StatusBar.instance().show_charging(charging)
                prev_charging = charging

        # update battery every second
        await loop.sleep(1000)
