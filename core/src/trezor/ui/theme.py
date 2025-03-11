import lvgl as lv

from trezor import log

from . import colors
from . import font
from . import Style


class DSTheme(lv.theme_t):
    def __init__(self, parent: lv.theme_t = None):
        super().__init__()
        self.set_parent(parent or lv.theme_default_get())
        self.set_apply_cb(self.theme_apply_cb)

    def theme_apply_cb(self, theme, obj: lv.obj):
        typ = obj.get_class()
        if typ == lv.label_class:
            parent = obj.get_parent()
            if parent.get_class() == lv.btn_class:
                obj.add_style(Styles.button_label, lv.PART.MAIN)
                obj.add_style(Styles.disabled, lv.STATE.DISABLED)
                return
            if parent.get_class() == lv.textarea_class:
                obj.add_style(Styles.ta_label, lv.PART.MAIN)
                return
            obj.add_style(Styles.label, lv.PART.MAIN | lv.STATE.DEFAULT)
            obj.add_style(Styles.label_disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        elif typ == lv.btn_class:
            obj.add_style(Styles.button, lv.PART.MAIN)
            obj.add_style(Styles.pressed, lv.STATE.PRESSED)
            obj.add_style(Styles.disabled, lv.STATE.DISABLED)

        # 回调函数在调用时，obj对象会转换成lvgl内部对象，无法保留子类信息
        # 例如 class Title(lv.label), 只能获取到都应的lvgl对象
        # 故而无法在此处统一对子类进行设置style
        # from .component.title import Title, Subtitle
        # if isinstance(obj, Title):
        #     log.debug(__name__, "Got a `Title` object")
        #     obj.add_style(Styles.title, lv.PART.MAIN)
        # elif isinstance(obj, Subtitle):
        #     log.debug(__name__, "Got a `Subtitle` object")
        #     obj.add_style(Styles.subtitle, lv.PART.MAIN)


def ds_theme():
    # default theme
    theme = lv.theme_default_init(
        None,
        colors.DS.PRIMARY,  # primary color
        colors.DS.SECONDARY,  # secondary color
        False,  # dark mode? No
        lv.font_default(),
    )
    disp = lv.disp_get_default()
    disp.set_theme(DSTheme(theme))


pressed_dsc = lv.color_filter_dsc_t()
pressed_dsc.init(lambda _, c, o: colors.DS.PRESSED_FILTER_COLOR.color_mix(c, o))

checked_dsc = lv.color_filter_dsc_t()
checked_dsc.init(lambda _, c, o: colors.DS.CHECKED_FILTER_COLOR.color_mix(c, o))

disabled_dsc = lv.color_filter_dsc_t()
disabled_dsc.init(lambda _, c, o: colors.DS.DISABLED_FILTER_COLOR.color_mix(c, o))


class Styles:
    primary = Style().bg_color(colors.DS.PRIMARY)

    label = Style().text_color(colors.DS.BLACK)
    label = Style().text_font(font.Bold.SCS30)
    label_disabled = Style().text_color(colors.DS.TEXT_DISABLED)

    ta_label = Style().text_color(colors.STD.WHITE)

    button = Style().radius(lv.RADIUS.CIRCLE)
    button_label = (
        Style()
        .text_color(colors.DS.BUTTON_TEXT)
        .text_align(lv.TEXT_ALIGN.CENTER)
        .bg_color(lv.color_hex(0x3C84FC))
        .align(lv.ALIGN.CENTER)
    )

    pin_keyboard = (
        Style()
        .border_width(0)
        .bg_opa(lv.OPA.TRANSP)
        .pad_all(16)
        .pad_row(12)
        .pad_column(12)
    )
    pin_keyboard_btn = (
        Style()
        .radius(12)
        .shadow_color(colors.DS.SHADOW)
        .shadow_opa(colors.DS.SHADOW_OPA)
        .shadow_ofs_y(2)
        .shadow_width(8)
        .shadow_spread(4)
    )
    pin_keyboard_pressed = (
        Style()
        .text_color(colors.DS.KEYBOARD_PRESSED_TEXT_COLOR)
        .shadow_color(colors.DS.SHADOW)
        .shadow_opa(colors.DS.SHADOW_OPA)
        .shadow_ofs_x(4)
        .shadow_ofs_y(4)
        .shadow_width(8)
        .shadow_spread(4)
        .bg_color(colors.DS.KEYBOARD_PRESSED)
    )

    mnemonic_keyboard = (
        Style()
        .border_width(0)
        .bg_opa(lv.OPA.TRANSP)
        .pad_all(2)
        .pad_column(5)
        .pad_row(3)
    )
    mnemonic_keyboard_btn = Style().radius(4).shadow_ofs_y(2).shadow_width(4)

    pressed = (
        Style()
        .color_filter_opa(colors.DS.PRESSED_FILTER_OPA)
        .color_filter_dsc(pressed_dsc)
    )

    checked = (
        Style()
        .color_filter_opa(colors.DS.CHECKED_FILTER_OPA)
        .color_filter_dsc(checked_dsc)
    )

    focused = Style().border_color(colors.DS.PRIMARY).border_width(1)
    disabled = (
        Style()
        .color_filter_opa(colors.DS.DISABLED_FILTER_OPA)
        .color_filter_dsc(disabled_dsc)
    )

    # 组件的style无法在callback里统一设置，但是尽量在此处配置style，不要分散在组件里去设置
    # 此处设置style然后在组件代码里进行添加

    # a filled transparent container
    container = (
        Style()
        .pad_all(0)
        .width(lv.pct(100))
        .height(lv.pct(100))
        .bg_opa(lv.OPA.TRANSP)
        .border_width(0)
        # .border_width(1)
        # .border_color(colors.DS.BLUE)
    )

    # message pad
    board = (
        Style()
        .pad_all(16)
        # .bg_opa(lv.OPA.COVER)
        .bg_opa(lv.OPA.TRANSP)
        .radius(16)
    )
    title_text = Style().text_font(font.Bold.SCS38)

    popup = (
        Style()
        .text_font(font.Bold.SCS38)
        .width(lv.pct(100))
        .text_align(lv.TEXT_ALIGN.CENTER)
    )

    subtitle = Style().text_font(font.Regular.SCS24).text_color(colors.DS.GRAY)

    # apps in home screen: icon and a label
    home_app = (
        Style()
        # .bg_color(colors.DS.WHITE)
        # .bg_opa(lv.OPA._60)
        .pad_top(0)
        .pad_bottom(0)
        .pad_column(0)
        .width(194)
        .height(194)
        .radius(20)
        .border_width(0)
    )


ds_theme()
