
import lvgl as lv

from . import *
from trezor import motor
from storage import device

class Vibration(ToggleItem):

    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.vibration, "A:/res/vibration-two.png")
        self.checked = device.keyboard_haptic_enabled()

    def toggle(self):
        # 1. vibrate to indicate change
        motor.vibrate()
        enabled = self.checked
        log.debug(__name__, f"keyboard haptic {'enabled' if enabled else 'disabled'}")
        device.toggle_keyboard_haptic(enabled)
        # 2. vibrate again
        # wether enable or disable keyboard haptic, `1` and `2` will vibrate to indicate change
        motor.vibrate()
