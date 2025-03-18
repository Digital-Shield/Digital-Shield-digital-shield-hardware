import lvgl as lv

from . import *

from trezor.ui import i18n, Style, colors, font
from trezor.ui.screen import Modal
from trezor.ui.theme import Styles
from trezor.ui.component.container import HStack

from trezor.ui.types import *

if TYPE_CHECKING:

    class SecurityMessage(Protocol):
        header: str | None = None
        tips: List[str] | None = None


class XSecurity(base(Modal)):
    def __init__(self, title, message: SecurityMessage):
        super().__init__()
        # self.set_title(title, "A:/res/app_security.png")
        self.set_title(title)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(Styles.board, lv.PART.MAIN)

        header = lv.label(self.content)
        header.set_long_mode(lv.label.LONG.WRAP)
        header.add_style(
            Style()
            .width(lv.pct(100))
            .bg_color(colors.DS.ORANGE)
            .bg_opa(lv.OPA.COVER)
            .radius(16)
            .pad_all(16)
            .text_line_space(10)
            .text_font(font.Bold.SCS26),
            lv.PART.MAIN,
        )

        header.set_text(message.header)

        for msg in message.tips:
            tip = lv.label(self.content)
            tip.set_long_mode(lv.label.LONG.WRAP)
            tip.add_style(
                Styles.subtitle.width(lv.pct(100))
                .height(lv.SIZE.CONTENT)
                .text_color(colors.DS.WHITE)
                .text_line_space(10)
                .text_align(lv.TEXT_ALIGN.LEFT),
                lv.PART.MAIN,
            )
            tip.set_text(msg)


class PinSecurity(XSecurity):
    title = i18n.Title.pin_security
    message = i18n.PinSecurity

    def __init__(self):
        super().__init__(title=self.title, message=self.message)


class MnemonicSecurity(XSecurity):
    title = i18n.Title.mnemonic_security
    message = i18n.MnemonicSecurity

    def __init__(self):
        super().__init__(title=self.title, message=self.message)
