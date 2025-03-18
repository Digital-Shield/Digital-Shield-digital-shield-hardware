import lvgl as lv
from typing import Callable

from storage import device
from trezor import log, workflow, motor
from trezor.ui import i18n, events,font
from trezor.ui.theme import Styles
from trezor.ui.screen import Screen, Navigation, with_title
from trezor.ui.component import VStack, HStack
from trezor.ui.component import Swipedown

class Developing(with_title(Navigation)):
    """
    A placeholder for development
    """

    def __init__(self, title):
        super().__init__()
        self.set_title(title)

        img = lv.img(self.content)
        img.set_src("A:/res/logo.png")
        img.center()

        from trezor.ui.theme import Styles

        txt = lv.label(self.content)
        txt.set_text("developing ...")
        txt.add_style(Styles.subtitle, lv.PART.MAIN)
        txt.align(lv.ALIGN.BOTTOM_MID, 0, -128)


class HomeScreen(Screen):
    def __init__(self):
        super().__init__()
        self.set_style_pad_top(64, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        tip = lv.label(self)
        tip.set_text(i18n.Tip.swipe_down_to_close)
        tip.align(lv.ALIGN.TOP_MID, 0, -32)
        tip.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)# 设置文本颜色

        self.add_event_cb(self.on_swipe_down, events.SWIPEDOWN, None)
        self.add_event_cb

       # apps
        self.create_content(VStack)# 创建内容
        self.content : VStack# 设置内容为VStack
        self.content.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)# 设置排列方式
        self.content.set_style_flex_main_place(lv.FLEX_ALIGN.SPACE_EVENLY, lv.PART.MAIN)# 设置主轴排列方式
        self.content.set_style_pad_top(50, lv.PART.MAIN)  # 设置顶部填充
        self.content.set_style_pad_row(30, lv.PART.MAIN)  # 设置行间距
        self.content.align(lv.ALIGN.TOP_MID, 0, 0)# 设置位置


        apps = [
            # account
            {
                "label": i18n.App.account,
                "icon": "A:/res/app_account_six.png",
                "action": self.click_account,
            },
            # scan
            {
                "label": i18n.App.scan,
                "icon": "A:/res/app_scan_six.png",
                "action": self.click_scan,
            },
            # NFT
            {
                "label": i18n.App.nft,
                "icon": "A:/res/app_nft_six.png",
                "action": self.click_nft,
            },
            # security
            {
                "label": i18n.App.security,
                "icon": "A:/res/app_security_six.png",
                "action": self.click_security,
            },
            # guide
            {
                "label": i18n.App.guide,
                "icon": "A:/res/app_guide_six.png",
                "action": self.click_guide,
            },
            # setting
            {
                "label": i18n.App.setting,
                "icon": "A:/res/app_settings_six.png",
                "action": self.click_setting,
            },
        ]

        for a in apps:
            label, icon, action = a["label"], a["icon"], a["action"]
            app = Item(self.content, label, icon)
            app.on_click = action

    def on_swipe_down(self, event: lv.event_t):
        self.dismiss()

    def on_change_wallpaper(self, event):
        wallpaper = device.get_homescreen()
        self.set_style_bg_img_src(wallpaper, 0)

    def on_loaded(self):
        super().on_loaded()
        Swipedown.instance().enable()
    def on_unload_start(self):
        super().on_unload_start()
        Swipedown.instance().disable()

    def click_account(self, app: 'Item'):
        log.debug(__name__, "click account")
        motor.vibrate()#触摸振动
        from .account import AccountApp
        workflow.spawn(AccountApp().show())

    def click_scan(self, app: 'Item'):
        log.debug(__name__, "click scan")
        motor.vibrate()#触摸振动
        from .scan import ScanApp
        workflow.spawn(ScanApp().show())

    def click_nft(self, app: 'Item'):
        log.debug(__name__, "click nft")
        motor.vibrate()#触摸振动
        from .nft import NftApp
        workflow.spawn(NftApp().show())

    def click_security(self, app: 'Item'):
        log.debug(__name__, "click security")
        motor.vibrate()#触摸振动
        from .security import SecurityApp
        workflow.spawn(SecurityApp().show())

    def click_guide(self, app: 'Item'):
        log.debug(__name__, "click guide")
        motor.vibrate()#触摸振动
        from .guide import GuideApp
        workflow.spawn(GuideApp().show())

    def click_setting(self, app: 'Item'):
        motor.vibrate()#触摸振动
        from .setting import SettingApp
        workflow.spawn(SettingApp().show())

    async def show(self):
        from trezor.ui.screen import manager
        await manager.switch_scene(self)

    def dismiss(self):
        from apps.base import lock_device
        lock_device()

class Item(HStack):

    def __init__(self, parent, label: str, icon: str):
        super().__init__(parent)
        self.add_style(Styles.home_app, lv.PART.MAIN)
        self.add_style(Styles.pressed, lv.STATE.PRESSED)
        self.items_center()
        self.set_style_flex_main_place(lv.FLEX_ALIGN.SPACE_EVENLY, lv.PART.MAIN)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)  # 禁止拖拽

        self.set_style_pad_row(0, lv.PART.MAIN)  # 行间距
        self.set_style_pad_column(0, lv.PART.MAIN)

        img = lv.img(self)
        img.set_src(icon)
        img.set_zoom(230)
        img.clear_flag(lv.obj.FLAG.SCROLLABLE)  # 禁止拖拽
        
        title = lv.label(self)
        title.set_text(label)
        title.set_height(60)
        title.set_style_pad_top(12, lv.PART.MAIN)  # 调小此值，减少文字与图片之间的间距
        title.align(lv.ALIGN.OUT_BOTTOM_MID, 0, -2)  # 减小 y 轴偏移
        title.set_style_text_font(font.Bold.SCS26, lv.PART.MAIN)
        title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.on_click: Callable[["Item"], None] = None

        self.add_event_cb(self.__on_clicked, lv.EVENT.CLICKED, None)

    def __on_clicked(self, event: lv.event_t):
        if self.on_click:
            self.on_click(self)
