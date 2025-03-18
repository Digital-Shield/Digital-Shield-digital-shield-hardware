import lvgl as lv

from . import *

from trezor import log, utils, workflow
from trezor.ui import i18n, Style, colors, font
from trezor.ui.screen import Modal
from trezor.ui.theme import Styles
from trezor.ui.component.container import VStack, HStack

# LanguageScreen is first screen when device is not initialized
# It not allow to go back
class LanguageScreen(base(Modal)):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.select_language, "A:/res/language.png")

        # content
        self.create_content(HStack)
        self.content: HStack

        # languages item
        langs = [
            {"title" : "English", "icon" : "A:/res/lang-en_UK.png"},
            {"title" : "简体中文", "icon" : "A:/res/lang-zh_CN.png"},
            {"title" : "繁體中文", "icon" : "A:/res/lang-zh_CN.png"},
            {"title" : "한국어", "icon" : "A:/res/lang-zh_CN.png"},
            {"title" : "日本語", "icon" : "A:/res/lang-zh_CN.png"},
            # {"title" : "بالعربية", "icon" : "A:/res/lang-zh_CN.png"},
            {"title" : "Tiếng Việt", "icon" : "A:/res/lang-zh_CN.png"},
        ]

        self.languages = [Item(parent=self.content, **lang) for lang in langs]
        utils.first(self.languages).checked = True

        self.content.add_event_cb(self.on_click_languages, lv.EVENT.CLICKED, None)

    def on_click_languages(self, event: lv.event_t):
        target = event.target
        selected = utils.first(enumerate(self.languages), lambda c: c[1] == target)
        if not selected:
            return

        (idx, obj) = selected
        obj.checked = True
        global language
        language = i18n.languages[idx]
        i18n.change_language(language)
        self.update_ui()

        for l in filter(lambda target: target != obj, self.languages):
            l.checked = False

    def update_ui(self):
        self.title.set_text(i18n.Title.select_language)
        self.btn_next.set_text(i18n.Button.next)

    # override `on_click_next`
    def on_click_next(self, event):
        from .quickstart import Quickstart
        workflow.spawn(Quickstart().show())

    async def show(self):
        from trezor.ui.screen import manager
        await manager.switch_scene(self)

class Item(VStack):
    def __init__(self, parent, title, icon):
        super().__init__(parent)
        self.items_center()
        self.add_style(item_style, 0)
        self.add_flag(lv.obj.FLAG.CLICKABLE)

        # icon
        self.icon = lv.img(self)
        self.icon.set_src(icon)

        # name
        self.title = lv.label(self)
        self.title.add_style(Styles.title_text, lv.PART.MAIN)
        self.title.set_text(title)
        self.title.set_flex_grow(1)

        # state
        self.state = lv.label(self)
        self.state.set_text("")
        self.state.set_size(32, 32)
        # normal state
        self.state.add_style(
            Style()
            .radius(lv.RADIUS.CIRCLE)
            .bg_color(colors.DS.WHITE)
            .border_color(colors.DS.BORDER)
            .border_width(1),
            lv.STATE.DEFAULT
        )
        # checked state
        self.state.add_style(
            Style()
            .text_color(colors.DS.WHITE)
            .text_align_center()
            .text_font(font.small)
            .radius(lv.RADIUS.CIRCLE)
            .bg_color(colors.DS.PRIMARY)
            .bg_opa(lv.OPA.COVER)
            .border_width(0),
            lv.PART.MAIN | lv.STATE.CHECKED
        )

    @property
    def checked(self):
        return self.state.has_state(lv.STATE.CHECKED)

    @checked.setter
    def checked(self, checked: bool):
        if checked:
            self.state.add_state(lv.STATE.CHECKED)
            self.state.set_text(lv.SYMBOL.OK)
        else:
            self.state.clear_state(lv.STATE.CHECKED)
            self.state.set_text("")
