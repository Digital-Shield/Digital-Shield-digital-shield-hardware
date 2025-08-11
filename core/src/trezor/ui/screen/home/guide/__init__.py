import lvgl as lv
from trezor.ui import i18n, Style, theme, colors, font
from trezor.ui.component import HStack, VStack, LabeledItem,LabeledText
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate
from trezor import log, workflow
class GuideApp(Navigate):
    def __init__(self):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.title.set_text(i18n.App.guide)

        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色


        # use HStack as content
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.content.set_style_pad_top(15, lv.PART.MAIN)  # 设置顶部填充
        guides = [
            # device info
            {
                "label": i18n.Guide.device_info,
                "action": self.click_device,
            },
            # firmware update
            {
                "label": i18n.Guide.firmware_update,
                "action": self.click_firmware,
            }
        ]
        #选项容器
        self.options_container = HStack(self.content)
        self.options_container.set_size(440,lv.SIZE.CONTENT)
        self.options_container.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.options_container.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container.set_style_radius(20, lv.PART.MAIN) #圆角16
        self.options_container.set_style_pad_left(20, lv.PART.MAIN) #设置左上角显示
        #设置上下行间距0
        self.options_container.set_style_pad_row(0, lv.PART.MAIN)
        for idx, g in enumerate(guides):
            label, action = g["label"], g["action"]
            app = Item(self.options_container, label)
            app.action = action
            # 在 firmware_update 后插入一个空的 item
            if label == i18n.Guide.firmware_update:
                spacer = lv.obj(self.content)
                spacer.set_height(10)
                spacer.set_width(lv.pct(100))
                spacer.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
                #去掉边框
                spacer.set_style_border_width(0, lv.PART.MAIN)
            else:
                if label != i18n.Guide.firmware_update:
                    # 添加底边灰色边框
                    app.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
                    app.set_style_border_width(2, lv.PART.MAIN)
                    app.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
                    app.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)

        guides2 = [
            # terms of use
            {
                "label": i18n.Guide.terms_of_use,
                "action": self.click_terms,
            },
            # download
            {
                "label": i18n.Title.download_app,
                "action": self.click_download,
            },
            # about
            {
                "label": i18n.Guide.about,
                "action": self.click_about,
            },
        ]
        #选项容器2
        self.options_container2 = HStack(self.content)
        self.options_container2.set_size(440,lv.SIZE.CONTENT)
        self.options_container2.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.options_container2.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.options_container2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container2.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container2.set_style_radius(20, lv.PART.MAIN) #圆角16
        self.options_container2.set_style_pad_left(20, lv.PART.MAIN) #设置左上角显示
        #设置上下行间距0
        self.options_container2.set_style_pad_row(0, lv.PART.MAIN)
        for idx, g in enumerate(guides2):
            label, action = g["label"], g["action"]
            app = Item(self.options_container2, label)
            app.action = action
            if label != i18n.Guide.about:
                # 添加底边灰色边框
                app.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
                app.set_style_border_width(2, lv.PART.MAIN)
                app.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
                app.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)

    def click_terms(self):
        log.debug(__name__, "click terms")
        from .terms import Terms
        workflow.spawn(Terms(i18n.Guide.terms_of_use).show())

    def click_download(self):
        log.debug(__name__, "click firmware")
        from .download import Download
        workflow.spawn(Download(i18n.Title.download_app).show())

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
            .bg_color(lv.color_hex(0x15151E))  # 深色背景
            .bg_opa(lv.OPA._90)  # 90% 不透明，避免影响子组件
            #字号28
            .text_font(font.Regular.SCS30)
            # .bg_opa(lv.OPA.COVER)
            .width(400)
            .height(72)
            .pad_right(32)
            .pad_row(0)
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
            #设置字号30
            self.label.set_style_text_font(font.Regular.SCS30, 0)
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
            #设置字号30
            self.label.set_style_text_font(font.Regular.SCS30, 0)
            self.add_flag(lv.obj.FLAG.CLICKABLE)
            # right-arrow
            # self.arrow = lv.label(self)
            # self.arrow.set_text(lv.SYMBOL.RIGHT)
            # self.arrow.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN) # type: ignore
            self.arrow = lv.img(self)
            self.arrow.set_width(21)
            self.arrow.set_height(32)
            #设置箭头背景图
            self.arrow.set_src("A:/res/a_right_arrow.png")

        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)

    def action(self):
        pass
