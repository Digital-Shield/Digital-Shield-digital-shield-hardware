import lvgl as lv

from trezor.ui import Style
from trezor.ui.types import *

item_style = (
    Style()
    .width(lv.pct(100))
    .bg_color(lv.color_hex(0x111126))
    .bg_opa(lv.OPA._90)
    .border_width(0)
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
            #获取i18n.Button.next当前语言内容，重新赋值
            self.btn_right.set_text(i18n.Button.next)
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
