import lvgl as lv

from trezor.ui.types import *

class HStack(lv.obj):
    """HStack container layout it's children in horizontal direction
    item0
    item1
    ...
    itemN
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.remove_style_all()
        # Horizontal layout
        self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        # as a container, we don't process events
        self.add_flag(lv.obj.FLAG.EVENT_BUBBLE)

        style = lv.style_t()
        style.init()

        # fill parent content area
        style.set_width(lv.pct(100))
        style.set_height(lv.pct(100))
        # no border
        style.set_border_width(0)
        # as a container, not a visible object
        style.set_bg_opa(lv.OPA.TRANSP)
        # padding top and bottom 8
        style.set_pad_top(8)
        style.set_pad_bottom(8)
        # padding row 16
        style.set_pad_row(16)

        self.add_style(style, lv.PART.MAIN)

    def reverse(self):
        self.set_flex_flow(lv.FLEX_FLOW.COLUMN_REVERSE)

    def items_center(self):
        self.set_flex_align(
            lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER
        )

    def add(self, cls: Type[Widget]) -> Widget:
        return cls(self)

class VStack(lv.obj):
    """
    VStack container layout it's children in vertical direction
    item0 item1 ... itemN
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.remove_style_all()
        # Vertical layout
        self.set_flex_flow(lv.FLEX_FLOW.ROW)
        # as a container, we don't process events
        self.add_flag(lv.obj.FLAG.EVENT_BUBBLE)

        style = lv.style_t()
        style.init()

        # fill parent content area
        style.set_width(lv.pct(100))
        style.set_height(lv.pct(100))
        # no border
        style.set_border_width(0)
        # as a container, not a visible object
        style.set_bg_opa(lv.OPA.TRANSP)
        # padding left and right 8
        style.set_pad_left(8)
        style.set_pad_right(8)
        # pad column 16
        style.set_pad_column(16)

        self.add_style(style, lv.PART.MAIN)

    def reverse(self):
        self.set_flex_flow(lv.FLEX_FLOW.ROW_REVERSE)

    def items_center(self):
        self.set_flex_align(
            lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER
        )

    def add(self, cls: Type[Widget]) -> Widget:
        return cls(self)
