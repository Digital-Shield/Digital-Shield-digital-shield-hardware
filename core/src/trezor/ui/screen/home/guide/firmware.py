import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from trezor.ui import Style, font
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate

if TYPE_CHECKING:
    from typing import List
    pass

class Firmware(Navigate):
    def __init__(self,title):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_title(title)
        #设置字号32
        # self.add_style(Style().text_font(font.Medium.SCS32), 0)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .pad_left(40)
            .pad_right(16)
            .pad_top(25)
            #字号28
            .text_font(font.Regular.SCS30),
            0
        )

        view = self.add(lv.label)
        view.set_text(i18n.Guide.attention_events)
        view.set_width(lv.pct(100))  # 设置固定宽度
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)
        view.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)  # 使用较小的字体

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_1)
        view.set_width(lv.pct(100))  # 设置固定宽度（例如 300 像素）
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)
        view.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)  # 使用较小的字体
        cur_language = i18n.using.code if i18n.using is not None else None
        #阿拉伯语
        if cur_language == "al":
            view.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置文本方向为从右到左

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_2)
        view.set_width(lv.pct(100))
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)
        view.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)  # 使用较小的字体
        #阿拉伯语
        if cur_language == "al":
            view.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置文本方向为从右到左

        view = self.add(lv.label)
        view.set_text(i18n.Guide.firmware_title_3)
        view.set_width(lv.pct(100))
        view.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)
        view.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)  # 使用较小的字体
        #阿拉伯语
        if cur_language == "al":
            view.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置文本方向为从右到左

        style = (
            Style()
            .width(lv.pct(100))
            .pad_right(16)
            .pad_left(16)
            .text_color(lv.color_hex(0xFFFFFF))#lv.color_hex(0xc39700)
        )

        view = self.add(lv.label)
        view.add_style(style,0)
        view.set_long_mode(lv.label.LONG.WRAP)
        view.set_text(i18n.Guide.firmware_title_caution)
        view.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)  # 使用较小的字体
        #阿拉伯语
        if cur_language == "al":
            view.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置文本方向为从右到左

        view = self.add(lv.label)
        view.add_style(style,0)
        view.set_long_mode(lv.label.LONG.WRAP)
        view.set_text(i18n.Guide.firmware_describe_caution)
        view.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)  # 使用较小的字体
        #阿拉伯语
        if cur_language == "al":
            view.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置文本方向为从右到左
