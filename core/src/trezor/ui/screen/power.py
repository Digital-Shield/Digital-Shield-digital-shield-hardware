import lvgl as lv

from . import Modal
from trezor import utils, workflow
from trezor.ui import i18n, colors, Style, theme, font
from trezor.ui.component import HStack
from trezor.ui.screen.confirm import Confirm
from trezor.ui.screen.message import Message

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable
    pass

class PowerOff(Confirm):
    def __init__(self):
        super().__init__()
        # self.set_title(i18n.Title.power_off)
        self.btn_cancel.set_text(i18n.Button.cancel)
        self.btn_cancel.set_style_width(214, lv.PART.MAIN)
        self.btn_cancel.set_style_height(89, lv.PART.MAIN)
        # btn_cancel替换为一张图片显示，具有和它一样的事件功能
        self.btn_cancel.set_style_bg_img_src("A:/res/close_btn.png", lv.PART.MAIN)
        #需要将btn_cancel设置透明，图片才能显示出来
        self.btn_cancel.set_text("")
        self.btn_cancel.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.btn_confirm.set_text(i18n.Button.power_off)
        self.btn_confirm.color(colors.DS.DANGER)
        #滑块关机效果
        # 先隐藏确认键，滑块到头直接执行确认
        self.btn_confirm.add_state(lv.STATE.DISABLED)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_style_pad_left(16, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)

        # 替换为滑动滑块确认
        self.slider = self.add(lv.slider)
        # self.slider.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.KNOB)
        # self.slider.set_style_bg_img_src("A:/res/instagram.png",lv.PART.MAIN)
        self.slider.set_width(260)
        self.slider.set_height(66)
        self.slider.set_range(0, 280)
        self.slider.set_value(0, lv.ANIM.OFF)
        self.slider.set_pos(100, 60)  # 距离左边100px，距离上方60px（可根据实际UI调整）
        # 设置滑动条背景为灰色
        self.slider.add_style(Style().bg_color(colors.DS.GRAY).radius(60), lv.PART.MAIN)
        # 设置滑块为白色
        self.slider.add_style(Style().bg_color(colors.DS.WHITE).radius(60), lv.PART.KNOB)
        self.slider.add_style(Style().bg_img_src("A:/res/wipe_button.png"), lv.PART.KNOB)
        #滑过的轨道的颜色设置蓝色
        self.slider.add_style(Style().bg_color(lv.color_hex(0x0062CE)).radius(60), lv.PART.INDICATOR)
        # 新增：松开时如果没滑到头就回弹
        def on_slider_released(event):
            slider = event.get_target()
            value = slider.get_value()
            def update_confirm(timer):
                timer._del()
                # 滑到头，触发确认按钮的回调
                lv.event_send(self.btn_confirm, lv.EVENT.CLICKED, None)
            if value >= 260:
                if value >= 200:
                    #改变slider背景图片
                    print("改变slider背景图片")
                    self.slider.set_style_bg_img_src("A:/res/wipe_button_ok.png", lv.PART.KNOB)
                    #暂停1秒
                self._timer = lv.timer_create(update_confirm, 500, None)
            else:
                slider.set_value(0, lv.ANIM.ON)
                self.slider_label.set_style_text_opa(255, lv.PART.MAIN)
                
        self.slider.add_event_cb(on_slider_released, lv.EVENT.RELEASED, None)
        # 添加提示滑动关机文本
        self.slider_label = lv.label(self.slider)
        self.slider_label.set_width(260)
        self.slider_label.set_text(i18n.Button.hold_to_power_off)
        #居中显示
        self.slider_label.set_style_pad_left(60, lv.PART.MAIN)
        #超出滑块轨道则向左滚动显示
        self.slider_label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)  # 启用循环滚动模式
        self.slider_label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)  # 滚动条自适应
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            self.slider_label.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置显示方向为向右
        else:
            self.slider_label.set_style_base_dir(lv.BASE_DIR.LTR, 0)  # 设置滚动方向为向左

        self.slider_label.add_style(
            Style().bg_color(colors.DS.GRAY).radius(60).text_color(lv.color_hex(0xFFFFFF)),
            lv.PART.MAIN
        )
        self.slider_label.add_style(Style().text_opa(255), lv.PART.MAIN)
        def on_slider_value_changed(event):
            slider = event.get_target()
            value = slider.get_value()
            opa = max(0, 255 - round(value / 230) * 255)  # 计算不透明度，使文本在滑动块向右滑动时淡出
            self.slider_label.set_style_text_opa(opa, lv.PART.MAIN)

        self.slider.add_event_cb(on_slider_value_changed, lv.EVENT.VALUE_CHANGED, None)
        # 滑块弹回后文字淡入
        def on_slider_anim_end(event):
            slider = event.get_target()
            if slider.get_value() == 0:
                self.slider_label.set_style_text_opa(255, lv.PART.MAIN)

        self.slider.add_event_cb(on_slider_anim_end, lv.EVENT.VALUE_CHANGED, None)
        self.slider_label.center()

    def on_click_confirm(self):
        # no need close self, so we not call super
        screen = ShutingDown()
        workflow.spawn(screen.show())

    def on_click_cancel(self):
        super().on_click_cancel()

