import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from trezor.ui.screen import Navigation

if TYPE_CHECKING:
    from typing import List
    pass

class Firmware(Navigation):
    def __init__(self,title):
        super().__init__()
        self.set_title(title)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .pad_left(16)
            .pad_right(16)
            .pad_top(25),
            0
        )

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_1)
        view.set_width(lv.pct(100))
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_2)
        view.set_width(lv.pct(100))
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_3)
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)

        style = (
            Style()
            .width(lv.pct(100))
            .pad_right(16)
            .pad_left(16)
            .text_color(lv.color_hex(0xc39700))
        )

        view = self.add(lv.label)
        view.add_style(style,0)
        view.set_long_mode(lv.label.LONG.WRAP)
        view.set_text(i18n.Guide.firmware_title_caution)

        view = self.add(lv.label)
        view.add_style(style,0)
        view.set_long_mode(lv.label.LONG.WRAP)
        view.set_text(i18n.Guide.firmware_describe_caution)
