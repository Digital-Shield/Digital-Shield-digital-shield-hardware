import lvgl as lv

from . import Modal
from trezor.ui import i18n
from trezor.ui.theme import Styles
from trezor.ui.component.container import HStack

class Popup(Modal):
    """
    A Popup screen with a log and a message, will auto close after a timeout


    User not need do anything, it just show some message. e.g. "Unlocking..." "Wiping ..."
    """
    def __init__(self, operating: str, icon: str|None=None):
        super().__init__()

        self.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.add_style(Styles.popup_board, lv.PART.MAIN)

        self.content.items_center()
        self.content.center()

        self.add(lv.img).set_src(icon or "A:/res/logo_two.png")

        self.text = self.add(lv.label)
        self.text.add_style(Styles.popup, lv.PART.MAIN)
        self.text.set_long_mode(lv.label.LONG.WRAP)
        self.text.set_text(operating)
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            self.text.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置显示方向从右向左
        self.text_color(lv.color_hex(0xFFFFFF))  
        # auto close after 1.5 seconds
        self.auto_close_timeout = 2500

    def text_color(self, color):
        self.text.set_style_text_color(color, 0)

