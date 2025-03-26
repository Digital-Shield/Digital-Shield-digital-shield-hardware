import lvgl as lv

from trezor.ui.theme import Styles
from trezor.ui.component.container import VStack
class Title(VStack):
    """
        Title with optional subtitle and icon
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.set_size(lv.pct(100), lv.SIZE.CONTENT)
        self.items_center()

        self.icon = None

        self.text = self.add(lv.label)
        self.text.add_style(Styles.title_text, lv.PART.MAIN)
        self.text.set_text("")

    def set(self, text: str, icon: str|None):
        self.set_text(text)
        if icon:
            self.set_icon(icon)

    def set_text(self, text: str):
        self.text.set_text(text)

    def set_icon(self, icon: str):
        if not self.icon:
            self.icon = lv.img(self)
            self.icon.move_to_index(0)
        self.icon.set_src(icon)


class Subtitle(lv.label):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_style(Styles.subtitle, lv.PART.MAIN)
        self.set_text("")

    def set_text(self, text: str):
        self.set_text(text)
