import lvgl as lv
from trezor import utils, workflow
from trezor.ui import i18n, colors, Style
from trezor.ui.component import VStack
from trezor.ui.screen.preview import Preview
from storage import device
from trezor.ui import display
from trezor.ui import font
from trezor.ui.component import HStack, VStack

class Brightness(Preview):
    def __init__(self):
        super().__init__()
        # 设置黑色背景
        self.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)
        
        # 顶部标题设置
        self.title.set_text(i18n.Title.screen_bright)
        self.title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.title.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
        
        # 隐藏不需要的按钮
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)

        # 主内容容器
        self.container = VStack(self.content)
        self.container.set_size(lv.pct(100), lv.pct(50))
        self.container.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        self.container.align(lv.ALIGN.TOP_LEFT, 0, 0)

        # 太阳图标
        self.sun_icon = lv.img(self.container)
        self.sun_icon.set_src("A:/res/sun_light.png")
        self.sun_icon.set_size(32, 32)
        self.sun_icon.set_style_img_opa(20, lv.PART.MAIN)
        self.sun_icon.set_style_pad_top(0, lv.PART.MAIN)

        # 百分比标签
        self.percent_label = lv.label(self.container)
        self.percent_label.set_style_text_font(font.Bold.SCS30, lv.PART.MAIN)
        self.percent_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.percent_label.set_style_pad_top(30, lv.PART.MAIN)
        self.percent_label.set_style_pad_bottom(40, lv.PART.MAIN)

        self.container2 = HStack(self.content)
        self.container2.set_size(lv.pct(100), lv.pct(50))
        self.container2.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        self.container2.align(lv.ALIGN.TOP_LEFT, 0, 160)

        # 垂直滑块容器
        self.slider_container = HStack(self.container2)
        self.slider_container.set_size(60, 200)
        self.slider_container.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)

        # 垂直滑块
        self.slider = lv.slider(self.slider_container)
        self.slider.set_size(60, 200)
        self.slider.set_range(20, 100)
        self.slider.set_value(device.get_brightness(), lv.ANIM.OFF)
        
        # 样式设置
        self.slider.set_style_radius(30, lv.PART.MAIN)
        self.slider.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.slider.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.INDICATOR)
        self.slider.set_style_bg_opa(255, lv.PART.INDICATOR)
        self.slider.set_style_pad_all(0, lv.PART.MAIN)

        # === 关键修改1: 确保INDICATOR占满 ===
        self.slider.set_style_height(200, lv.PART.INDICATOR)
        self.slider.set_style_align(lv.ALIGN.BOTTOM_MID, lv.PART.INDICATOR)
        self.slider.set_style_width(lv.pct(100), lv.PART.INDICATOR)
        
        # === 关键修改2: 修复圆角设置问题 ===
        # 使用单个值设置所有圆角（替代元组方式）
        self.slider.set_style_radius(0, lv.PART.INDICATOR)  # 重置所有圆角
        
        # === 关键修改3: 调整KNOB位置 ===
        self.slider.set_style_align(lv.ALIGN.TOP_MID, lv.PART.KNOB)
        
        # knob 样式
        self.slider.set_style_radius(15, lv.PART.KNOB)
        self.slider.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)
        self.slider.set_style_border_color(colors.DS.BLUE, lv.PART.KNOB)
        self.slider.set_style_size(16, lv.PART.KNOB)
        
        self.slider.add_event_cb(self.on_brightness_change, lv.EVENT.VALUE_CHANGED, None)
        
        # 初始化UI
        self.update_ui(device.get_brightness())

    def on_brightness_change(self, event):
        brightness = event.get_target().get_value()
        device.set_brightness(brightness)
        display.backlight(brightness)
        self.update_ui(brightness)
    
    def update_ui(self, brightness):
        display_value = 0 if brightness == 20 else brightness
        self.percent_label.set_text(f"{display_value}%")

        opacity = int(100 + (brightness * 1.55))
        self.sun_icon.set_style_img_opa(min(opacity, 255), lv.PART.MAIN)

        slider_height = 200
        fill_height = int(((brightness - 20) / 80) * slider_height)
        self.slider.set_style_height(fill_height, lv.PART.INDICATOR)

        min_radius = 5
        if fill_height >= slider_height:
            dynamic_radius = 0  # 满格时直角
        else:
            dynamic_radius = int(min(30, max(min_radius, fill_height / 2)))

        self.slider.set_style_radius(dynamic_radius, lv.PART.INDICATOR)
        self.slider.set_style_clip_corner(True, lv.PART.MAIN)
