import lvgl as lv

from trezor import log
from trezor.ui import i18n, Style, theme, colors
from trezor.ui.component import HStack, VStack
from trezor.ui.screen import Navigation

class SettingApp(Navigation):
    def __init__(self):
        super().__init__()
        self.title.set_text(i18n.App.setting)

        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色
        # use HStack as content
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.content.set_style_pad_top(20, lv.PART.MAIN)
        # brightness
        from .brightness import Brightness
        Brightness(self.content)

        # language
        from .language import Language
        Language(self.content)

        # wallpaper
        from .wallpaper import Wallpaper
        Wallpaper(self.content)

        # bluetooth
        from .bluetooth import Bluetooth
        Bluetooth(self.content)

        # vibration
        from .vibration import Vibration
        Vibration(self.content)

        # transition animation
        # from .animation import Animation
        # Animation(self.content)

        from .auto import AutoLock
        AutoLock(self.content)

        from .auto import AutoShutdown
        AutoShutdown(self.content)

        # power off
        from .power import PowerOff
        PowerOff(self.content)

        # restart
        # from .power import Restart
        # Restart(self.content)


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
        # self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        self.icon = lv.img(self)
        self.icon.set_src(icon)
        # self.icon.set_style_img_recolor(lv.color_white(), lv.PART.MAIN)  # 让图标变白
        # self.icon.set_style_img_recolor_opa(lv.OPA.COVER, lv.PART.MAIN)  # 确保颜色覆盖

        self.label = lv.label(self)
        self.label.set_flex_grow(1)
        self.label.set_text(text)
        self.label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        self.label.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 确保背景透明
        self.label.set_width(230)  # 设置标签的宽度
        self.label.set_height(40)  # 设置标签的宽度
        # 启动滚动
        self.label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)  # 启用循环滚动模式
        #获取当前语言
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            log.debug(__name__, f"current language--: {cur_language}")
            self.label.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置滚动方向为向右
        else:
            self.label.set_style_base_dir(lv.BASE_DIR.LTR, 0)  # 设置滚动方向为向左
        
        self.label.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN)  # 设置左对齐
        self.label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO) # 滚动条自适应
        # self.timer = lv.timer_create(self._start_scroll, 500, self)

    # def _start_scroll(self, timer):
    #     # 启动滚动
    #     self.label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
    

class SampleItem(Item):
    def __init__(self, parent, text, icon):
        super().__init__(parent, text, icon)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)

    def action(self):
        pass


class ToggleItem(Item):
    def __init__(self, parent, text, icon):
        super().__init__(parent, text, icon)
        self.add_flag(lv.obj.FLAG.CLICKABLE)

        # a switcher for enabling/disabling state
        self.switch = lv.switch(self)
        self.switch.set_height(48)
        self.switch.set_width(96)
        self.switch.add_flag(lv.obj.FLAG.CLICKABLE)
        self.switch.add_event_cb(lambda _: self.toggle(), lv.EVENT.VALUE_CHANGED, None)

        self.switch.set_style_bg_color(lv.color_hex(0x3C84FC), lv.PART.INDICATOR | lv.STATE.CHECKED)
        self.switch.set_style_bg_opa(lv.OPA.COVER, lv.PART.INDICATOR | lv.STATE.CHECKED)

    @property
    def checked(self):
        return self.switch.has_state(lv.STATE.CHECKED)

    @checked.setter
    def checked(self, checked: bool):
        if checked:
            self.switch.add_state(lv.STATE.CHECKED)
        else:
            self.switch.clear_state(lv.STATE.CHECKED)

    def toggle(self):
        pass


__OPTION_VALUE_CHANGED = lv.event_register_id()
class OptionsItem(SampleItem):
    def __init__(self, parent, text, icon):
        super().__init__(parent, text, icon)

        # current option
        self.option = lv.label(self)
        text = self.current()
        self.option.set_text(text)
        self.option.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)

        # right-arrow
        self.arrow = lv.label(self)
        self.arrow.set_text(lv.SYMBOL.RIGHT)
        self.arrow.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)

        # update `option` when an option value is changed
        self.add_event_cb(
            lambda _: self.option.set_text(self.current()),
            __OPTION_VALUE_CHANGED,
            None,
        )

    def current(self) -> str:
        """
        User provides current option
        """
        raise NotImplementedError

    def show_options(self):
        """
        User is showing options and selecting an option
        """
        raise NotImplementedError

    def action(self):
        self.show_options()
