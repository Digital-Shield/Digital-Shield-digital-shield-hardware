import lvgl as lv

from . import *
from trezor import utils, log
from trezor.ui import i18n, Style, colors, Redo, font
from trezor.ui.screen import Modal, Navigation, with_title_and_buttons
from trezor.ui.theme import Styles
from trezor.ui.component import HStack, VStack, Title
from trezor.ui.component import MnemonicKeyboard

from trezor.ui.types import *

class MnemonicDisplay(with_title_and_buttons(Modal, i18n.Button.next, i18n.Button.redo)):

    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.backup_mnemonic, "A:/res/app_security.png")

        self.create_content(VStack)
        self.content: VStack
        self.content.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.content.set_style_pad_left(12, lv.PART.MAIN)
        self.content.set_style_pad_row(16, lv.PART.MAIN)

        self.btn_next = self.btn_right
        self.btn_redo = self.btn_left
        self.btn_redo.bg_opa(lv.OPA.TRANSP)
        self.btn_redo.text_color(colors.DS.PRIMARY)

        self.btn_redo.add_event_cb(
            lambda e: self.channel.publish(Redo()), lv.EVENT.CLICKED, None
        )
        self.btn_next.add_event_cb(
            lambda e: self.channel.publish(Done()), lv.EVENT.CLICKED, None
        )

        self.items: List[Item] = []

    def update_mnemonics(self, mnemonics: Sequence[str]):
        log.debug(__name__, f"mnemonics: {mnemonics}")

        mnemonics = list(enumerate(mnemonics))

        if self.items:
            for item, (index, word) in zip(self.items, mnemonics):
                item.word = word
                item.index = index
            return

        for index, word in mnemonics:
            item = Item(self.content, word, index)
            item.add_style(
                Style()
                .pad_top(0)
                .pad_bottom(0),
                lv.PART.MAIN,
            )
            self.items.append(item)

class MnemonicCheck(base(Navigation)):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.check_mnemonic, "A:/res/app_security.png")

        self.content.set_style_pad_all(0, 0)
        self.create_content(VStack)
        self.content: VStack
        self.content.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.content.set_style_pad_left(12, lv.PART.MAIN)
        self.content.set_style_pad_row(16, lv.PART.MAIN)

        self.content.add_event_cb(self.click_mnemonic, lv.EVENT.CLICKED, None)
        self.btn_next.add_state(lv.STATE.DISABLED)

    def on_click_next(self, event):
        self.channel.publish(self.checked_mnemonic)

    def update_mnemonics(self, mnemonics: Sequence[str]):
        self.items: List[Item] = []
        self.index_iter = self.create_index_iter()

        if self.items:
            for item, word in zip(self.items, mnemonics):
                item.word = word
                item.index = None
                return

        for word in mnemonics:
            item = Item(self.content, word)
            item.add_style(
                Style()
                .pad_top(0)
                .pad_bottom(0),
                lv.PART.MAIN,
            )
            self.items.append(item)

        # mark all items as clickable
        for item in self.items:
            item.clickable = True

    def click_mnemonic(self, event):
        target = event.target
        log.debug(__name__, f"click_mnemonic {target}")
        try:
            # 按用户点击顺序设置单词的index
            item: Item = utils.first(self.items, lambda i: i == target)
            if item is None:
                return
            # 若当前单词未被设置，则设置成下一个index
            if item.index is None:
                index = next(self.index_iter)
                log.debug(__name__, f"set index {index}")
                item.index = index
                item.checked = True
                return

            index = item.index
            log.debug(__name__, f"unset index >= {index}")
            # 若当前单词已经设置index，取消index大于等于当前index的单词
            for i in filter(lambda item: item.index is not None and item.index >= index, self.items):
                i.index = None
                i.checked = False

            self.index_iter = self.create_index_iter(index)
        finally:
            enable = all(item.index is not None for item in self.items)
            if enable:
                self.btn_next.clear_state(lv.STATE.DISABLED)
            else:
                self.btn_next.add_state(lv.STATE.DISABLED)

    @property
    def checked_mnemonic(self) -> list[str]:
        checked = [item for item in self.items if item.index is not None]
        checked.sort(key=lambda item: item.index)
        return [item.word for item in checked]

    def create_index_iter(self, init: int|None = None):
        index = init or 0
        while True:
            yield index
            index += 1

    def on_unloaded(self):
        from trezor.ui.screen import manager
        manager.mark_dismissing(self)

