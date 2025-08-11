import lvgl as lv
from micropython import const

from . import Modal
from trezor.ui import i18n
from trezor.ui.theme import Styles
from trezor.ui.component.container import VStack, HStack

# 颜色定义（白色到蓝色渐变）
_WHITE = lv.color_hex(0xFFFFFF)
_BLUE = lv.color_hex(0x0062CE)

# 保留原始Popup类（若需要）
class Popup(Modal):
    """原始Popup类，保持不变"""
    def __init__(self, operating: str, icon: str|None=None):
        super().__init__()

        self.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)
        # self.set_style_bg_img_src("A:/res/wallpapers/4.png", lv.PART.MAIN)
        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.add_style(Styles.popup_board, lv.PART.MAIN)

        self.content.items_center()
        self.content.center()  
        # self.auto_close_timeout = 200
        # self.add(lv.img).set_src(icon or "A:/res/logo_two.png")

        self.text = self.add(lv.label)
        self.text.add_style(Styles.popup, lv.PART.MAIN)
        self.text.set_long_mode(lv.label.LONG.WRAP)
        self.text.set_text(operating)
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            self.text.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置显示方向从右向左
        self.text_color(lv.color_hex(0xFFFFFF))  
        # auto close after 1.5 seconds
        self.auto_close_timeout = 2500

    def text_color(self, color):
        self.text.set_style_text_color(color, 0)

class LoadingPopup(Popup):
    def __init__(self, operating: str, icon: str | None = None, duration: int = 1000):
        """
        带圆环加载动画的弹窗（适配ArcLoader逻辑）
        :param operating: 显示文本（如"加载中..."）
        :param icon: 图标路径（可选）
        :param duration: 动画持续时间（毫秒，默认1500ms）
        """
        super().__init__(operating, icon)
        self.duration = duration
        self.text.set_text("")
        # 使用VStack布局
        self.create_content(VStack)
        self.content: VStack
        self.content.set_flex_align(
            lv.FLEX_ALIGN.CENTER,
            lv.FLEX_ALIGN.CENTER,
            lv.FLEX_ALIGN.CENTER
        )
        self.content.set_style_pad_all(20, lv.PART.MAIN)

        # 创建圆环
        self.arc = lv.arc(self.content)
        self.arc.set_size(120, 120)
        self.arc.set_bg_angles(0, 360)
        self.arc.set_angles(270, 270)
        self.arc.remove_style(None, lv.PART.KNOB)  # 彻底移除旋钮部件
        self.arc_style = lv.style_t()
        self.arc_style.init()
        self.arc_style.set_line_width(10)
        self.arc_style.set_line_color(_WHITE)
        self.arc_style.set_line_opa(255)
        self.arc_style.set_bg_grad_color(_BLUE)
        self.arc_style.set_bg_opa(lv.OPA.TRANSP)
        # 关键：去掉圆头
        self.arc_style.set_arc_width(10)
        self.arc_style.set_line_rounded(False)
        self.arc.add_style(self.arc_style, lv.PART.INDICATOR)  # 应用到 INDICATOR 部分
        self.arc.add_style(self.arc_style, lv.PART.MAIN)       # 可选：也应用到 MAIN

        # 加载动画控制器
        self._arc_loader_angle = 270
        self._arc_loader_timer = lv.timer_create(self._arc_loader_cb, 10, None)
        self._arc_loader_start = lv.tick_get()

    def _arc_loader_cb(self, timer):
        # 每次回调增加角度
        self._arc_loader_angle += 5
        self.arc.set_angles(270, self._arc_loader_angle)
        # 判断是否到达一圈
        if self._arc_loader_angle >= 270 + 360 or lv.tick_elaps(self._arc_loader_start) >= self.duration:
            timer._del()
            self.close(self)
