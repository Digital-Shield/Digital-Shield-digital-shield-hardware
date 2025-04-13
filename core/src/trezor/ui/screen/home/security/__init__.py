import lvgl as lv

from trezor import log
from storage import device
from trezor.ui import i18n, Style, theme, colors
from trezor.ui.component import HStack, VStack
from trezor.ui.screen import Navigation

class SecurityApp(Navigation):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.App.security)

        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        self.create_content(HStack)
        self.content: HStack

        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.content.set_style_pad_top(15, lv.PART.MAIN)  # 设置顶部填充

        # change pin
        from .pin import ChangePin
        ChangePin(self.content)

        # backup mnemonic
        if device.needs_backup():
            from .mnemonic import BackupMnemonic
            BackupMnemonic(self.content)

        # check mnemonic
        from .mnemonic import CheckMnemonic
        CheckMnemonic(self.content)

        # wipe device
        from .wipe import WipeDevice
        WipeDevice(self.content)


class Item(VStack):
    """
    Item with an icon and text
    """

    def __init__(self, parent, text, icon):
        super().__init__(parent)
        self.items_center()
        self.add_style(
            Style()
            .radius(16)
            .bg_color(lv.color_hex(0x111126))  # 深色背景
            .bg_opa(lv.OPA._90)  # 90% 不透明，避免影响子组件
            # .bg_opa(lv.OPA.COVER)
            .width(lv.pct(100))
            .height(72)
            .pad_right(32)
            .pad_column(16),
            0,
        )
        self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        
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
            
            self.icon = lv.img(self)
            self.icon.set_src(icon)
        else:
            self.icon = lv.img(self)
            self.icon.set_src(icon)

            self.label = lv.label(self)
            self.label.set_flex_grow(1)
            self.label.set_text(text)
            self.label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)#字体白色
            self.label.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 确保背景透明
        # 启动滚动
        self.label.set_width(200)  # 设置标签的宽度
        self.label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)  # 启用循环滚动模式
        self.label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)  # 滚动条自适应

class SampleItem(Item):
    def __init__(self, parent, text, icon):
        super().__init__(parent, text, icon)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)

    def action(self):
        pass