class MnemonicInput(base(Navigation)):
    def __init__(self, count):
        super().__init__()
        self.set_title(i18n.Title.enter_mnemonic, "A:/res/app_security.png")

        self.content.set_style_pad_all(0, 0)
        self.create_content(VStack)
        self.content: VStack
        self.content.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.content.set_style_pad_left(12, lv.PART.MAIN)
        self.content.set_style_pad_row(16, lv.PART.MAIN)
        self.content.add_style( Styles.board, lv.PART.MAIN)

        self.items: List[Item] = []
        for index in range(count):
            item = Item(self.content, index=index)
            item.add_style(
                Style()
                .pad_top(0)
                .pad_bottom(0),
                lv.PART.MAIN,
            )
            self.items.append(item)

        # mark all items as clickable
        for item in self.items:
            item.clickable = True
        self.content.add_event_cb(self.on_click_item, lv.EVENT.CLICKED, None)
        self.btn_next.add_state(lv.STATE.DISABLED)
        self.input = None

    @property
    def mnemonics(self) -> List[str]:
        return [item.word for item in self.items]

    def update_next_btn(self):
        enable = all(item.word is not None for item in self.items)
        if enable:
            self.btn_next.clear_state(lv.STATE.DISABLED)
        else:
            self.btn_next.add_state(lv.STATE.DISABLED)

    def close_input(self):
        log.debug(__name__, "close input")
        if not self.input:
            return

        item = utils.first(self.items, lambda i: i.inputting)
        if item:
            item.inputting = False

        self.input.delete()
        self.input = None

    def popup_input(self, item: 'Item'):
        log.debug(__name__, f"popup input for {item.index}")
        if self.input:
            return

        # reset inputted word
        # item.word = ""

        index = item.index
        self.input = Input(self, index)

        # close input when click close
        self.input.add_event_cb(lambda e: self.close_input(), lv.EVENT.CANCEL, None)
        self.input.add_event_cb(self.on_input_ready, lv.EVENT.READY, None)

    def on_input_ready(self, event):
        log.debug(__name__, "input ready")
        word = self.input.ta.get_text()
        item = utils.first(self.items, lambda i: i.inputting)
        assert item is not None
        item.word = word
        self.update_next_btn()

        # if input is last item, input done, close input
        if item == self.items[-1]:
            self.close_input()
            return

        index = item.index
        index += 1
        item = self.items[index]
        # if next have input, close input, wait user click other
        if item.word:
            self.close_input()
            return

        # input next
        self.input.set_index(index)
        self.input.reset()

        lv.event_send(item, lv.EVENT.CLICKED, None)


    def on_click_item(self, event):
        target: Item = event.target

        if target not in self.items:
            return
        prev = utils.first(self.items, lambda i: i.inputting)
        item = utils.first(self.items, lambda i: i == target)
        log.debug(__name__, f"inputting item {item.index}")
        if prev == item:
            return
        item.inputting = True
        self.popup_input(item)

        # may not inputting
        if prev:
            prev.inputting = False

