import lvgl as lv

from . import Modal
from trezor.ui import i18n, colors, font
from trezor.ui.theme import Styles
from trezor.ui.component.container import HStack

class Tips(Modal):
    """
    A Popup screen with a log and a message, will auto close after a timeout


    User not need do anything, it just show some message. e.g. "Unlocking..." "Wiping ..."
    """
    def __init__(self, title: str, message: str, icon: str|None=None):
        super().__init__()

        self.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        # 隐藏原有的btn_right按钮
        self.btn_right.add_flag(lv.obj.FLAG.HIDDEN)

        # self.create_content(HStack)
        # self.content: HStack
        # self.add_style(Styles.popup_board, lv.PART.MAIN)

        # self.content.items_center()
        # self.content.center()

        self.icon = self.add(lv.img)
        self.icon.set_src(icon or "A:/res/word_error.png")
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
        self.a_container.set_size(460, 400)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_pad_left(0, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align_to(self.icon, lv.ALIGN.TOP_LEFT, 10, 100)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(title)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_text_font(font.Medium.SCS40, lv.PART.MAIN)

        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(message)
        self.text2.set_style_text_line_space(10, lv.PART.MAIN)
        self.text2.set_style_text_font(font.Medium.SCS28, lv.PART.MAIN)
        self.text2.set_style_text_color(colors.DS.WHITE, 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 60)
        # auto close after 1.5 seconds
        self.auto_close_timeout = 5000
        # 倒计时相关
        self.remaining_time = self.auto_close_timeout // 1000  # 秒
        self.countdown_label = lv.label(self)
        self.countdown_label.set_text(f"{self.remaining_time}秒后重启")
        self.countdown_label.set_style_text_color(colors.DS.RED, 0)
        self.countdown_label.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
        self.countdown_label.align(lv.ALIGN.BOTTOM_MID, 0, -20)

        def update_countdown(timer):
            self.remaining_time -= 1
            if self.remaining_time > 0:
                self.countdown_label.set_text(i18n.Text.restart_countdown.format(self.remaining_time))
            else:
                timer._del()
                # self.close(True)
                from trezor import utils
                utils.reset()

        self._timer = lv.timer_create(update_countdown, 1000, None)


