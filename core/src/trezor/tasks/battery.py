"""
background task for updating battery
"""
from trezor import io, utils, loop, log
from trezor.ui.screen.statusbar import StatusBar
battery = io.Battery()

async def updating_battery_state():
    prev_charge = None
    prev_charging = None
    while True:
        # update battery every second
        await loop.sleep(1000)

        state_of_charge = battery.state_of_charge()
        # log.debug(__name__, f"state of battery: {state_of_charge}")
        state_of_current = battery.state_of_current()
        # log.debug(__name__, f"state of current: {state_of_current}")

        charging = state_of_current >= 0
        
        # need refresh if charge state changed
        refresh = prev_charge != state_of_charge
        # need refresh if charging is chaged
        refresh |= prev_charging != charging

        if not refresh:
            continue

        if state_of_charge is None:
            prev_charge = state_of_charge
            StatusBar.instance().show_battery_none()
            continue
        
        # cache charge state
        if prev_charge != state_of_charge:
            prev_charge = state_of_charge
            StatusBar.instance().show_battery_img(state_of_charge, charging)
            
        # cache charging state
        if prev_charging != charging:
            StatusBar.instance().show_charging(charging)
            prev_charging = charging

