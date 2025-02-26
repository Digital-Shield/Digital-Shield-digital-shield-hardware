import lvgl as lv

from typing import TYPE_CHECKING

from trezor.ui import i18n, Style, Done
from trezor.ui.screen import with_title_and_buttons
from trezor.ui.types import *

if TYPE_CHECKING:
    from trezor.ui.screen import Navigation, Modal, ButtonsTitledScreen
    from trezor.ui.component import Button

    class TemplatedScreen(ButtonsTitledScreen, Screen):

        def __init__(self):
            self.btn_next: Button
            ...
        def on_click(self, event: lv.event_t):
            ...

item_style = (
    Style()
    .width(lv.pct(100))
    .height(106)
    .radius(16)
    .bg_opa()
    )

def base(S: Type[S]) -> Type[TemplatedScreen]:
    class Template(with_title_and_buttons(S, i18n.Button.next)):
        def __init__(self):
            super().__init__()
            self.content: lv.obj
            self.content.set_style_pad_left(16, lv.PART.MAIN)
            self.content.set_style_pad_right(16, lv.PART.MAIN)
            self.btn_next = self.btn_right
            self.btn_next.add_event_cb(self.on_click_next, lv.EVENT.CLICKED, None)

        def on_click_next(self, event):
            # if is `Modal` screen, we need close it
            from trezor.ui.screen import Modal
            if isinstance(self, Modal):
                self.close(Done())
            else:
                self.channel.publish(Done())
    return Template