class QrcodeDetail(Navigate):
    def __init__(self, title: str ,qrcode: str, icon: str):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.title.set_text(title)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style().pad_left(16).pad_right(16),
            0
        )
        #行间距20
        self.content.set_style_pad_row(10, 0)
        
        contaner = self.add(lv.obj)
        contaner.add_style(
            theme.Styles.container,
            0
        )
        contaner.set_height(230)
        contaner.clear_flag(lv.obj.FLAG.SCROLLABLE)
        #行间距10
        contaner.set_style_pad_row(10, 0)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)
        self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        #边框2
        # contaner.set_style_border_width(2, lv.PART.MAIN)
        # # qrcode
        # view = lv.qrcode(contaner, 440, colors.DS.BLACK, colors.DS.WHITE)
        # view.set_style_border_width(5, lv.PART.MAIN)
        # view.set_style_radius(25, lv.PART.MAIN)
        # view.update(qrcode, len(qrcode))
        # view.center()
        label0 = lv.label(contaner)
        label0.set_text(i18n.Title.go_link)
        label0.set_style_text_font(font.Regular.SCS26, 0)
        label0.add_style(Style()
                        .text_color(lv.color_hex(0xFFFFFF)),
                        0)
        #做边距20
        label0.add_style(Style().pad_left(40),0)
        label0.set_width(460)
        label0.set_height(100)

        label = lv.label(contaner)
        label.set_text(qrcode)
        label.set_style_text_font(font.Regular.SCS26, 0)
        label.add_style(Style()
                        .text_color(lv.color_hex(0xFFFFFF)),
                        0)
        #做边距20
        label.add_style(Style().pad_left(40),0)
        #上边距30
        label.add_style(Style().pad_top(30),0)
        label.set_width(460)
        #高度自适应
        label.set_height(100)
        label.set_long_mode(lv.label.LONG.WRAP)
        label.set_style_pad_row(10, 0)
        # 二维码容器（居中布局）
        self.qrcode_container = lv.obj(self)
        self.qrcode_container.set_size(400, 400)
        self.qrcode_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        # self.qrcode_container.align(lv.ALIGN.TOP_MID, 0, 100)  # 调整垂直位置
        #圆角24
        self.qrcode_container.set_style_radius(24, lv.PART.MAIN)
        self.qrcode_container.set_style_shadow_width(0, lv.PART.MAIN)
        self.qrcode_container.set_style_outline_width(0, lv.PART.MAIN)
        self.qrcode_container.align(lv.ALIGN.TOP_LEFT, 40, 180)  # 调整垂直位置
        self.qrcode_container.set_style_border_width(0, lv.PART.MAIN)
        
        view = lv.qrcode(self.qrcode_container, 312, colors.DS.BLACK, colors.DS.WHITE)
        view.set_style_border_width(24, lv.PART.MAIN)
        
        #去除二维码内部白边
        view.set_style_shadow_width(0, lv.PART.MAIN)
        view.set_style_outline_width(0, lv.PART.MAIN)
        view.set_style_radius(24, lv.PART.MAIN)
        view.set_style_border_color(lv.color_hex(0xffffff), lv.PART.MAIN)#边框颜色0x141419
        view.update(qrcode, len(qrcode))
        view.center()
        # 在二维码中心添加icon图片
        print("icon",icon)
        icon_img = lv.img(self.qrcode_container)
        icon_img.set_src(icon)
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
