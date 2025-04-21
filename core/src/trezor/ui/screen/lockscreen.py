import lvgl as lv

from . import Screen
from storage import device
from trezor import log, ui, utils
from trezor.ui import i18n
from trezor.ui.component.container import HStack

class LockScreen(Screen):
    def __init__(self):
        super().__init__()

        wallpaper = device.get_homescreen()
        # self.set_style_bg_img_src(wallpaper, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色
        self.create_content(HStack)
        # manually type annotation
        self.content: HStack

        self.content.items_center()
        # items space equally
        self.content.set_style_flex_main_place(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.PART.MAIN)

        self.content.set_style_pad_top(32, lv.PART.MAIN)
        self.content.set_style_pad_bottom(32, lv.PART.MAIN)

        # lock icon
        icon = lv.img(self.content)
        icon.set_src("A:/res/lock_two.png")

        # logo icon
        logo = lv.img(self.content)
        logo.set_src("A:/res/logo_two.png")

        # tip
        tip = lv.label(self.content)
        tip.set_text(i18n.Text.tap_to_unlock)
        tip.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            tip.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置显示方向为从右向左
        self.add_event_cb(self.on_click, lv.EVENT.CLICKED, None)


    def on_click(self, e):
        if not ui.display.backlight() and not device.is_tap_awake_enabled():
            return
        if utils.turn_on_lcd_if_possible():
            return
        from trezor import workflow
        from apps.base import unlock_device

        workflow.spawn(unlock_device())

    async def show(self):
        from . import manager
        # as the first screen when the device is booted, it should be a scene, switch it
        await manager.switch_scene(self)
