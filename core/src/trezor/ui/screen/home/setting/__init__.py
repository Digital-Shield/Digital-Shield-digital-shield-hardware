import lvgl as lv

from trezor import log
from trezor.ui import i18n, Style, theme, colors, font
from trezor.ui.component import HStack, VStack
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate

class SettingApp(Navigate):
    def __init__(self):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.title.set_text(i18n.App.setting)

        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)# 设置背景颜色
        # use HStack as content
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.content.set_style_pad_top(10, lv.PART.MAIN)

        # # 容器（重新设计布局）
        # self.a_container = lv.obj(self.content)
        # self.a_container.set_size(440, lv.SIZE.CONTENT)
        # self.a_container.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        # #设置背景色
        # self.a_container.set_style_bg_color(lv.color_hex(0x0c0d16), lv.PART.MAIN)
        # self.a_container.set_style_pad_left(20, lv.PART.MAIN)
        # self.a_container.set_style_border_width(0, lv.PART.MAIN)
        # self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        # self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        # self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 20)
        # self.a_container.set_flex_flow(lv.FLEX_FLOW.COLUMN_REVERSE)

        #选项容器1
        self.options_container = HStack(self.content)
        self.options_container.set_size(440,lv.SIZE.CONTENT)
        self.options_container.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.options_container.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container.set_style_radius(20, lv.PART.MAIN) #圆角16
        self.options_container.set_style_pad_left(20, lv.PART.MAIN) #设置左上角显示
        #设置喊行间距0
        self.options_container.set_style_pad_row(0, lv.PART.MAIN)
        # self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN_REVERSE)
        

        # language
        from .language import Language
        Language(self.options_container)

        # wallpaper
        from .wallpaper import Wallpaper
        Wallpaper(self.options_container)

        # 空开一行
        spacer = lv.obj(self.content)
        spacer.set_height(20)
        spacer.set_width(lv.pct(110))
        spacer.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)  # 背景色
        spacer.set_style_border_width(0, lv.PART.MAIN)  # 去掉边框，防止出现竖点
        spacer.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 保证背景不透明
        spacer.set_style_border_side(0, lv.PART.MAIN)  # 去掉所有边

        #选项容器2
        self.options_container2 = HStack(self.content)
        self.options_container2.set_size(440,lv.SIZE.CONTENT)
        self.options_container2.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.options_container2.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.options_container2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container2.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container2.set_style_radius(20, lv.PART.MAIN) #圆角20
        self.options_container2.set_style_pad_left(20, lv.PART.MAIN) #设置左上角显示
        #设置喊行间距0
        self.options_container2.set_style_pad_row(0, lv.PART.MAIN)
        # bluetooth
        from .bluetooth import Bluetooth
        Bluetooth(self.options_container2)

        # vibration
        from .vibration import Vibration
        Vibration(self.options_container2)
        #空开一行
        spacer = lv.obj(self.content)
        spacer.set_height(20)
        spacer.set_width(lv.pct(110))
        spacer.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)#背景色
        spacer.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        spacer.set_style_border_width(0, lv.PART.MAIN)#去掉边框
        # transition animation
        # from .animation import Animation
        # Animation(self.content)

        #选项容器3
        self.options_container3 = HStack(self.content)
        self.options_container3.set_size(440,lv.SIZE.CONTENT)
        self.options_container3.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.options_container3.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.options_container3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container3.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container3.set_style_radius(20, lv.PART.MAIN) #圆角20
        self.options_container3.set_style_pad_left(20, lv.PART.MAIN) #设置左上角显示
        #设置喊行间距0
        self.options_container3.set_style_pad_row(0, lv.PART.MAIN)
        # brightness
        from .brightness import Brightness
        Brightness(self.options_container3)

        from .auto import AutoLock
        AutoLock(self.options_container3)

        from .auto import AutoShutdown
        app = AutoShutdown(self.options_container3)
        #空开一行
        spacer = lv.obj(self.content)
        spacer.set_height(20)
        spacer.set_width(lv.pct(110))
        spacer.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)#背景色
        spacer.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        spacer.set_style_border_width(0, lv.PART.MAIN)#去掉边框

        #选项容器4
        self.options_container4 = HStack(self.content)
        self.options_container4.set_size(440,lv.SIZE.CONTENT)
        self.options_container4.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.options_container4.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.options_container4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container4.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container4.set_style_radius(20, lv.PART.MAIN) #圆角20
        self.options_container4.set_style_pad_left(20, lv.PART.MAIN) #设置左上角显示
        #设置喊行间距0
        self.options_container4.set_style_pad_row(0, lv.PART.MAIN)
        # power off
        from .power import PowerOff
        PowerOff(self.options_container4)

        #设置上下行间距0
        self.content.set_style_pad_row(0, lv.PART.MAIN)
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
            # .radius(16)
            .bg_color(lv.color_hex(0x15151E))  # 深色背景
            .bg_opa(lv.OPA._90)  # 90% 不透明，避免影响子组件
            #字号28
            .text_font(font.Regular.SCS30)
            # .bg_opa(lv.OPA.COVER)
            .width(400)
            .height(90)
            # .pad_row(200)
            .pad_top(10)
            .pad_left(20)
            .pad_right(20)
            .pad_column(16),
            0,
        )
        # self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        self.icon = lv.img(self)
        self.icon.set_src(icon)
        self.icon.set_style_pad_bottom(5, lv.PART.MAIN)
        self.icon.set_zoom(int(256 *1.3))  # 设置为原尺寸的1.3倍
        
        # self.icon.set_style_img_recolor(lv.color_white(), lv.PART.MAIN)  # 让图标变白
        # self.icon.set_style_img_recolor_opa(lv.OPA.COVER, lv.PART.MAIN)  # 确保颜色覆盖

        self.label = lv.label(self)
        self.label.set_flex_grow(1)
        self.label.set_text(text)
        self.label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        self.label.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 确保背景透明
        self.label.set_width(230)  # 设置标签的宽度
        self.label.set_height(66)  # 设置标签的高度
        self.label.set_style_pad_top(15, lv.PART.MAIN)  # 增大下边距
        #28号字体
        self.label.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
        # self.label.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)  # 设置垂直居中对齐
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
        # self.label.set_style_pad_bottom(10, lv.PART.MAIN)
        # # arrow
        # self.arrow = lv.img(self)
        # #设置箭头背景图
        # self.arrow.set_src("A:/res/a_right_arrow.png")


        # self.arrow.set_width(32)
        # self.arrow.set_height(32)
        # #显示到item最右边
        # self.arrow.set_style_pad_left(200, lv.PART.MAIN)
        # self.timer = lv.timer_create(self._start_scroll, 500, self)

    # def _start_scroll(self, timer):
    #     # 启动滚动
    #     self.label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
    