class Item(HStack):
    #    <index>
    #    <word>

    def __init__(self, parent, word: str | None = None, index: int | None = None):
        super().__init__(parent)
        self._word = word
        self._index = index
        self.add_style(
            Style()
            .radius(16)
            .width(140)
            .height(96)
            .border_width(1)
            .bg_opa(lv.OPA.COVER),
            lv.PART.MAIN,
        )

        self.items_center()

        self.add_style(Styles.checked, lv.PART.MAIN | lv.STATE.CHECKED)
        # we use USER_1 to mark inputting
        # not directly use lv.STATE.FOCUSED, because it will changed when `Input` popup
        self.add_style(Styles.focused, lv.PART.MAIN | lv.STATE.USER_1)

        self.index_label = lv.label(self)
        self.index_label.add_style(
            Style().text_font(font.small).text_color(colors.DS.GRAY), lv.PART.MAIN
        )
        self.index_label.set_text("" if index is None else str(index + 1))

        self.word_label = lv.label(self)
        self.word_label.add_style(Style().text_font(font.small), lv.PART.MAIN)
        self.word_label.set_text(word or "")

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, value):
        self._word = value
        self.word_label.set_text(value)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        self.index_label.set_text("" if value is None else str(value+1))

    @property
    def clickable(self):
        return self.has_flag(lv.obj.FLAG.CLICKABLE)

    @clickable.setter
    def clickable(self, value):
        if value:
            self.add_flag(lv.obj.FLAG.CLICKABLE)
            self.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        else:
            self.clear_flag(lv.obj.FLAG.CLICKABLE)
            self.clear_flag(lv.obj.FLAG.EVENT_BUBBLE)

    @property
    def checked(self):
        return self.has_state(lv.STATE.CHECKED)

    @checked.setter
    def checked(self, value):
        if value:
            self.add_state(lv.STATE.CHECKED)
        else:
            self.clear_state(lv.STATE.CHECKED)

    @property
    def inputting(self):
        return self.has_state(lv.STATE.USER_1)

    @inputting.setter
    def inputting(self, value):
        if value:
            self.add_state(lv.STATE.USER_1)
        else:
            self.clear_state(lv.STATE.USER_1)

    def toggle(self):
        self.checked = not self.checked


class Input(lv.obj):
    def on_click_blank(self, e: lv.event_t):
        if e.get_target() != self:
            return

        lv.event_send(self, lv.EVENT.CANCEL, None)

    def __init__(self, parent, index):
        super().__init__(parent)
        self.add_flag(lv.obj.FLAG.EVENT_BUBBLE)

        self.add_style(
            Style()
            .pad_left(0)
            .pad_right(0)
            .pad_bottom(0)
            .bg_color(colors.DS.GRAY)
            .bg_opa(lv.OPA._40)
            .width(lv.pct(100))
            .height(lv.pct(100)),
            0
        )
        self.set_pos(0, 0)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(self.on_click_blank, lv.EVENT.CLICKED, None)

        self.content = HStack(self)
        self.content.add_style(
            Style()
            .pad_left(0)
            .pad_right(0)
            .pad_bottom(0)
            .pad_top(0)
            .width(lv.pct(100))
            .height(lv.SIZE.CONTENT)
            .bg_color(colors.DS.WHITE)
            .bg_opa(),
            lv.PART.MAIN
        )
        self.content.items_center()
        self.content.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        
        # <index> and `textarea`
        container = VStack(self.content)
        container.add_style(
            Style()
            .width(lv.pct(100))
            .height(80)
            .pad_left(16)
            .pad_right(16)
            .pad_column(16),
            lv.PART.MAIN
        )
        container.set_style_flex_cross_place(lv.FLEX_ALIGN.END, lv.PART.MAIN)

        # a label for index
        self.index = lv.label(container)
        self.index.add_style(Styles.title_text, lv.PART.MAIN)
        self.index.set_text(f"#{index + 1}")
        
        self.ta = lv.textarea(container)
        self.ta.set_one_line(True)
        self.ta.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self.ta.add_style(
            Style()
            .bg_opa(lv.OPA.TRANSP)
            .width(300)
            .height(64)
            .text_font(font.Bold.SCS38)
            .text_align_center()
            .border_width(3)
            .border_color(colors.DS.BLACK)
            .border_side(lv.BORDER_SIDE.BOTTOM),
            lv.PART.MAIN,
        )
        self.ta.set_flex_grow(1)

        self.kbd = MnemonicKeyboard(self.content)
        self.kbd.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.kbd.textarea = self.ta

    def reset(self):
        self.ta.set_text("")
        self.kbd.default_state()

    def set_index(self, index):
        self.index.set_text(f"#{index + 1}")
