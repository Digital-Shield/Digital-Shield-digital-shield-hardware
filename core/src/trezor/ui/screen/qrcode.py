import lvgl as lv

from . import Modal,Navigation
from trezor.ui import i18n, colors, font, Done, Cancel
from trezor.ui import i18n, Style, theme
from trezor.ui.theme import Styles
from trezor.ui.screen.confirm import Confirm
from trezor.ui.screen.message import Message
from trezor.ui.component.container import HStack

from trezor.ui.types import *

if TYPE_CHECKING:

    class DigtalMessage(Protocol):
        # header: str | None = None
        tips: List[str] | None = None

class Qrcode(Modal):
    """
    A Popup screen with a log and a message, will auto close after a timeout


    User not need do anything, it just show some message. e.g. "Unlocking..." "Wiping ..."
    """
    def __init__(self, title: str, message: str, show_qrcode: bool=False, messages: DigtalMessage | None = None) -> None:
        super().__init__()
        self._address = "https://ds.pro"
        self.set_title("")
        self.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        # 隐藏原有的btn_right按钮
        self.btn_left.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_right.set_text(i18n.Button.continue_)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.set_style_width(440, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        

         # 容器（重新设计布局）
        self.a_container = lv.obj(self)
        self.a_container.set_size(436, 400)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.set_style_pad_left(40, lv.PART.MAIN)
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 30)
        self.content.set_style_pad_top(0, lv.PART.MAIN)
        self.content.set_style_pad_left(30, lv.PART.MAIN)
        self.content.align(lv.ALIGN.TOP_LEFT, 0, 30)
        #隐藏滚动条
        self.content.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF) 

        self.text1 = lv.label(self.content)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(title)
        #字号38
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        # self.text1.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        # self.text1.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.texts = []
        if messages and messages.tips:
            for idx, msg in enumerate(messages.tips):
                text2 = lv.label(self.a_container)
                text2.set_long_mode(lv.label.LONG.WRAP)
                text2.set_width(lv.pct(100))
                text2.set_height(lv.SIZE.CONTENT)
                if idx == 1:
                    # bluetooth name
                    from trezor import utils
                    ble_name = utils.BLE_NAME if utils.BLE_NAME is not None else ""
                    print("ble_name",ble_name)
                    msg = msg + ble_name
                text2.set_text(msg)
                text2.set_style_pad_top(30, lv.PART.MAIN)
                text2.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)
                text2.set_style_text_color(colors.DS.WHITE, 0)
                # 设置每条消息的垂直位置，避免重叠
                if idx == len(messages.tips)-1:
                    text2.align(lv.ALIGN.TOP_LEFT, 0, 40 + idx * 50)
                else:
                    text2.align(lv.ALIGN.TOP_LEFT, 0, 40 + idx * 40)
                #行间距10
                text2.set_style_text_line_space(10, lv.PART.MAIN)
                self.texts.append(text2)
                #行间距20
                # text2.set_style_text_line_space(20, lv.PART.MAIN)
        else:        
            self.text2 = lv.label(self.content)
            self.text2.set_long_mode(lv.label.LONG.WRAP)
            self.text2.set_width(lv.pct(90))
            self.text2.set_height(lv.SIZE.CONTENT)
            self.text2.set_text(message)
            #设置行间距10
            self.text2.set_style_text_line_space(10, 0)
            self.text2.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)
            self.text2.set_style_text_color(colors.DS.WHITE, 0)
            self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 60)

        self.btn_right.add_event_cb(
            lambda _: self.on_click_confirm(), lv.EVENT.CLICKED, None
        )
        if show_qrcode:
            # 二维码容器（居中布局）
            self.qrcode_container = lv.obj(self.content)
            self.qrcode_container.set_size(360, 360)
            self.qrcode_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
            # self.qrcode_container.align(lv.ALIGN.TOP_MID, 0, 100)  # 调整垂直位置
            self.qrcode_container.set_style_shadow_width(0, lv.PART.MAIN)
            self.qrcode_container.set_style_outline_width(0, lv.PART.MAIN)
            self.qrcode_container.align(lv.ALIGN.TOP_LEFT, 10, 210)  # 调整垂直位置
            self.qrcode_container.set_style_border_width(0, lv.PART.MAIN)
            # self.qrcode_container.set_style_border_color(colors.DS.GRAY, lv.PART.MAIN)
            view = lv.qrcode(self.qrcode_container, 280, colors.DS.BLACK, colors.DS.WHITE)
            view.set_style_border_width(24, lv.PART.MAIN)
            #去除二维码内部白边
            view.set_style_shadow_width(0, lv.PART.MAIN)
            view.set_style_outline_width(0, lv.PART.MAIN)
            view.set_style_radius(24, lv.PART.MAIN)
            view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
            view.update(self._address, len(self._address))
            view.center()
            # 在二维码中心添加icon图片
            icon_path = "A:/res/dunan.png"
            
            icon_img = lv.img(self.qrcode_container)
            icon_img.set_src(icon_path)
            # 保证图片完整显示
            icon_img.set_zoom(300)  # 1.0倍缩放，防止裁剪
            icon_img.set_style_img_opa(lv.OPA.COVER, 0)
            icon_img.set_style_img_recolor_opa(lv.OPA.TRANSP, 0)
            icon_img.set_style_clip_corner(0, 0)
            # 添加白色四方形背景容器（无边框）
            bg_container = lv.obj(self.qrcode_container)
            bg_container.set_size(60, 60)
            bg_container.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
            bg_container.set_style_radius(16, lv.PART.MAIN)  # 四方形，无圆角
            bg_container.set_style_border_width(0, lv.PART.MAIN)
            bg_container.set_style_border_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 彻底隐藏边框
            bg_container.set_style_shadow_width(0, lv.PART.MAIN)
            bg_container.align_to(view, lv.ALIGN.CENTER, 0, 0)
            bg_container.move_foreground()

            # 将icon图片放到背景容器上方并居中
            icon_img.align_to(bg_container, lv.ALIGN.CENTER, 0, 0)
            icon_img.move_foreground()
            # 居中到二维码中心
            icon_img.align_to(view, lv.ALIGN.CENTER, 0, 0)
            # 置于二维码之上
            icon_img.move_foreground()
            self._qrcode_icon = icon_img
        
        
     #点击确认
    def on_click_confirm(self):
        from trezor.ui import Confirm
        
        from trezor.ui.screen import manager
        manager.mark_dismissing(self)
        self.close(Confirm())
        # self.close(Done())
        # from .home import HomeScreen
        # from trezor import workflow
        # workflow.spawn(HomeScreen().show())
    # #点完成则返回
    def on_click_cancel(self):
        # self.close(Cancel())
        from trezor.ui import NavigationBack
        self.channel.publish(NavigationBack())
        # from . import manager
        # from trezor import workflow
        # workflow.spawn(manager.pop(self))
