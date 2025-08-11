import lvgl as lv

from trezor import log
from storage import device
from trezor.ui import i18n, Style, theme, colors, font
from trezor.ui.component import HStack, VStack
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate

class SecurityApp(Navigate):
    def __init__(self):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_title(i18n.App.security)

        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        self.create_content(HStack)
        self.content: HStack

        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.content.set_style_pad_top(15, lv.PART.MAIN)  # 设置顶部填充

        # 容器（重新设计布局）
        self.a_container = lv.obj(self.content)
        self.a_container.set_size(440, lv.SIZE.CONTENT)
        self.a_container.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        #设置背景色
        self.a_container.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.a_container.set_style_pad_left(20, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 20)

         # 选项
        self.options_container = HStack(self.a_container)
        self.options_container.set_size(440, lv.SIZE.CONTENT)
        self.options_container.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container.set_style_radius(20, lv.PART.MAIN)#圆角20
        self.options_container.set_width(lv.pct(100))
        self.options_container.align(lv.ALIGN.TOP_LEFT, -8, 0)
        self.options_container.set_style_border_width(0, lv.PART.MAIN)
        self.options_container.set_style_pad_left(15, lv.PART.MAIN)#设置左上角显示
        #设置喊行间距0
        self.options_container.set_style_pad_row(0, lv.PART.MAIN)

        # change pin
        from .pin import ChangePin
        ChangePin(self.options_container)

        # backup mnemonic
        if device.needs_backup():
            from .mnemonic import BackupMnemonic
            BackupMnemonic(self.options_container)

        # check mnemonic
        from .mnemonic import CheckMnemonic
        CheckMnemonic(self.options_container)

        # wipe device
        from .wipe import WipeDevice
        WipeDevice(self.options_container)


class Item(VStack):
    """
    Item with an icon and text
    """

    def __init__(self, parent, text, icon):
        super().__init__(parent)
        self.items_center()
        self.add_style(
            Style()
            # .radius(16)
            .bg_color(lv.color_hex(0x15151E))  # 深色背景
            .bg_opa(lv.OPA._90)  # 90% 不透明，避免影响子组件
            #字体28号
            .text_font(font.Regular.SCS30)
            # .bg_opa(lv.OPA.COVER)
            .width(400)
            .height(92)
            # .pad_right(32)
            # .pad_column(16)
            ,
            0,
        )
        self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        if text != i18n.Security.wipe_device: 
            # 添加底边灰色边框
            self.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
            self.set_style_border_width(2, lv.PART.MAIN)
            self.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
            self.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)
        #获取当前语言
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            log.debug(__name__, f"current language--: {cur_language}")
            self.label = lv.label(self)
            self.label.set_flex_grow(1)
            self.label.set_text(text)
            self.label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)#字体白色
            self.label.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 确保背景透明
            # self.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN)  # 设置右对齐
            self.label.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置显示方向为从右向左
            #28号字体
            self.label.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
            
            self.icon = lv.img(self)
            self.icon.set_src(icon)
            self.icon.set_zoom(int(256 *1.3))  # 设置为原尺寸的1.3倍
        else:
            self.icon = lv.img(self)
            self.icon.set_src(icon)
            self.icon.set_zoom(int(256 *1.3))  # 设置为原尺寸的1.3倍

            self.label = lv.label(self)
            self.label.set_flex_grow(1)
            self.label.set_text(text)
            self.label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)#字体白色
            self.label.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 确保背景透明
            #28号字体
            self.label.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
        # 启动滚动
        self.label.set_width(200)  # 设置标签的宽度
        self.label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)  # 启用循环滚动模式
        self.label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)  # 滚动条自适应

        # arrow
        self.arrow = lv.img(self)
        #设置箭头背景图
        self.arrow.set_src("A:/res/a_right_arrow.png")
        #右侧显示
        # self.arrow.set_style_align(lv.ALIGN.RIGHT_MID, lv.PART.MAIN)
        # self.arrow.set_style_pad_left(70, lv.PART.MAIN)
        # self.arrow.set_width(32)
        # self.arrow.set_height(32)

class SampleItem(Item):
    def __init__(self, parent, text, icon):
        super().__init__(parent, text, icon)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)

    def action(self):
        pass
