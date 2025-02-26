import lvgl as lv

from trezor import log
from storage import device
from trezor.ui import i18n, Style, theme, colors
from trezor.ui.component import HStack, VStack
from trezor.ui.screen import Navigation, with_title

class SecurityApp(with_title(Navigation)):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.App.security)
        self.create_content(HStack)
        self.content: HStack

        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)

        # change pin
        from .pin import ChangePin
        ChangePin(self.content)

        # backup mnemonic
        if device.needs_backup():
            from .mnemonic import BackupMnemonic
            BackupMnemonic(self.content)

        # check mnemonic
        from .mnemonic import CheckMnemonic
        CheckMnemonic(self.content)

        # wipe device
        from .wipe import WipeDevice
        WipeDevice(self.content)


class Item(VStack):
    """
    Item with an icon and text
    """

    def __init__(self, parent, text, icon):
        super().__init__(parent)
        self.items_center()
        self.add_style(
            Style()
            .radius(16)
            .bg_opa(lv.OPA.COVER)
            .width(lv.pct(100))
            .height(72)
            .pad_right(32)
            .pad_column(16),
            0,
        )
        self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        self.icon = lv.img(self)
        self.icon.set_src(icon)

        self.label = lv.label(self)
        self.label.set_flex_grow(1)
        self.label.set_text(text)


class SampleItem(Item):
    def __init__(self, parent, text, icon):
        super().__init__(parent, text, icon)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)

    def action(self):
        pass
