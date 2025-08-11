import lvgl as lv
from storage import device
from trezor.ui import i18n, font, Done, colors
from trezor.ui.screen import Modal
from trezor.ui.component import HStack, VStack

class BluetoothPairing(Modal):
    def __init__(self, code: str):
        super().__init__()
        # self.set_title(i18n.Title.bluetooth_pairing)
        self.btn_right.set_text(i18n.Button.done)
        self.btn_right.set_style_width(440, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
        self.create_content(HStack)
        # type annotation
        self.content: HStack

        # self.content.set_height(lv.SIZE.CONTENT)
        # self.content.set_style_pad_column(32, 0)
        # self.content.items_center()
        # self.content.center()
        
        
        # icon
        # img = self.add(lv.img)
        # img.set_src("A:/res/bluetooth-pairing-new.png")
        self.icon = self.add(lv.img)
        self.icon.set_src("A:/res/bluetooth-pairing-new.png")
        self.icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        # 使用绝对定位到左上角
        # self.icon.align(lv.ALIGN.TOP_LEFT, 40, 0)
        self.icon.set_style_pad_left(40, lv.PART.MAIN)
        self.icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
        self.icon.set_zoom(256)  # 1.0x zoom, ensures full image is shown
        self.icon.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.icon.set_style_clip_corner(False, lv.PART.MAIN)
          # 容器（重新设计布局）
        self.a_container = lv.obj(self)
        self.a_container.set_size(460, 400)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_pad_left(40, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 120)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(400)
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(i18n.Title.bluetooth_pairing)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)

        # self.show_area = lv.label(self.a_container)
        # self.show_area.set_size(440, 80)
        # self.show_area.align(lv.ALIGN.TOP_LEFT, 10,0)
        
        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(i18n.Text.bluetooth_pair)
        self.text2.set_style_text_line_space(10, lv.PART.MAIN)
        self.text2.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)
        self.text2.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 60)
        # # tips
        # label = self.add(lv.label)
        # label.set_width(lv.pct(100))
        # label.set_text(i18n.Text.bluetooth_pair)
        # label.set_style_text_font(font.Bold.SCS26, 0)
        # label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        # # label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # label.set_long_mode(lv.label.LONG.WRAP)

        # code
        label = lv.label(self.a_container)
        label.set_text(code)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        label.align_to(self.text2,lv.TEXT_ALIGN.LEFT, 0, 40)

        self.btn_right.add_event_cb(lambda _: self.close(Done()), lv.EVENT.CLICKED, None)
