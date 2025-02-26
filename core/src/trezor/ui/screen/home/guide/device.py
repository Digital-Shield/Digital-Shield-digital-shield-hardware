import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from trezor.ui.screen import Navigation, with_title

if TYPE_CHECKING:
    from typing import List
    pass

class Device(with_title(Navigation)):
    def __init__(self,title):
        super().__init__()
        self.set_title(title)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style().pad_left(16).pad_right(16),
            0
        )
        Item(self.content,i18n.Guide.device_title_firmware_version,'v1.0.0')
        Item(self.content,i18n.Guide.device_title_serial_number,'888727411212144')

class Item(HStack):
    def __init__(self, parent,title,desc):
        super().__init__(parent)
        self.items_center()
        self.add_style(
            Style()
            .radius(16)
            .bg_opa(lv.OPA.COVER)
            .width(lv.pct(100))
            .height(90)
            .pad_right(32)
            .pad_column(16),
            0,
        )
        self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.set_flex_align(
            lv.FLEX_ALIGN.START,lv.FLEX_ALIGN.START,lv.FLEX_ALIGN.START
        )
        view = self.add(Text)
        view.set_label(title)
        view.set_text(desc)
        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)
    
    def action(self):
        pass

class Text(LabeledText):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_style(
            Style()
            .border_width(0)
            .pad_top(0)
            .pad_bottom(0),
            0
        )