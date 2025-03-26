from . import *
from typing import TYPE_CHECKING

from trezor import workflow, utils
from trezor.ui import i18n, Cancel
from trezor.ui.screen.confirm import SimpleConfirm
from trezor.ui.screen.power import Restarting
from trezor.ui.screen import Modal
from storage import device
from .options import OptionDetails

if TYPE_CHECKING:
    from typing import List
    pass

class Language(OptionsItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.language, "A:/res/language-setting-two.png")

    def current(self):
        return i18n.using.name

    def show_options(self):
        screen = LanguageDetails(i18n.Setting.language, i18n.languages)
        screen.subscriber = self

        workflow.spawn(screen.show())

class LanguageDetails(OptionDetails):
    def __init__(self, title, languages: List[i18n.Language]):
        super().__init__(title, languages)
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色
        self.reverting = False

    @classmethod
    def current(cls):
        return i18n.using

    @classmethod
    def option_format(cls, lang: i18n.Language):
        return lang.name

    def save_option(self, option: i18n.Language):
        if self.reverting:
            self.reverting = False
            return
        workflow.spawn(self.do_confirm_save_option(option))

    def on_loaded(self):
        super().on_loaded()

        # focus on current again
        # maybe user click cancel on confirm
        # revert to current
        current = self.current()
        item = utils.first(self.options, lambda item: item.option == current)
        obj = self.group.get_focused()
        if obj != item:
            # this function will trigger save_option
            lv.group_focus_obj(item)

    async def do_confirm_save_option(self, option: i18n.Language):
        screen = SimpleConfirm(i18n.Text.changing_language)
        screen.btn_confirm.set_text(i18n.Button.continue_)
        screen.btn_confirm.color(colors.DS.DANGER)
        await screen.show()
        r = await screen
        if isinstance(r, Cancel):
            self.reverting = True
            return

        # `Continue`
        i18n.change_language(option)
        device.set_language(option.code)
        await RestartApp().show()

class RestartApp(Modal):
    def __init__(self):
        super().__init__()

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack

        self.content.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        self.content.items_center()
        self.content.center()

        self.add(lv.img).set_src("A:/res/logo_two.png")
        # self.add(lv.label).set_text(i18n.Text.restarting)
        # 添加文本并设置颜色
        label = self.add(lv.label)
        label.set_text(i18n.Text.restarting)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN) 
        # self.add(lv.label).set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


        async def restart_delay():
            from trezor import loop
            await loop.sleep(1500)
            utils.restart_app()

        from trezor import workflow
        workflow.spawn(restart_delay())

    async def show(self):
        from trezor.ui.screen import manager
        await manager.replace(self)