class SampleItem(Item):
    def __init__(self, parent, text, icon):
        super().__init__(parent, text, icon)
        # print("icon",icon)
        # self.add_flag(lv.obj.FLAG.CLICKABLE)
        # 添加底边灰色边框
        self.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        self.set_style_border_width(1, lv.PART.MAIN)
        self.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
        self.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)
        if icon in [
            "A:/res/wallpaper-two.png",
            "A:/res/auto-power-off-two.png",
            "A:/res/power-off-two.png",
        ]:
            self.set_style_border_width(0, lv.PART.MAIN)#不显示底边线
        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)

    def action(self):
        pass


class ToggleItem(Item):
    def __init__(self, parent, text, icon):
        super().__init__(parent, text, icon)
        self.add_flag(lv.obj.FLAG.CLICKABLE)

        # a switcher for enabling/disabling state
        self.switch = lv.switch(self)
        self.switch.set_height(40)
        self.switch.set_width(80)
        self.switch.add_flag(lv.obj.FLAG.CLICKABLE)
        self.switch.add_event_cb(lambda _: self.toggle(), lv.EVENT.VALUE_CHANGED, None)
        # 添加底边灰色边框
        self.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        self.set_style_border_width(2, lv.PART.MAIN)
        self.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
        self.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)
        #底边线显示
        if icon in [
            "A:/res/vibration-two.png",
        ]:
            self.set_style_border_width(0, lv.PART.MAIN)#不显示底边线
        self.switch.set_style_bg_color(lv.color_hex(0x3C84FC), lv.PART.INDICATOR | lv.STATE.CHECKED)
        self.switch.set_style_bg_opa(lv.OPA.COVER, lv.PART.INDICATOR | lv.STATE.CHECKED)
        #上边距10
        # self.switch.set_style_pad_top(5, lv.PART.MAIN)
        #设置self.arrow箭头为不显示
        # self.arrow.add_flag(lv.obj.FLAG.HIDDEN)

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
        self.option.set_style_pad_bottom(0, lv.PART.MAIN)  # 增大右边距
        self.option.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)

        # right-arrow
        # self.arrow = lv.label(self)
        # self.arrow.set_text(lv.SYMBOL.RIGHT)
        # self.arrow.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        # self.arrow = lv.img(self)
        # self.arrow.set_width(32)
        # self.arrow.set_height(32)
        # #设置箭头背景图
        # self.arrow.set_src("A:/res/a_right_arrow.png")
        # arrow
        self.arrow = lv.img(self)
        #设置箭头背景图
        self.arrow.set_src("A:/res/a_right_arrow.png")
        #设置在self.option最右边
        self.arrow.align_to(self.option, lv.ALIGN.OUT_RIGHT_MID, 0,0)
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
