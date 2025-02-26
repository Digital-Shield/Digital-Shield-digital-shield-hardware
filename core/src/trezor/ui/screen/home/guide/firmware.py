import lvgl as lv
from typing import TYPE_CHECKING

from . import *
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
        self.content.add_style(
            Style().pad_left(16).pad_right(16),
            0
        )
        view = self.add(Text)
        view.set_label(i18n.Guide.firmware_title_1)

        view = self.add(Text)
        view.set_label(i18n.Guide.firmware_title_2)

        view = self.add(Text)
        view.set_label(i18n.Guide.firmware_title_3)
        style = (
            Style()
            .pad_right(16)
            .pad_left(16)
            .text_color(lv.color_hex(0xc39700))
        )
        view = self.add(lv.label)
        view.add_style(style,0)
        view.set_text(i18n.Guide.firmware_title_caution)
        view = self.add(lv.label)
        view.add_style(style,0)
        view.set_text(i18n.Guide.firmware_describe_caution)
        
class Text(LabeledItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_style(
            Style()
            .border_width(0)
            .pad_top(0)
            .pad_bottom(0),
            0
        )