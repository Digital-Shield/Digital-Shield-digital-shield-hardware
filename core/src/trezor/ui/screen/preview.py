import lvgl as lv

from . import Modal
from trezor import log
from trezor.ui import i18n, Cancel, events, colors, Style, theme
from trezor.ui.component import ArcHolder, HStack, VStack
from trezor.ui.screen import Navigation
from trezor.ui.component import HStack, VStack

class Preview(Modal):
    """
    Confirm screen have 2 buttons: `cancel` and `ok`

    User can wait this screen to get result
    """

    def __init__(self,option=None):
        super().__init__()

        # `cancel` and `confirm` buttons
        if option is None:
            self.btn_cancel = self.btn_left
            self.btn_confirm = self.btn_right
            self.btn_cancel.set_text(i18n.Button.cancel)
            self.btn_confirm.set_text(i18n.Button.confirm)
            self.btn_cancel.add_event_cb(
                lambda _: self.on_click_cancel(), lv.EVENT.CLICKED, None
            )
            self.content
            self.btn_confirm.add_event_cb(
                lambda _: self.on_click_confirm(), lv.EVENT.CLICKED, None
            )

            # 创建一个悬浮的返回按钮容器，并确保其在 bottom_bar 之上
            obj = lv.obj(self)
            obj.set_size(68, 68)
            # 设置边框宽度为0，去除白色竖线
            obj.add_style(Style().bg_opa(lv.OPA.TRANSP).border_width(0), lv.PART.MAIN)
            obj.add_flag(lv.obj.FLAG.CLICKABLE)
            obj.add_flag(lv.obj.FLAG.FLOATING)
            obj.set_style_border_side(lv.BORDER_SIDE.RIGHT, 0)
            obj.align(lv.ALIGN.TOP_LEFT, 0, -20)

            nav = lv.img(obj)
            nav.set_src("A:/res/nav-back.png")
            nav.set_zoom(400)
            nav.add_flag(lv.obj.FLAG.CLICKABLE)
            nav.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
            # 使导航图片与页面 title 水平齐平
            # 假设 title 的 y 坐标为 36（可根据实际 title 的 y 坐标调整）
            nav.align(lv.ALIGN.TOP_LEFT, 0, 0)  # x=0，y=8 让图片与 title 水平齐平

            obj.add_event_cb(self.on_nav_back, lv.EVENT.CLICKED, None)
            self.add_event_cb(self.on_nav_back, events.NAVIGATION_BACK, None)

        else:
            
            # # Create a floating bottom bar for the buttons
            # 创建底部浮动栏，背景图铺满
            self.bottom_bar = lv.obj(self)
            self.bottom_bar.set_size(self.get_width(), self.get_height())
            self.bottom_bar.align(lv.ALIGN.BOTTOM_MID, 0, 0)
            self.bottom_bar.add_flag(lv.obj.FLAG.FLOATING)
            self.bottom_bar.add_style(theme.Styles.board, lv.PART.MAIN)
            self.bottom_bar.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
            self.bottom_bar.set_style_bg_img_src(option, lv.PART.MAIN)
            self.bottom_bar.set_style_border_width(0, lv.PART.MAIN)
            self.bottom_bar.set_style_pad_all(0, lv.PART.MAIN)
            self.bottom_bar.set_style_radius(0, lv.PART.MAIN)
            #设置bottom_bar的边框宽度
            # self.bottom_bar.set_style_border_width(1, lv.PART.MAIN)
            # self.bottom_bar.set_style_border_color(colors.DS.BLUE, lv.PART.MAIN)

            # # 创建一个悬浮的返回按钮容器，并确保其在 bottom_bar 之上
            # obj = lv.obj(self.bottom_bar)
            # obj.set_size(68, 68)
            # # 设置边框宽度为0，去除白色竖线
            # obj.add_style(Style().bg_opa(lv.OPA.TRANSP).border_width(0), lv.PART.MAIN)
            # obj.add_flag(lv.obj.FLAG.CLICKABLE)
            # obj.add_flag(lv.obj.FLAG.FLOATING)
            # obj.set_style_border_side(lv.BORDER_SIDE.RIGHT, 0)
            # obj.align(lv.ALIGN.TOP_LEFT, 8, 50)

            # nav = lv.img(obj)
            # nav.set_src("A:/res/nav-back.png")
            # nav.set_zoom(350)
            # nav.add_flag(lv.obj.FLAG.CLICKABLE)
            # nav.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
            # # 使导航图片与页面 title 水平齐平
            # # 假设 title 的 y 坐标为 36（可根据实际 title 的 y 坐标调整）
            # nav.align(lv.ALIGN.TOP_LEFT, 0, 0)  # x=0，y=8 让图片与 title 水平齐平

            # obj.add_event_cb(self.on_nav_back, lv.EVENT.CLICKED, None)
            # self.add_event_cb(self.on_nav_back, events.NAVIGATION_BACK, None)

            self.btn_left.set_style_width(214, lv.PART.MAIN)
            self.btn_left.set_style_height(89, lv.PART.MAIN)
            self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
            self.btn_right.set_style_width(214, lv.PART.MAIN)
            self.btn_right.set_style_height(89, lv.PART.MAIN)
            self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
            self.btn_cancel = self.btn_left
            self.btn_confirm = self.btn_right
            self.btn_cancel.set_text(i18n.Button.cancel)
            self.btn_confirm.set_text(i18n.Button.confirm)
            self.btn_cancel.add_event_cb(
                lambda _: self.on_click_cancel(), lv.EVENT.CLICKED, None
            )

            self.btn_confirm.add_event_cb(
                lambda _: self.on_click_confirm(), lv.EVENT.CLICKED, None
            )

    def on_nav_back(self, event):
        from trezor.ui import NavigationBack

        # should notify caller
        self.channel.publish(NavigationBack())
        from . import manager
        from trezor import workflow

        workflow.spawn(manager.pop(self))        

    def on_click_confirm(self):
        log.debug(__name__, "Confirm click ok")
        from trezor.ui import Confirm
        self.close(Confirm())

    def on_click_cancel(self):
        # log.debug(__name__, "Confirm click cancel")
        print("Confirm click cancel")
        self.close(Cancel())
        
    def on_click_cancel2(self):
        log.debug(__name__, "Confirm click cancel2")
        # self.close(Cancel())