class Restart(Confirm):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.restart)
        self.btn_confirm.set_text(i18n.Button.restart)
        self.btn_confirm.color(colors.DS.DANGER)

    def on_click_confirm(self):
        # no need close self, so we not call super
        screen = Restarting()
        workflow.spawn(screen.show())

class ShutingDown(Modal):
    def __init__(self):
        super().__init__()

        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)  # 设置背景颜色
        
        self.create_content(HStack)
        self.content: HStack
        self.content.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        self.content.items_center()
        self.content.center()

        # self.add(lv.img).set_src("A:/res/logo_two.png")
        # self.add(lv.label).set_text(i18n.Text.shutting_down)
        # 添加文本并设置颜色
        label = self.add(lv.label)
        label.set_text(i18n.Text.shutting_down)
         #label并不显示在垂直的中央，向下偏移300高度
        # label.set_style_pad_top(300, lv.PART.MAIN)
        #设置居中
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

        async def shutdown_delay():
            from trezor import loop
            await loop.sleep(1500)
            utils.power_off()

        from trezor import workflow
        workflow.spawn(shutdown_delay())

    async def show(self):
        from trezor.ui.screen import manager
        await manager.replace(self)

class Restarting(Modal):
    def __init__(self):
        super().__init__()

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack

        self.content.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        self.content.items_center()
        self.content.center()

        self.add(lv.img).set_src("A:/res/logo_two.png")
        # self.add(lv.label).set_text(i18n.Text.restarting)
        # 添加文本并设置颜色
        label = self.add(lv.label)
        label.set_text(i18n.Text.restarting)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

        async def restart_delay():
            from trezor import loop
            await loop.sleep(1500)
            utils.reset()

        from trezor import workflow
        workflow.spawn(restart_delay())

    async def show(self):
        from trezor.ui.screen import manager
        await manager.replace(self)



class LowPower(Confirm):
    on_confirm: Callable[[], None]|None

    def __init__(self, charge):
        msg = i18n.Text.low_power_message.format(charge)
        super().__init__()
        # self.on_confirm = None
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_right.set_text(i18n.Button.confirm)
        self.btn_right.set_style_width(440, lv.PART.MAIN)
        self.btn_right.set_style_height(107, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
        self.icon = self.add(lv.img)
        self.icon.set_src("A:/res/battery_lower.png")
        self.icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        # 使用绝对定位到左上角
        self.icon.align(lv.ALIGN.TOP_LEFT, 40, 0)
        self.icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
        self.icon.set_zoom(256)  # 1.0x zoom, ensures full image is shown
        self.icon.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.icon.set_style_clip_corner(False, lv.PART.MAIN)
        
         # 容器（重新设计布局）
        self.a_container = lv.obj(self)
        self.a_container.set_size(436, 400)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align_to(self.icon,lv.ALIGN.TOP_LEFT, 0, 130)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(i18n.Title.low_power)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        # self.text1.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        # self.text1.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(msg)
        #行间距10
        self.text2.set_style_text_line_space(10, 0)
        self.text2.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)
        self.text2.set_style_text_color(colors.DS.WHITE, 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 60)

    def update_charge(self, charge: int):
        msg = i18n.Text.low_power_message.format(charge)
        self.text.set_text(msg)

    def on_click_ok(self):
        super().on_click_ok()
        if self.on_confirm:
            self.on_confirm()
