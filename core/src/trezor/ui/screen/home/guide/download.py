import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from trezor.ui import Style, font
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate

if TYPE_CHECKING:
    from typing import List
    pass

class Download(Navigate):
    def __init__(self,title):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_title(title)
        self._address = "https://ds.pro"
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .pad_left(16)
            .pad_right(16)
            .pad_top(25),
            0
        )

        view = self.add(lv.label)
        view.set_text(i18n.Text.download_digital_tips)
        view.set_width(430)  # 设置固定宽度（例如 300 像素）
        #边框宽度2
        # view.set_style_border_width(2, lv.PART.MAIN)
        #颜色白色
        # view.set_style_border_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        view.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)
        #白色
        view.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        #行间距10
        view.set_style_text_line_space(10, lv.PART.MAIN)
        view.set_style_pad_left(40, lv.PART.MAIN)
        view.set_long_mode(lv.label.LONG.WRAP)
        # view.set_style_text_font(font.Bold.SCS26, lv.PART.MAIN)  # 使用较小的字体
        cur_language = i18n.using.code if i18n.using is not None else None
        #阿拉伯语
        if cur_language == "al":
            view.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置文本方向为从右到左

        # 二维码容器（居中布局）
        self.qrcode_container = lv.obj(self)
        self.qrcode_container.set_size(360, 360)
        self.qrcode_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        # self.qrcode_container.align(lv.ALIGN.TOP_MID, 0, 100)  # 调整垂直位置
        self.qrcode_container.set_style_shadow_width(0, lv.PART.MAIN)
        self.qrcode_container.set_style_outline_width(0, lv.PART.MAIN)
        self.qrcode_container.align(lv.ALIGN.TOP_LEFT, 50, 214)  # 调整垂直位置
        self.qrcode_container.set_style_border_width(0, lv.PART.MAIN)
        
        view = lv.qrcode(self.qrcode_container, 300, colors.DS.BLACK, colors.DS.WHITE)
        view.set_style_border_width(24, lv.PART.MAIN)
        #去除二维码内部白边
        view.set_style_shadow_width(0, lv.PART.MAIN)
        view.set_style_outline_width(0, lv.PART.MAIN)
        view.set_style_radius(24, lv.PART.MAIN)
        view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
        view.set_style_radius(25, lv.PART.MAIN)
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
        
