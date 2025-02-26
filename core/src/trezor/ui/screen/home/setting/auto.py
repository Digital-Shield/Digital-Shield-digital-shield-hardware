import lvgl as lv

from . import *
from .options import TimeOptionDetails
from storage import device


class AutoLock(OptionsItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.auto_lock, "A:/res/lock-setting.png")

        # seconds, -1 means never
        self.times = [30, 60, 120, 300, 600, -1]

    def current(self):
        cur = AutoLockDetails.current()
        return AutoLockDetails.option_format(cur)

    def show_options(self):
        screen = AutoLockDetails(i18n.Setting.auto_lock, self.times)
        screen.subscriber = self
        from trezor import workflow
        workflow.spawn(screen.show())
class AutoLockDetails(TimeOptionDetails):
    def __init__(self, title, times):
        super().__init__(title, times)

    @classmethod
    def current(cls):
        t = device.get_autolock_delay_ms()
        return t // 1000

    def save_option(self, option):
        device.set_autolock_delay_ms(option * 1000)
        from apps.base import reload_settings_from_storage
        reload_settings_from_storage()

class AutoShutdown(OptionsItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.auto_shutdown, "A:/res/auto-power-off.png")
        # seconds, -1 means never
        self.times = [60, 120, 300, 600, 900, 1800, -1]

    def current(self):
        cur = AutoShutdownDetails.current()
        return AutoShutdownDetails.option_format(cur)

    def show_options(self):
        screen = AutoShutdownDetails(i18n.Setting.auto_shutdown, self.times)
        screen.subscriber = self
        from trezor import workflow
        workflow.spawn(screen.show())

class AutoShutdownDetails(TimeOptionDetails):
    def __init__(self, title, times):
        super().__init__(title, times)

    @classmethod
    def current(cls):
        t = device.get_autoshutdown_delay_ms()
        return t // 1000

    def save_option(self, option):
        device.set_autoshutdown_delay_ms(option * 1000)
        from apps.base import reload_settings_from_storage
        reload_settings_from_storage()
