import lvgl as lv

from trezor import utils, log
from trezor.ui import Style, colors, i18n, theme
from trezor.ui.screen import Navigation, with_title
from trezor.ui.component import HStack, VStack

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar, Sequence, List
    T = TypeVar["T"]

class Item(VStack):
    def __init__(self, parent, text):
        super().__init__(parent)

        # the `option` value
        self.option :T = None

        self.add_style(
            Style()
            .bg_opa(lv.OPA.COVER)
            .width(lv.pct(100))
            .height(72)
            .pad_right(32)
            .pad_column(16)
            .border_width(1)
            .border_side(lv.BORDER_SIDE.BOTTOM),
            0,
        )
        self.items_center()
        # option
        self.label = lv.label(self)
        self.label.set_text(text)

        # state
        self.state = lv.label(self)
        self.state.set_text("")
        self.state.set_style_text_align(lv.TEXT_ALIGN.RIGHT, 0)
        self.state.set_style_text_color(colors.DS.PRIMARY, 0)
        self.state.set_flex_grow(1)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(self.__on_event, lv.EVENT.ALL, None)

    def __on_event(self, event):
        code = event.code
        if code == lv.EVENT.FOCUSED:
            self.state.set_text(lv.SYMBOL.OK)
        elif code == lv.EVENT.DEFOCUSED:
            self.state.set_text("")

class OptionDetails(with_title(Navigation)):
    def __init__(self, title, options: Sequence):
        self.subscriber: lv.obj = None

        super().__init__()
        self.set_title(title)

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .radius(16)
            .pad_all(16)
            .height(lv.SIZE.CONTENT)
            .bg_opa(lv.OPA.COVER),
            lv.PART.MAIN
        )

        self.options = [Item(self.content, self.option_format(o)) for o in options]
        for item, o in zip(self.options, options):
            # add time to item as a property
            item.option = o

        self.group = lv.group_create()
        for item in self.options:
            self.group.add_obj(item)

        # find the current and set focus
        current = self.current()
        item = utils.first(self.options, lambda item: item.option == current)
        lv.group_focus_obj(item)

        self.group.set_focus_cb(self.on_group_focus_changed)


    @classmethod
    def option_format(cls, v: T) -> str:
        """ format options """
        raise NotImplementedError

    @classmethod
    def current(cls) -> T:
        """the default one"""
        raise NotImplementedError

    def save_option(self, option: T):
        raise NotImplementedError

    def on_deleting(self):
        super().on_deleting()
        self.group._del()

    def on_group_focus_changed(self, group: lv._group_t):
        obj = group.get_focused()
        item = utils.first(self.options, lambda item: obj == item)
        log.debug(__name__, f"user clicked: {self.option_format(item.option)}")
        self.save_option(item.option)

        from . import __OPTION_VALUE_CHANGED
        if self.subscriber:
            lv.event_send(self.subscriber, __OPTION_VALUE_CHANGED, None)

def _time_format(t: int) -> str:
    if t < 0:
        return i18n.Text.never
    elif t < 60:
        return f"{t} {i18n.Text.seconds}"
    elif t == 60:
        return f"{t // 60} {i18n.Text.minute}"
    else:
        return f"{t // 60} {i18n.Text.minutes}"

class TimeOptionDetails(OptionDetails):
    def __init__(self, title, times: List[int]):
        super().__init__(title, times)

    @classmethod
    def option_format(cls, v: int):
        return _time_format(v)
