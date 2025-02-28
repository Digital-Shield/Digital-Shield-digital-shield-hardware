import lvgl as lv
from micropython import const

from trezor.ui.constants import MAX_PIN_LENGTH, MIN_PIN_LENGTH
from trezor.ui import colors, Style, font
from trezor.ui.theme import Styles
from trezor.ui.component.container import VStack
from trezor import motor, loop, log, utils
from storage import device
from trezor.crypto import random, bip39
from typing import TYPE_CHECKING

__BTN_CTRL = (lv.btnmatrix.CTRL.CLICK_TRIG | lv.btnmatrix.CTRL.NO_REPEAT | lv.btnmatrix.CTRL.POPOVER)

class Keyboard(lv.btnmatrix):
    """
    DO NOT use this class directly, use it's subclasses
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        # a channel for notify caller
        self.channel = loop.chan()
        self.add_event_cb(self.on_event, lv.EVENT.VALUE_CHANGED, None)
        self.add_event_cb(lambda e: self.channel.publish(e.code), lv.EVENT.CANCEL, None)
        self.add_event_cb(lambda e: self.channel.publish(e.code), lv.EVENT.READY, None)
        self._ta = None

    @property
    def textarea(self) -> lv.textarea | None:
        return self._ta

    @textarea.setter
    def textarea(self, ta: lv.textarea | None):
        self._ta = ta

    def set_textarea(self, ta: lv.textarea):
        self.textarea = ta

    # trigger when textarea content changed
    def content_changed(self):
        pass

    def on_event(self, event: lv.event_t):
        target = event.target

        btn_id = target.get_selected_btn()
        # do nothing if not a button
        if btn_id == lv.BTNMATRIX_BTN.NONE:
            return

        txt = target.get_btn_text(btn_id)
        if not txt:
            return
        # click `close` or `keyboard`
        if txt in (lv.SYMBOL.CLOSE, lv.SYMBOL.KEYBOARD):
            if self.textarea:
                lv.event_send(self.textarea, lv.EVENT.CANCEL, None)
            lv.event_send(target, lv.EVENT.CANCEL, None)
            return
        # click `ok`
        if txt == lv.SYMBOL.OK:
            if self.textarea:
                lv.event_send(self.textarea, lv.EVENT.READY, None)
            lv.event_send(target, lv.EVENT.READY, None)
            return

        # update textarea content if set
        ta = self.textarea
        if not ta:
            return

        motor.vibrate()

        # click `new line`
        if txt in (lv.SYMBOL.NEW_LINE, "Enter"):
            ta.add_char("\n")
            # textarea is one line mode
            if ta.get_one_line():
                lv.event_send(ta, lv.EVENT.READY, None)
        # click `left`
        elif txt == lv.SYMBOL.LEFT:
            ta.cursor_left()
        # click `right`
        elif txt == lv.SYMBOL.RIGHT:
            ta.cursor_right()
        # click `backspace`
        elif txt == lv.SYMBOL.BACKSPACE:
            ta.del_char()
            self.content_changed()
        else:
            ta.add_text(str(txt))
            self.content_changed()


class PinKeyboard(Keyboard):
    """A pin keyboard"""

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.ACCESS_BTN_ID = const(11)
        # btn id 9: backspace or close
        self.DELETE_BTN_ID = const(9)
        self.CLOSE_BTN_ID = const(9)
        self.add_style(Styles.pin_keyboard, lv.PART.MAIN)
        self.add_style(Styles.pin_keyboard_btn, lv.PART.ITEMS)
        self.add_style(Styles.disabled, lv.STATE.DISABLED)
        self.add_style(Styles.pressed, lv.STATE.PRESSED)
        # show length of user have input
        self.tip_count_min: int = 10
        self.min_pin_length: int = MIN_PIN_LENGTH
        self.max_pin_length: int = MAX_PIN_LENGTH

        # a tip label and keyboard
        self.set_size(lv.pct(100), 362)
        self.set_style_pad_top(48, lv.PART.MAIN)
        self.tip = lv.label(self)
        self.tip.set_size(lv.pct(100), 32)
        self.tip.align(lv.ALIGN.TOP_MID, 0, -40)
        self.tip.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)
        self.tip.add_flag(lv.obj.FLAG.HIDDEN)
        self.tip.set_recolor(True)

        """
        1  2  3
        4  5  6
        7  8  9
        x  0  OK
        """
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        if device.is_random_pin_map_enabled():
            random.shuffle(nums)
        nums = [str(i) for i in nums]
        # fmt: off
        self.maps = [
            nums[0], nums[1], nums[2], "\n",
            nums[3], nums[4], nums[5], "\n",
            nums[6], nums[7], nums[8], "\n",
            lv.SYMBOL.CLOSE, nums[9], lv.SYMBOL.OK,
            "",
        ]
        # fmt: on
        self.set_map(self.maps)
        self.set_btn_ctrl_all(__BTN_CTRL)

        self.accessable = False

        self.add_event_cb(self.on_draw, lv.EVENT.DRAW_PART_BEGIN, None)

    # override `content_changed`
    def content_changed(self):
        # no need this test, because only called when `textarea` is set
        # if not self.textarea:
        #     return
        count = len(self.textarea.get_text())
        max_count = self.textarea.get_max_length()
        if self.max_pin_length and max_count:
            max_count = min(self.max_pin_length, max_count)
        elif self.max_pin_length:
            max_count = self.max_pin_length

        # count in [min, max]
        self.accessable = max_count >= count >= (self.min_pin_length or 1)

        symbol = lv.SYMBOL.BACKSPACE if count else lv.SYMBOL.CLOSE
        self.maps[12] = symbol
        self.set_map(self.maps)

        if count < self.tip_count_min:
            self.tip.add_flag(lv.obj.FLAG.HIDDEN)
            return
        if count < max_count:
            g = colors.DS.GREEN.color_to32() & 0xFFFFFF
            r = colors.DS.RED.color_to32() & 0xFFFFFF
            tip = f"#{g:06X} {count}#/#{r:06X} {max_count}#"
        else:
            r = colors.DS.RED.color_to32() & 0xFFFFFF
            tip = f"#{r:06X} {count}#/#{r:06X} {max_count}#"

        self.tip.set_text(tip)
        self.tip.clear_flag(lv.obj.FLAG.HIDDEN)

    @property
    def accessable(self):
        return not self.has_btn_ctrl(self.ACCESS_BTN_ID, lv.btnmatrix.CTRL.DISABLED)

    @accessable.setter
    def accessable(self, value):
        if value:
            self.clear_btn_ctrl(self.ACCESS_BTN_ID, lv.btnmatrix.CTRL.DISABLED)
        else:
            self.set_btn_ctrl(self.ACCESS_BTN_ID, lv.btnmatrix.CTRL.DISABLED)

    def on_draw(self, event):
        dsc = lv.obj_draw_part_dsc_t.__cast__(event.get_param())
        if dsc.id == self.ACCESS_BTN_ID and self.accessable:
            dsc.rect_dsc.bg_color = colors.DS.PLEASURE
        elif dsc.id == self.DELETE_BTN_ID:
            dsc.rect_dsc.bg_color = colors.DS.DANGER

class MnemonicKeyboard(Keyboard):


    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.ACCESS_BTN_ID = const(29)
        self.DELETE_BTN_ID = const(21)
        self.CLOSE_BTN_ID = const(21)

        self.add_style(Styles.mnemonic_keyboard, lv.PART.MAIN)
        self.add_style(Styles.mnemonic_keyboard_btn, lv.PART.ITEMS)
        self.add_style(Styles.pressed, lv.STATE.PRESSED)
        self.add_style(Styles.disabled.bg_color(colors.DS.GRAY), lv.STATE.DISABLED)

        self.set_size(lv.pct(100), 260)
        self.set_style_pad_top(64, lv.PART.MAIN)
        self.tip_container = VStack(self)
        self.tip_container.set_height(64)
        self.tip_container.align(lv.ALIGN.TOP_MID, 0, -64)
        self.tip_container.set_style_pad_column(0, lv.PART.MAIN)
        self.tip_container.clear_flag(lv.obj.FLAG.EVENT_BUBBLE)

        self.add_event_cb(self.on_draw, lv.EVENT.DRAW_PART_BEGIN, None)
        self.add_event_cb(self.on_ready, lv.EVENT.READY, None)

        self.default_state()

    @property
    def accessable(self):
        return not self.has_btn_ctrl(self.ACCESS_BTN_ID, lv.btnmatrix.CTRL.DISABLED)

    @accessable.setter
    def accessable(self, value):
        if value:
            self.clear_btn_ctrl(self.ACCESS_BTN_ID, lv.btnmatrix.CTRL.DISABLED)
        else:
            self.set_btn_ctrl(self.ACCESS_BTN_ID, lv.btnmatrix.CTRL.DISABLED)

    def on_draw(self, event):
        dsc = lv.obj_draw_part_dsc_t.__cast__(event.get_param())
        if dsc.id == self.ACCESS_BTN_ID and self.accessable:
            dsc.rect_dsc.bg_color = colors.DS.PLEASURE
        elif dsc.id == self.DELETE_BTN_ID:
            dsc.rect_dsc.bg_color = colors.DS.DANGER

    def content_changed(self):
        # delete all tips
        self.tip_container.clean()
        txt = self.textarea.get_text()

        # update control symbol
        symbol = lv.SYMBOL.BACKSPACE if txt else lv.SYMBOL.CLOSE
        self.maps[23] = symbol
        self.set_map(self.maps)

        # update buttons state
        mask = bip39.word_completion_mask(txt)
        self.update_btn_state(mask)

        # test have text and update access button state
        if not txt:
            self.accessable = False
            return

        words = bip39.complete_word(txt)
        if words is None:
            # tow many candidates, not show tips
            return

        candidates = words.rstrip().split()

        # if only one candidate or txt in candidates, enable access button
        self.accessable = txt in candidates or len(candidates) == 1

        # show tips
        for candidate in candidates:
            label = lv.label(self.tip_container)
            label.set_text(candidate)
            label.add_style(
                Style()
                .pad_left(8)
                .pad_right(8)
                .border_width(3)
                .border_color(colors.DS.BORDER)
                .border_side(lv.BORDER_SIDE.RIGHT)
                .size(lv.SIZE.CONTENT),
                lv.PART.MAIN
            )
            label.add_flag(lv.obj.FLAG.CLICKABLE)
            label.add_event_cb(self.on_click_candidate, lv.EVENT.CLICKED, None)

        # remove last separator
        label.set_style_border_width(0, lv.PART.MAIN)

    def on_ready(self, event):

        # get ready event from user click `Ok` button or click `candidate` label
        # 1. txt not empty
        # 2. candidate not too many
        # 3. txt in candidates or only one candidate
        txt = self.textarea.get_text()

        words = bip39.complete_word(txt)
        candidates = words.rstrip().split()

        # text of textarea already is mnemonic
        if txt in candidates:
            return
        # only one candidate
        self.textarea.set_text(candidates[0])
        self.content_changed()

    def on_click_candidate(self, event):
        target = event.target
        txt = target.get_text()
        self.textarea.set_text(txt)
        self.content_changed()
        lv.event_send(self, lv.EVENT.READY, None)

    def update_btn_state(self, mask):
        # mask is a 27 bits mask
        # from right to left one bit represent a character a - z
        def have(c):
            return mask & (1 << (ord(c) - 97))

        for i in utils.count():
            c = self.get_btn_text(i)
            if not c:
                break
            if not 'a' <= c <= 'z':
                continue
            if have(c):
                self.clear_btn_ctrl(i, lv.btnmatrix.CTRL.DISABLED)
            else:
                self.set_btn_ctrl(i, lv.btnmatrix.CTRL.DISABLED)

    def default_state(self):
        # keyboard lower characters
        # fmt: off
        self.maps = [
            "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "\n",
            " ","a", "s", "d", "f", "g", "h", "j", "k", "l", " ", "\n",
            lv.SYMBOL.CLOSE, "z", "x", "c", "v", "b", "n", "m", lv.SYMBOL.OK, "",
        ]
        # fmt: on

        # see lvgl/src/extra/widgets/keyboard/lv_keyboard.c
        self.set_map(self.maps)

        # first line 10 characters
        self.ctrls = [__BTN_CTRL] * 10

        # second line 11 characters contains 2 placeholders
        self.ctrls.append(1 | lv.btnmatrix.CTRL.HIDDEN) # placeholder
        self.ctrls.extend([2 | __BTN_CTRL] * 9) # characters
        self.ctrls.append(1 | lv.btnmatrix.CTRL.HIDDEN) # placeholder

        # third line 9 characters contains 3 placeholders
        self.ctrls.append(3 | __BTN_CTRL) # BACKSPACE
        self.ctrls.extend([2 | __BTN_CTRL] * 7) # characters
        self.ctrls.append(3 | __BTN_CTRL) # OK

        self.set_ctrl_map(self.ctrls)

        self.accessable = False
        self.deleteable = False

        self.tip_container.clean()