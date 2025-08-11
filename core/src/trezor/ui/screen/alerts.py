import lvgl as lv

from . import Modal,Navigation
from trezor.ui import i18n, colors, font, Done, Cancel
from trezor.ui.theme import Styles
from trezor.ui.screen.confirm import Confirm
from trezor.ui.screen.message import Message
from trezor.ui.component.container import HStack

class Alerts(Modal):
    """
    A Popup screen with a log and a message, will auto close after a timeout


    User not need do anything, it just show some message. e.g. "Unlocking..." "Wiping ..."
    """
    def __init__(self, title: str, message: str, icon: str|None=None,left_btn_hidden=True) -> None:
        super().__init__()
        self.set_title("")
        self.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        # 隐藏原有的btn_right按钮
        # self.btn_left.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_left.set_text(i18n.Button.cancel)
        self.btn_left.set_style_width(214, lv.PART.MAIN)
        self.btn_left.set_style_height(89, lv.PART.MAIN)
        self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.set_text(i18n.Button.continue_)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.set_style_width(214, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        #判断self.btn_left是否隐藏
        if left_btn_hidden:
            self.btn_right.set_style_width(440, lv.PART.MAIN)
            self.btn_right.set_style_height(89, lv.PART.MAIN)
        #先清除原有的icon
        # self.icon.set_src(None)
        if icon:
            self.icon = self.add(lv.img)
            self.icon.set_src(icon)
            self.icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
            # 使用绝对定位到左上角
            # self.icon.align(lv.ALIGN.TOP_LEFT, 10, 0)
            self.icon.set_style_pad_left(40, lv.PART.MAIN)
            self.icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
            self.icon.set_zoom(256)  # 1.0x zoom, ensures full image is shown
            self.icon.clear_flag(lv.obj.FLAG.CLICKABLE)
            self.icon.set_style_clip_corner(False, lv.PART.MAIN)
        
         # 容器（重新设计布局）
        self.a_container = lv.obj(self)
        self.a_container.set_size(436, 500)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.set_style_pad_left(40, lv.PART.MAIN)
        if icon:
            self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 170)
        else:
            self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 30)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(title)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        #字号40
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        # self.text1.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        # self.text1.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        # self.text.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(lv.pct(90))
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(message)
        #设置行间距10
        self.text2.set_style_text_line_space(10, 0)
        self.text2.set_style_text_font(font.Bold.SCS30, lv.PART.MAIN)
        self.text2.set_style_text_color(colors.DS.WHITE, 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 90)

        # self.text.set_text("")
        # view = self.add(Text)
        # view.set_label(title)
        # view.set_text(desc)
        self.btn_right.add_event_cb(
            lambda _: self.on_click_confirm(), lv.EVENT.CLICKED, None
        )
        self.btn_left.add_event_cb(
            lambda _: self.on_click_cancel(), lv.EVENT.CLICKED, None
        )
        # 新建一个底部居中的按钮
        # self.btn_bottom = self.add(lv.btn)
        # self.btn_bottom.set_width(200)
        # self.btn_bottom.set_height(60)
        # self.btn_bottom.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        # self.btn_bottom.set_style_radius(30, lv.PART.MAIN)
        # self.btn_bottom.set_style_bg_color(colors.DS.PRIMARY, lv.PART.MAIN)
        # self.btn_bottom_label = lv.label(self.btn_bottom)
        # self.btn_bottom_label.set_text(i18n.Button.continue_)
        # self.btn_bottom_label.center()
        # self.btn_bottom.add_event_cb(
        #     lambda _: self.on_click_confirm(), lv.EVENT.CLICKED, None
        # )
    #点击确认
    def on_click_confirm(self):
        print("on_click_confirm")
        self.close(Done())
    # #点完成则返回
    def on_click_cancel(self):
        # self.close(Cancel())
        from trezor.ui import NavigationBack
        self.channel.publish(NavigationBack())
        # from . import manager
        # from trezor import workflow
        # workflow.spawn(manager.pop(self))

    # class Text(LabeledText):
    # def __init__(self, parent):
    #     super().__init__(parent)
    #     self.add_style(
    #         Style()
    #         .border_width(0)
    #         .pad_top(0)
    #         .pad_bottom(0),
    #         0
    #     )

