"""
background task for updating battery
"""
from trezor import io, utils, loop, log
from trezor.ui.screen.statusbar import StatusBar
battery = io.Battery()

LOW_STATE_OF_CHARGE = 5


async def updating_battery_state():

    prev_charge = None
    prev_charging = None
    charging_changed = False
    state_of_charge = None
    state_of_charge_changed = False
    alert = LowPowerAlert()
    while True:
        # update battery every second
        await loop.sleep(1000)

        if not battery.exist():
            prev_charge = state_of_charge
            StatusBar.instance().show_battery_none()
            continue

        state_of_charge = battery.state_of_charge()
        # log.debug(__name__, f"battery state of charge: {state_of_charge}%%")
        # current = battery.current()
        # log.debug(__name__, f"battery current: {current}mA")
        voltage = battery.voltage()
        # log.debug(__name__, f"battery voltage: {voltage}mV")

        charging = battery.charging()

        charging_changed = prev_charging != charging
        prev_charging = charging

        state_of_charge_changed = prev_charge != state_of_charge
        prev_charge = state_of_charge

        # need refresh if charge state changed or charging changed
        refresh = charging_changed or state_of_charge_changed

        if not refresh:
            continue

        # cache charge state
        if state_of_charge_changed:
            prev_charge = state_of_charge
            StatusBar.instance().show_battery_img(state_of_charge, charging)

        # cache charging state
        if charging_changed:
            StatusBar.instance().show_battery_img(state_of_charge, charging)
            StatusBar.instance().show_charging(charging)
            prev_charging = charging

            if charging:
                # reset alert state
                alert.destroy()
                del alert
                alert = LowPowerAlert()

        if charging_changed or state_of_charge_changed:
            # less than 20%, show a message
            if not charging and state_of_charge <= LOW_STATE_OF_CHARGE:
                await alert(state_of_charge)

        # not connect usb, and battery is empty, shut down device
        if not state_of_charge and not charging:
            from trezor.ui.screen.power import ShutingDown
            screen = ShutingDown()
            await screen.show()
            await screen

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    AlertState = Literal[
        # Just create
        'None',
        # Showing `LowPower` screen
        'Showing',
        # user have click confirm, screen has disappeared
        'Confirmed'
        ]
from trezor.ui.screen.power import LowPower

class LowPowerAlert():
    state: AlertState
    screen: LowPower | None
    def __init__(self):
        self.state = 'None'
        self.screen = None

    def destroy(self):
        from trezor.ui import Cancel
        if self.screen:
            self.screen.close(Cancel())

    async def __call__(self, charge: int):
        if self.state == 'Confirmed':
            return
        elif self.state == 'Showing':
            self.screen.update_charge(charge)
        elif self.state == 'None':
            self.state = 'Showing'
            self.screen = LowPower(charge)
            # self.screen.on_confirm = self.on_confirm
            await self.screen.show()

    def on_confirm(self):
        self.state = 'Confirmed'
        self.screen = None
