import lvgl as lv

from . import *

from trezor.ui import i18n, Style, font, Confirm, NavigationBack
from trezor.ui.screen import Navigation
from trezor.ui.theme import Styles
from trezor.ui.component.container import VStack, HStack
from trezor.ui.screen.navaigate import Navigate

class Quickstart(Navigate):
    def __init__(self):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        # self.title.set_text(i18n.Title.wallet)
        # self.title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)  # 设置文本颜色为白色
         # 容器（重新设计布局）
        self.a_container = lv.obj(self)
        self.a_container.set_size(460, 800)
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
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(i18n.Title.start_setup)
        self.text1.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        self.text1.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        
        self.text2 = lv.label(self.a_container)
        self.text2.set_style_pad_top(8, lv.PART.MAIN)  # 设置上边距为8
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(i18n.Text.start_setup)
        #设置行间距10
        self.text2.set_style_text_line_space(10, lv.PART.MAIN)
        self.text2.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)
        self.text2.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 60)
        self.text2.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓


        self.create_content(VStack)
        self.content: VStack
        self.content.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.content.set_flex_flow(lv.FLEX_FLOW.COLUMN)  # 设置为列布局，居中对齐
        self.content.set_style_pad_top(460, lv.PART.MAIN)  # 设置左边距为0
        self.content.set_style_pad_left(20, lv.PART.MAIN)  # 设置左边距为0
        self.content.set_style_pad_right(20, lv.PART.MAIN)  # 设置右边距为0
        #在self.content设置一个容器，用于存放两个按钮
        # 选项容器
        self.options_container = HStack(self.a_container)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container.set_style_pad_row(10, lv.PART.MAIN)
        self.options_container.set_style_pad_top(200, lv.PART.MAIN)
        self.options_container.set_style_pad_left(10, lv.PART.MAIN)
        self.options_container.set_width(450)
        # #边框2
        # self.options_container.set_style_border_width(2, lv.PART.MAIN)
        # #边框颜色
        # self.options_container.set_style_border_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        #高度200
        self.options_container.set_height(500)
        #可点击
        self.options_container.add_flag(lv.obj.FLAG.CLICKABLE)
        #设置显示到底部
        self.options_container.set_style_align(lv.ALIGN.BOTTOM_MID, lv.PART.MAIN)

        # create new walletA:/res/create-new-wallet.png
        create = Item(
            self.options_container, i18n.Title.create_wallet, ""
        )
        # # 让整个Item区域都能响应点击事件
        # create.set_width(440)
        # create.set_height(90)
        # create.add_flag(lv.obj.FLAG.CLICKABLE)
        create.add_event_cb(self.on_create_new_wallet, lv.EVENT.CLICKED, None)

        # restore new walletA:/res/restore-wallet.png
        restore = Item(
            self.options_container, i18n.Title.import_wallet, ""
        )
        restore.add_event_cb(self.on_restore_wallet, lv.EVENT.CLICKED, None)

    def on_create_new_wallet(self, event: lv.event_t):
        from trezor import workflow
        from trezor.ui.screen.confirm import WordCheckConfirm
        screen = WordCheckConfirm(i18n.Title.create_wallet,i18n.Text.create_wallet,"",False)
        screen.btn_confirm.set_text(i18n.Button.continue_)
        screen.btn_confirm.add_event_cb(self.on_click_confirm_cteate, lv.EVENT.CLICKED, None)
        workflow.spawn(screen.show())

        
    def on_click_confirm_cteate(self, event: lv.event_t):
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
        from trezor import workflow
        from trezor.ui.screen.confirm import WordCheckConfirm
        screen = WordCheckConfirm(i18n.Title.import_wallet,i18n.Text.import_wallet,"",False)
        screen.btn_confirm.set_text(i18n.Button.continue_)
        screen.btn_confirm.add_event_cb(self.on_click_confirm_restore, lv.EVENT.CLICKED, None)
        workflow.spawn(screen.show())

    def on_click_confirm_restore(self, event: lv.event_t):
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
        self.add_style(
            Style()
            .radius(42)
            .bg_opa(lv.OPA.COVER)
            .width(440)  # 432
            .height(90)
            .pad_top(0)
            # .pad_left(20)
            # .pad_right(20)
            .bg_color(lv.color_hex(0x141419)),
            0,
        )
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        #item点击的时候背景色的色值变成0x0062CE
        self.add_style(
            Style()
            .radius(42)
            .bg_opa(lv.OPA.COVER)
            .width(440)  # 432
            .height(90)
            .bg_color(lv.color_hex(0x0062CE)),
            lv.STATE.PRESSED,
        )
        

        # # icon
        # self.icon = lv.img(self)
        # self.icon.set_src(icon)

        # text
        self.title = lv.label(self)
        self.title.add_style(Styles.title_text, lv.PART.MAIN)
        self.title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.title.set_text(title)
        self.title.set_flex_grow(1)
        #整个item可点击
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        # align item to bottom
        # self.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        # # right-arrow
        # self.arrow = lv.label(self)
        # self.arrow.set_text(lv.SYMBOL.RIGHT)
        # self.arrow.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        # self.arrow.add_style(
        #     Styles.subtitle
        #     .size(32)
        #     .text_align_center(),
        #     0,
        # )