class SimplePreview(Preview):
    """
    Confirm with a message
    """

    def __init__(self, message: str):
        super().__init__()
        # self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        # self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        self.content: lv.obj
        # self.content.set_style_pad_left(16, lv.PART.MAIN)
        # self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.create_content(lv.obj)
        self.content: lv.obj

        self.content.add_style(theme.Styles.board, lv.PART.MAIN)


        self.text = self.add(lv.label)
        self.text.set_long_mode(lv.label.LONG.WRAP)
        self.text.set_width(lv.pct(90))
        self.text.set_height(lv.SIZE.CONTENT)
        self.text.set_text(message)
        self.text.set_style_text_color(colors.DS.WHITE, 0)
        self.text.set_style_text_line_space(8, 0)
        self.text.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        cur_language = i18n.using.code if i18n.using is not None else None
        #阿拉伯语情况下
        if cur_language == "al":
            self.text.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置显示方向为从右向左
        self.text.center()

    def text_color(self, color):
        self.text.set_style_text_color(color, 0)


class HolderPreConfirm(Preview):
    """
    Confirm with a message with a holder button, when user press `holder` button enough time,
    `ok` button will be enabled
    """

    def __init__(self):
        super().__init__()

        # disable `ok` button, user need hold sometime on to enable `ok` button
        self.btn_confirm.add_state(lv.STATE.DISABLED)
        self.set_style_pad_left(16, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content : HStack
        self.content.items_center()
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)
        self.content.reverse()
        self.content.set_style_pad_bottom(32, lv.PART.MAIN)

        # a holder button, user need hold sometime on to enable `ok` button
        self.holder = self.add(ArcHolder)
        self.holder.set_text(i18n.Button.hold)
        self.holder.add_event_cb(
            lambda _: self.btn_confirm.clear_state(lv.STATE.DISABLED),
            events.HOLDER_DONE,
            None,
        )

        # `content` is remained, for draw all other ui components
        self.create_content(lv.obj)
        self.content.set_flex_grow(1)
