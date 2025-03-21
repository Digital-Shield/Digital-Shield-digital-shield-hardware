import lvgl as lv

from . import Modal
from trezor import utils, workflow
from trezor.ui import i18n, colors, Style
from trezor.ui.component import HStack
from trezor.ui.screen.confirm import Confirm
from trezor.ui.screen.message import Message

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable
    pass

class PowerOff(Confirm):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.power_off)
        self.btn_cancel.set_text(i18n.Button.cancel)
        self.btn_confirm.set_text(i18n.Button.power_off)
        self.btn_confirm.color(colors.DS.DANGER)

    def on_click_confirm(self):
        # no need close self, so we not call super
        screen = ShutingDown()
        workflow.spawn(screen.show())

class Restart(Confirm):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.restart)
        self.btn_confirm.set_text(i18n.Button.restart)
        self.btn_confirm.color(colors.DS.DANGER)

    def on_click_confirm(self):
        # no need close self, so we not call super
        screen = Restarting()
        workflow.spawn(screen.show())

class ShutingDown(Modal):
    def __init__(self):
        super().__init__()

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        self.content.items_center()
        self.content.center()

        self.add(lv.img).set_src("A:/res/logo_two.png")
        self.add(lv.label).set_text(i18n.Text.shutting_down)

        async def shutdown_delay():
            from trezor import loop
            await loop.sleep(1500)
            utils.power_off()

        from trezor import workflow
        workflow.spawn(shutdown_delay())

    async def show(self):
        from trezor.ui.screen import manager
        await manager.replace(self)

class Restarting(Modal):
    def __init__(self):
        super().__init__()

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack

        self.content.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        self.content.items_center()
        self.content.center()

        self.add(lv.img).set_src("A:/res/logo_two.png")
        self.add(lv.label).set_text(i18n.Text.restarting)


        async def restart_delay():
            from trezor import loop
            await loop.sleep(1500)
            utils.reset()

        from trezor import workflow
        workflow.spawn(restart_delay())

    async def show(self):
        from trezor.ui.screen import manager
        await manager.replace(self)



class LowPower(Message):
    on_confirm: Callable[[], None]|None

    def __init__(self, charge):
        msg = i18n.Text.low_power_message.format(charge)
        super().__init__(i18n.Title.low_power, msg)
        self.on_confirm = None

    def update_charge(self, charge: int):
        msg = i18n.Text.low_power_message.format(charge)
        self.text.set_text(msg)

    def on_click_ok(self):
        super().on_click_ok()
        if self.on_confirm:
            self.on_confirm()
