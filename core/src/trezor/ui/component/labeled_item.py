import lvgl as lv

from . import HStack
from trezor.ui import Style, colors

from trezor.ui.types import *

# can't use typing.Generic here, so T can't be infer
# class LabeledItem(HStack, Generic[T]) or class LabeledItem[T](HStack) after Python 3.12
class LabeledItem(HStack):
    style = (
        Style()
        .radius(16)
        .pad_all(16)
        .border_side(lv.BORDER_SIDE.BOTTOM)
        .border_width(1)
        .border_color(colors.DS.GRAY)
        .border_opa(lv.OPA._60)
    )

    def __init__(self, parent):
        super().__init__(parent)
        self.set_height(lv.SIZE.CONTENT)
        self.add_style(self.style, lv.PART.MAIN)

        self.label = self.add(lv.label)
        self.label.set_text("")
        self.label.set_style_text_color(colors.DS.GRAY, lv.PART.MAIN)

    def set_label(self, text: str):
        self.label.set_text(text)

    def add_item(self, cls: Type[Widget]) -> Widget:
        self.item = cls(self)
        return self.item


class LabeledText(LabeledItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_item(lv.label)

        # manually annotate self.item's type
        self.item: lv.label

        self.item.set_width(lv.pct(100))
        self.item.set_long_mode(lv.label.LONG.WRAP)

    def set_text(self, text: str):
        self.item.set_text(text)
