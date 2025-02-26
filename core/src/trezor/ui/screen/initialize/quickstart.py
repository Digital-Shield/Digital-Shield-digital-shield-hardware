import lvgl as lv

from . import *

from trezor.ui import i18n, Style
from trezor.ui.screen import Navigation
from trezor.ui.theme import Styles
from trezor.ui.component.container import VStack, HStack


class Quickstart(base(Navigation)):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.create_wallet, "A:/res/create-wallet.png")

        # no need next button
        self.btn_next.add_flag(lv.obj.FLAG.HIDDEN)

        self.create_content(HStack)
        self.content: HStack

        # create new wallet
        create = Item(
            self.content, i18n.Title.create_wallet, "A:/res/create-new-wallet.png"
        )
        create.add_event_cb(self.on_create_new_wallet, lv.EVENT.CLICKED, None)

        # restore new wallet
        restore = Item(
            self.content, i18n.Title.restore_wallet, "A:/res/restore-wallet.png"
        )
        restore.add_event_cb(self.on_restore_wallet, lv.EVENT.CLICKED, None)

    def on_create_new_wallet(self, event: lv.event_t):
        from trezor import workflow
        from trezor.wire import DUMMY_CONTEXT
        from apps.management.reset_device import reset_device
        from trezor.messages import ResetDevice

        workflow.spawn(
            reset_device(
                DUMMY_CONTEXT,
                ResetDevice(
                    strength=128,
                    language=i18n.using.code,
                    pin_protection=True,
                ),
            )
        )

    def on_restore_wallet(self, event: lv.event_t):
        from apps.management.recovery_device import recovery_device
        from trezor.messages import RecoveryDevice
        from trezor import workflow
        from trezor.wire import DUMMY_CONTEXT

        workflow.spawn(
            recovery_device(
                DUMMY_CONTEXT,
                RecoveryDevice(
                    enforce_wordlist=True,
                    language=i18n.using.code,
                    pin_protection=True,
                ),
            )
        )


class Item(VStack):
    def __init__(self, parent, title, icon):
        super().__init__(parent)
        self.items_center()
        self.add_style(item_style, 0)
        self.add_flag(lv.obj.FLAG.CLICKABLE)

        # icon
        self.icon = lv.img(self)
        self.icon.set_src(icon)

        # text
        self.title = lv.label(self)
        self.title.add_style(Styles.title_text, lv.PART.MAIN)
        self.title.set_text(title)
        self.title.set_flex_grow(1)

        # right-arrow
        self.arrow = lv.label(self)
        self.arrow.set_text(lv.SYMBOL.RIGHT)
        self.arrow.add_style(
            Styles.subtitle
            .size(32)
            .text_align_center(),
            0,
        )
