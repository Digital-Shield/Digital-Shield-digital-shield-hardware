import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from trezor.ui import Style, font
from trezor.ui.screen import Navigation, with_title

if TYPE_CHECKING:
    from typing import List
    pass

class Firmware(with_title(Navigation)):
    def __init__(self,title):
        super().__init__()
        self.set_title(title)
        self.create_content(HStack)
        self.content: HStack
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            self.content.add_style(
                Style()
                .pad_left(16)
                .pad_right(16)
                .pad_top(25)
                .text_align(lv.TEXT_ALIGN.RIGHT),  # 添加右对齐样式
                0
            )
        else:
            self.content.add_style(
                Style()
                .pad_left(16)
                .pad_right(16)
                .pad_top(25),
                0
            )

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_1)
        view.set_width(lv.pct(100))  # 设置固定宽度（例如 300 像素）
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)
        # view.set_style_text_font(font.Bold.SCS26, lv.PART.MAIN)  # 使用较小的字体

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_2)
        view.set_width(lv.pct(100))
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_3)
        view.set_width(lv.pct(100))
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)

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
        cur_language = i18n.using.code if i18n.using is not None else None
