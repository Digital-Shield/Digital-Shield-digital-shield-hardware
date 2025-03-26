import lvgl as lv

from . import Modal
from trezor.ui import i18n, colors, Done
from trezor.ui.component import HStack

class EthSignature(Modal):
    def __init__(self, sig: str):
        super().__init__()
        self.set_title(i18n.Title.signature)
        self.btn_right.set_text(i18n.Button.ok)

        self.create_content(HStack)
        self.content: HStack
        self.content.items_center()
        self.content.set_style_pad_top(32, lv.PART.MAIN)
        self.content.set_style_pad_row(32, lv.PART.MAIN)

        # tips
        note = self.add(lv.label)
        note.set_text(i18n.Text.use_app_scan_this_signature)

        # signature qrcode
        view = lv.qrcode(self.content, 400, colors.DS.BLACK, colors.DS.WHITE)
        view.set_style_border_width(16, lv.PART.MAIN)
        view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
        view.update(sig, len(sig))
        view.set_style_border_width(16, lv.PART.MAIN)

        self.btn_right.add_event_cb(lambda _: self.on_click_ok(), lv.EVENT.CLICKED, None)

    def on_click_ok(self):
        self.close(Done())

