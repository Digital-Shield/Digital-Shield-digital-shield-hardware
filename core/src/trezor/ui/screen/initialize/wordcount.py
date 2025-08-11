import lvgl as lv

from . import *

from trezor.ui import i18n, Style, colors,font
from trezor.ui.screen import Navigation
from trezor.ui.theme import Styles
from trezor.ui.component.container import HStack
from trezor.ui.screen.navaigate import Navigate

counts = [12, 18, 24]

class WordcountScreen(Navigate):
    def __init__(self, dry_run: bool = False, label: str = ""):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        # self.set_title(i18n.Title.select_word_count, "A:/res/app_security.png")
        # self.set_title(i18n.Title.select_word_count)
         # 容器（重新设计布局）
        self.a_container = lv.obj(self)
        self.a_container.set_size(450, lv.SIZE.CONTENT)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_pad_left(30, lv.PART.MAIN)  # 设置左边距为40
        self.a_container.set_style_pad_right(20, lv.PART.MAIN)  # 设置右边距为40
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 30)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(400)
        self.text1.set_height(66)
        if label=="create":
            title_desc = i18n.Title.prepare_create
        elif dry_run:
            title_desc = i18n.Title.prepare_check
        else:
            title_desc = i18n.Title.prepare_import
        self.text1.set_text(title_desc)
        self.text1.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        # self.text1.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        
        self.text2 = lv.label(self.a_container)
        self.text2.set_style_pad_top(8, lv.PART.MAIN)  # 设置上边距为8
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(123)
        self.text2.set_text(i18n.Text.select_word_count)
        #设置行间距10
        self.text2.set_style_text_line_space(10, lv.PART.MAIN)
        self.text2.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)
        self.text2.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 80)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .pad_top(220)
            .width(460)
            .pad_left(20)
            .pad_right(20),
            0
        )
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
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 150)

         # 选项
        self.options_container = HStack(self.a_container)
        self.options_container.set_size(440, 300)
        self.options_container.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container.set_style_radius(20, lv.PART.MAIN)#圆角20
        self.options_container.set_width(lv.pct(100))
        self.options_container.align(lv.ALIGN.TOP_LEFT, -8, 0)
        self.options_container.set_style_border_width(0, lv.PART.MAIN)
        self.options_container.set_style_pad_left(0, lv.PART.MAIN)#设置左上角显示

        #设置喊行间距0
        self.options_container.set_style_pad_row(0, lv.PART.MAIN)
        
        self.counts = [self.create_count_item(count) for count in counts]

    def create_count_item(self, count):
        # a container
        obj = lv.obj(self.options_container)
        obj.set_size(400, 89)
        obj.add_style(item_style, 0)
        obj.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        obj.set_style_pad_left(20, lv.PART.MAIN)
        # if count != 24:
        #     # 添加底边灰色边框
        #     obj.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        #     obj.set_style_border_width(1, lv.PART.MAIN)
        #     obj.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
        #     obj.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)
        obj.add_event_cb(lambda e: self.channel.publish(count), lv.EVENT.CLICKED, None)

        label = lv.label(obj)
        label.set_recolor(True)
        label.add_style(Styles.title_text, 0)
        label.set_text(i18n.Text.str_words.format(count))
        #上边距20
        label.set_style_pad_top(10, lv.PART.MAIN)
        #字号28
        label.set_style_text_font(font.Bold.SCS30, lv.PART.MAIN)
        #获取当前语言,如果是阿拉伯语则从右到左显示
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            label.set_style_base_dir(lv.BASE_DIR.RTL, 0)
        # label.center()
        self.arrow = lv.img(obj)
        # self.arrow.set_width(21)
        # self.arrow.set_height(32)
        self.arrow.set_style_pad_top(10, lv.PART.MAIN)
        self.arrow.set_style_pad_left(350, lv.PART.MAIN)
        #设置背景图
        self.arrow.set_src("A:/res/right_arw.png")

        return obj
