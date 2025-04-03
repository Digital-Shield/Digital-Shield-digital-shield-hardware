import lvgl as lv

from . import Modal, with_title

from trezor import log
from trezor.ui.component.keyboard import PinKeyboard
from trezor.ui import Style, font, colors, i18n, Cancel
from trezor.ui.constants import MAX_PIN_LENGTH, MIN_PIN_LENGTH
from trezor.ui.component.container import HStack


class InputPinScreen(with_title(Modal)):
    def __init__(self, title: str | None = None):
        super().__init__()
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色
        tip = lv.label(self)# 创建一个label
        tip.set_text(title)# 设置文本
        #获取当前语言,如果是阿拉伯语则右对齐,否则左对齐
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            # log.debug(__name__, f"current pin con--: {i18n.Title.enter_pin}")
            #置文本方向为从右到左
            tip.set_style_base_dir(lv.BASE_DIR.RTL, lv.PART.MAIN)
        tip.align(lv.ALIGN.TOP_MID, 0, -32)# 设置位置
        tip.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)# 设置文本颜色
        tip.set_style_text_font(font.Bold.SCS30, 0)

        self.create_content(HStack)
        self.content: HStack

        self.content.set_height(lv.SIZE.CONTENT)
        self.content.items_center()
        self.content.align(lv.ALIGN.BOTTOM_MID, 0, 0)

        self.ta = self.add(lv.textarea)

        self.ta.set_password_mode(True)
        # only allow numbers
        self.ta.set_accepted_chars("0123456789")
        self.ta.set_one_line(True)
        self.ta.set_max_length(MAX_PIN_LENGTH)
        self.ta.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.ta.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        self.ta.add_style(
            Style()
            # .bg_color(colors.DS.BLACK)
            # .border_color(colors.STD.WHITE)
            # .border_side(lv.BORDER_SIDE.BOTTOM),
            .border_width(0)
            .text_color(colors.STD.WHITE)
            .bg_opa(lv.OPA.TRANSP)
            .width(lv.pct(80))
            .text_font(font.Bold.SCS48)
            .text_letter_space(8)
            .text_align_center(),
            lv.PART.MAIN,
        )
        label = self.ta.get_label()
        label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        
        kbd = self.add(PinKeyboard)
        kbd.textarea = self.ta
        kbd.tip_count_min = MIN_PIN_LENGTH
        kbd.max_pin_length = MAX_PIN_LENGTH
        kbd.min_pin_length = MIN_PIN_LENGTH
        kbd.add_event_cb(lambda e: self.input_done(), lv.EVENT.READY, None)
        kbd.add_event_cb(lambda e: self.cancel(), lv.EVENT.CANCEL, None)

    def warning(self, msg: str):
        """
        Show a warning msg when show PIN screen
        """
        if not msg:
            return
        warn = self.add(lv.label)
        warn.set_width(lv.pct(100))
        warn.move_to_index(0)
        warn.set_text(msg)

        warn.set_long_mode(lv.label.LONG.WRAP)
        warn.add_style(
            Style()
            .text_color(colors.DS.DANGER)
            .text_align(lv.TEXT_ALIGN.CENTER),
            lv.PART.MAIN,
        )

    def input_done(self):
        pin = self.ta.get_text()
        self.close(pin)

    def cancel(self):
        self.close(Cancel())

