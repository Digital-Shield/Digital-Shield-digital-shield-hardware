import lvgl as lv
from trezor.ui import i18n, Style, theme, colors
from trezor.ui.component import HStack, VStack, LabeledItem,LabeledText
from trezor.ui.screen import Navigation, with_title
from trezor import log, workflow
class GuideApp(with_title(Navigation)):
    def __init__(self):
        super().__init__()
        # self.set_title(i18n.App.guide)
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        title_label = lv.label(self)
        title_label.set_text(i18n.App.guide)
        title_label.align(lv.ALIGN.TOP_MID, 0, 10)  # 让标题居中
        title_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        
        # use HStack as content
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.content.set_style_pad_top(15, lv.PART.MAIN)  # 设置顶部填充
        guides = [
            # terms of use
            {
                "label": i18n.Guide.terms_of_use,
                "action": self.click_terms,
            },
            # device info
            {
                "label": i18n.Guide.device_info,
                "action": self.click_device,
            },
            # firmware update
            {
                "label": i18n.Guide.firmware_update,
                "action": self.click_firmware,
            },
            # about
            {
                "label": i18n.Guide.about,
                "action": self.click_about,
            },
        ]

        for g in guides:
            label, action = g["label"], g["action"]
            app = Item(self.content, label)
            app.action = action
            
    def click_terms(self):
        log.debug(__name__, "click terms")
        from .terms import Terms
        workflow.spawn(Terms(i18n.Guide.terms_of_use).show())

    def click_device(self):
        log.debug(__name__, "click device")
        from .device import Device
        workflow.spawn(Device(i18n.Guide.device_info).show())

    def click_firmware(self):
        log.debug(__name__, "click firmware")
        from .firmware import Firmware
        workflow.spawn(Firmware(i18n.Guide.firmware_update).show())
    
    def click_about(self):
        log.debug(__name__, "click about")
        from .about import About
        workflow.spawn(About(i18n.Guide.about).show())
class Item(VStack):
    """
    Item with and text
    """
    def __init__(self, parent, text):
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
          #获取当前语言，判断阿拉伯语
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            # right-arrow
            self.arrow = lv.label(self)
            self.arrow.set_text(lv.SYMBOL.LEFT)
            self.arrow.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN) # type: ignore
            # text
            self.label = lv.label(self)
            self.label.set_flex_grow(1)
            self.label.set_text(text)
            self.label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)#字体白色
            self.label.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 确保背景透明
            self.label.add_style(Style().pad_right(10),0)
            self.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN)  # 设置右对齐
            self.add_flag(lv.obj.FLAG.CLICKABLE)
        else:
            # text
            self.label = lv.label(self)
            self.label.set_flex_grow(1)
            self.label.set_text(text)
            self.label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)#字体白色
            self.label.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 确保背景透明
            self.label.add_style(Style().pad_left(10),0)
            self.add_flag(lv.obj.FLAG.CLICKABLE)
            # right-arrow
            self.arrow = lv.label(self)
            self.arrow.set_text(lv.SYMBOL.RIGHT)
            self.arrow.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN) # type: ignore

        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)
  
    def action(self):
        pass
class QrcodeDetail(with_title(Navigation)):
    def __init__(self, title: str ,qrcode: str ):
        super().__init__()
        self.set_title(title)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style().pad_left(16).pad_right(16),
            0
        )
        contaner = self.add(lv.obj)
        contaner.add_style(
            theme.Styles.container,
            0
        )
        contaner.set_height(lv.SIZE.CONTENT)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        contaner.clear_flag(lv.obj.FLAG.SCROLLABLE)
        self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        # qrcode
        view = lv.qrcode(contaner, 440, colors.DS.BLACK, colors.DS.WHITE)
        view.set_style_border_width(5, lv.PART.MAIN)
        view.set_style_radius(25, lv.PART.MAIN)
        view.update(qrcode, len(qrcode))
        view.center()
        # text
        label = lv.label(self.content)
        label.set_text(qrcode)
        label.add_style(Style()
                        .text_color(lv.color_hex(0x37b7ae)),
                        0)
        label.set_width(500)
        label.set_flex_grow(1)
        label.set_long_mode(lv.label.LONG.WRAP)
       