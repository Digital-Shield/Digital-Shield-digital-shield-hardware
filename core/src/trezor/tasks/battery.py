"""
background task for updating battery
"""
from trezor import io, utils, loop, log
from trezor.ui.screen.statusbar import StatusBar
battery = io.Battery()

async def updating_battery_state():
    while True:
        state_of_charge = battery.state_of_charge()
        # log.debug(__name__, f"state of battery: {state_of_charge}")
        if state_of_charge is None:
            StatusBar.instance().show_battery_none()
        else:
            StatusBar.instance().show_battery_img(state_of_charge, utils.BATTERY_CHARGING)

        # update battery every second
        await loop.sleep(1000)
