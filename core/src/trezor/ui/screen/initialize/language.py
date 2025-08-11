import lvgl as lv

from . import *

from trezor import log, utils, workflow
from trezor.ui import i18n, Style, colors, font
from trezor.ui.screen import Modal
from trezor.ui.theme import Styles
from trezor.ui.component.container import VStack, HStack

# LanguageScreen is first screen when device is not initialized
# It not allow to go back
class LanguageScreen(Modal):
    def __init__(self):
        super().__init__()
        # self.set_title(i18n.Title.select_language, "A:/res/language.png")
        # self.set_title(i18n.Title.select_language)
        # self.title.set_height(40)  # 设置文本高度为 50 像素
        # self.title.set_text(i18n.Title.select_language)
        # self.btn_right.set_text(i18n.Button.next)
        # self.btn_next = self.btn_right
        self.btn_right.delete()
        # self.btn_next.add_event_cb(self.on_click_next, lv.EVENT.CLICKED, None)

        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)# 设置背景颜色
        # content
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .pad_top(0)
            .pad_left(20)
            .pad_right(20),
            0
        )
        #左上角图标
        self.icon = lv.img(self.content)
        self.icon.set_src("A:/res/languages.png")
        self.icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        # 使用绝对定位到左上角
        #设置水平右移20
        # self.icon.align(lv.ALIGN.TOP_LEFT, 20, 0)
        self.icon.set_style_pad_left(20, lv.PART.MAIN)
        self.icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
        self.icon.set_zoom(256)  # 1.0x zoom, ensures full image is shown
        self.icon.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.icon.set_style_clip_corner(False, lv.PART.MAIN)
        self.text1 = lv.label(self.content)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        # self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text("Language")
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_pad_left(20, lv.PART.MAIN)
        self.text1.set_style_pad_bottom(20, lv.PART.MAIN)
        # languages item
        langs = [
            # {"title" : "English", "icon" : "A:/res/lang-en_UK.png"},
            # {"title" : "简体中文", "icon" : "A:/res/lang-zh_CN.png"},
            # {"title" : "繁體中文", "icon" : "A:/res/lang-zh_CN.png"},
            # {"title" : "한국어", "icon" : "A:/res/lang-zh_CN.png"},
            # {"title" : "日本語", "icon" : "A:/res/lang-zh_CN.png"},
            # # {"title" : "بالعربية", "icon" : "A:/res/lang-zh_CN.png"},
            # {"title" : "Tiếng Việt", "icon" : "A:/res/lang-zh_CN.png"},
            # {"title" : "简体中文", "icon" : None},
            {"title" : "繁體中文", "icon" : None},
            {"title" : "English", "icon" : None},
            {"title" : "한국어", "icon" : None},
            {"title" : "日語", "icon" : None},
            {"title" : "بالعربية", "icon" : None},
            {"title" : "Tiếng Việt", "icon" : None},
            {"title" : "Deutsch", "icon" : None},
        ]
        # 容器（重新设计布局）
        self.a_container = lv.obj(self.content)
        self.a_container.set_size(440, lv.SIZE.CONTENT)
        self.a_container.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        #设置背景色
        self.a_container.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.a_container.set_style_pad_left(20, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 20)

         # 选项
        self.options_container = HStack(self.a_container)
        self.options_container.set_size(440, 660)
        self.options_container.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container.set_style_radius(20, lv.PART.MAIN) #圆角16
        self.options_container.set_width(lv.pct(100))
        self.options_container.align(lv.ALIGN.TOP_LEFT, -8, 0)
        self.options_container.set_style_border_width(0, lv.PART.MAIN)
        self.options_container.set_style_pad_left(0, lv.PART.MAIN) #设置左上角显示

        #设置喊行间距0
        self.options_container.set_style_pad_row(0, lv.PART.MAIN)
        self.languages = [Item(parent=self.options_container, **lang) for lang in langs]
        # utils.first(self.languages).checked = True
    
        self.options_container.add_event_cb(self.on_click_languages, lv.EVENT.CLICKED, None)

    def on_click_languages(self, event: lv.event_t):
        target = event.target
        selected = utils.first(enumerate(self.languages), lambda c: c[1] == target)
        if not selected:
            return
        print("on_click_languages")
        (idx, obj) = selected
        # obj.checked = True
        global language
        language = i18n.languages[idx]
        i18n.change_language(language)
        # self.update_ui()

        # for l in filter(lambda target: target != obj, self.languages):
        #     l.checked = False
        from .quickstart import Quickstart
        workflow.spawn(Quickstart().show())

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
        item_style = (
            Style()
            .width(400)
            .bg_color(lv.color_hex(0x0D0E17))
            .text_font(font.Mono.JB28)
            .bg_opa(lv.OPA._100)
            .border_width(0)
            .height(90)
            .radius(16)
            .pad_left(0)
            .pad_right(0)
            .pad_bottom(0)
            .bg_opa()
            #显示框颜色为灰色
            # .border_color(lv.color_hex(0x888888))
            # .border_width(1)
         )
        self.add_style(item_style, 0)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        # 添加底边灰色边框
        self.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        self.set_style_border_width(2, lv.PART.MAIN)
        self.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
        self.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)

        # icon
        self.icon = lv.img(self)
        self.icon.set_src(icon)

        # name
        self.title = lv.label(self)
        self.title.add_style(Styles.language_title_text, lv.PART.MAIN)
        self.title.set_text(title)
        # #左边距设置20
        # self.title.set_style_pad_left(20, lv.PART.MAIN)
        self.title.set_flex_grow(1)

        # arrow
        self.arrow = lv.img(self)
        # self.arrow.set_text(lv.SYMBOL.RIGHT)
        # self.arrow.set_width(21)
        # self.arrow.set_height(32)
        # self.arrow.set_style_pad_right(30, lv.PART.MAIN)
        #设置背景图
        self.arrow.set_src("A:/res/right_arw.png")
        # # state
        # self.state = lv.label(self)
        # self.state.set_text("")
        # self.state.set_size(32, 32)
        # # normal state
        # self.state.add_style(
        #     Style()
        #     .radius(lv.RADIUS.CIRCLE)
        #     .bg_color(lv.color_hex(0x0D0D17))
        #     .border_color(colors.DS.WHITE)
        #     .border_width(1),
        #     lv.STATE.DEFAULT
        # )
        # # checked state
        # self.state.add_style(
        #     Style()
        #     .text_color(colors.DS.BLACK)
        #     .bg_color(colors.DS.WHITE)
        #     .text_align_center()
        #     .text_font(font.small)
        #     .radius(lv.RADIUS.CIRCLE)
        #     .bg_opa(lv.OPA.COVER)
        #     .border_width(0),
        #     lv.PART.MAIN | lv.STATE.CHECKED
        # )

    # @property
    # def checked(self):
    #     return self.state.has_state(lv.STATE.CHECKED)

    # @checked.setter
    # def checked(self, checked: bool):
    #     if checked:
    #         self.state.add_state(lv.STATE.CHECKED)
    #         self.state.set_text(lv.SYMBOL.OK)
    #         self.state.set_style_text_color(lv.color_hex(0x0D0D17), 0)
    #     else:
    #         self.state.clear_state(lv.STATE.CHECKED)
    #         self.state.set_text("")
