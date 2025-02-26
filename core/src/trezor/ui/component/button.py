import lvgl as lv

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
    ButtonMode = Literal["cancel", "reject", "danger"]


class Button(lv.btn):
    def __init__(self, parent):
        super().__init__(parent)

        # set default size
        self.set_size(160, 64)
        self.label: lv.label = None

    def set_text(self, text: str):
        if not self.label:
            self.label = lv.label(self)
            self.center()

        self.label.set_text(text)

    def color(self, c):
        self.set_style_bg_color(c, 0)

    def bg_opa(self, opa):
        self.set_style_bg_opa(opa, 0)

    def text_color(self, c):
        self.label.set_style_text_color(c, 0)

    def mode(self, mode: ButtonMode):
        from trezor.ui.colors import DS
        if mode in ("cancel", "reject"):
            self.color(DS.WHITE)
            self.text_color(DS.DANGER)
        elif mode == "danger":
            self.color(DS.DANGER)
            self.text_color(DS.WHITE)
