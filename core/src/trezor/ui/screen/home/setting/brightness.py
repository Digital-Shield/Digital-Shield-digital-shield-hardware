import lvgl as lv

from . import *

from storage import device
from trezor.ui import display

class Brightness(Item):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.brightness, "A:/res/brightness-two.png")

        # a slider for adjusting brightness
        slider = lv.slider(self)
        slider.set_flex_grow(1)
        slider.set_range(10, 100)
        slider.add_event_cb(self.on_brightness_change, lv.EVENT.VALUE_CHANGED, None)
        slider.set_style_bg_color(lv.color_hex(0x3C84FC), lv.PART.INDICATOR)
        slider.set_style_bg_color(lv.color_hex(0x3C84FC), lv.PART.KNOB)  # 设置旋钮背景为白色

        brightness = device.get_brightness()
        slider.set_value(brightness, lv.ANIM.OFF)

    def on_brightness_change(self, event):
        slider = event.target
        brightness = slider.get_value()
        device.set_brightness(brightness)
        display.backlight(brightness)


