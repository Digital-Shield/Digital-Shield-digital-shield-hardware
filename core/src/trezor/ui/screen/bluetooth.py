import lvgl as lv
from storage import device
from trezor.ui import i18n, font, Done
from trezor.ui.screen import Modal, with_title_and_buttons
from trezor.ui.component import HStack

class BluetoothPairing(with_title_and_buttons(Modal, i18n.Button.ok)):
    def __init__(self, code: str):
        super().__init__()

        self.set_title(i18n.Title.bluetooth_pairing)

        self.create_content(HStack)
        # type annotation
        self.content: HStack

        self.content.set_height(lv.SIZE.CONTENT)
        self.content.set_style_pad_column(32, 0)
        self.content.items_center()
        self.content.center()

        # icon
        img = self.add(lv.img)
        img.set_src("A:/res/bluetooth-pairing-two.png")

        # tips
        label = self.add(lv.label)
        label.set_width(lv.pct(100))
        label.set_text(i18n.Text.bluetooth_pair)
        label.set_style_text_font(font.Bold.SCS26, 0)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        label.set_long_mode(lv.label.LONG.WRAP)

        # code
        label = self.add(lv.label)
        label.set_text(code)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        label.set_style_text_font(font.Bold.SCS48, 0)

        self.btn_right.add_event_cb(lambda _: self.close(Done()), lv.EVENT.CLICKED, None)
