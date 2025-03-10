import lvgl as lv

from . import *

from trezor import utils
from trezor.ui import colors

class PowerOff(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.power_off, "A:/res/power-off.png")
        self.label.set_style_text_color(colors.DS.DANGER, lv.PART.MAIN)

        enable = not utils.is_usb_connected()
        log.debug(__name__, f"power source: {'battery' if enable else 'USB'}")
        log.debug(__name__, f"power off is {'enabled' if enable else 'disabled'}")
        if enable:
            self.clear_state(lv.STATE.DISABLED)
        else:
            self.add_state(lv.STATE.DISABLED)

    def action(self):
        log.debug(__name__, "power off")
        from trezor import workflow
        from trezor.ui.screen.power import PowerOff as ConfirmPowerOff
        screen = ConfirmPowerOff()
        workflow.spawn(screen.show())
class Restart(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.restart, "A:/res/restart.png")
        self.label.set_style_text_color(colors.DS.DANGER, lv.PART.MAIN)

    def action(self):
        log.debug(__name__, "restart")
        from trezor import workflow
        from trezor.ui.screen.power import Restart as ConfirmRestart
        screen = ConfirmRestart()
        workflow.spawn(screen.show())
