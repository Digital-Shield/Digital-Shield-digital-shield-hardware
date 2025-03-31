import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from trezor.ui.screen import Navigation, with_title

if TYPE_CHECKING:
    from typing import List
    pass

class About(with_title(Navigation)):
    def __init__(self,title):
        super().__init__()
        self.set_title(title)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .pad_left(16)
            .pad_top(25)
            .pad_right(16),
            0
        )
        Item(self.content,'Digit Shield','A:/res/web.png',"https://digitshield.com")
        Item(self.content,'Twitter','A:/res/twitter.png',"https://x.com/DigitShield_HQ")
        Item(self.content,'Discord','A:/res/discord.png',"https://discord.gg/wH8HVsHz")
        Item(self.content,'Telegram','A:/res/telegram.png',"https://t.me/digitshield")

class Item(VStack):
    """
    Item with an icon and text
    """
    def __init__(self, parent, title, icon, url):
        super().__init__(parent)
        self.items_center()
        self.add_style(
            Style()
            .radius(16)
            .bg_color(lv.color_hex(0x111126))
            .bg_opa(lv.OPA._90)  # 90% 不透明，避免影响子组件
            .text_color(lv.color_hex(0xFFFFFF))
            # .bg_opa(lv.OPA.COVER)
            .width(lv.pct(100))
            .height(72)
            .pad_right(32)
            .pad_column(16),
            0,
        )
        #获取当前语言，判断阿拉伯语
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            # right-qc-code
            qr = lv.img(self)
            qr.set_src("A:/res/qr-code-two.png")
            qr.set_style_img_recolor(lv.color_white(), 0)

            self.label = lv.label(self)
            self.label.set_flex_grow(1)
            self.label.set_text(title)
            self.add_flag(lv.obj.FLAG.CLICKABLE)
            self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)
            self.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN)  # 设置右对齐
            # icon
            self.title = title
            self.url = url
            self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
            self.clear_flag(lv.obj.FLAG.SCROLLABLE)
            self.icon = lv.img(self)
            self.icon.set_src(icon)
        else:
            self.title = title
            self.url = url
            self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
            self.clear_flag(lv.obj.FLAG.SCROLLABLE)
            self.icon = lv.img(self)
            self.icon.set_src(icon)

            self.label = lv.label(self)
            self.label.set_flex_grow(1)
            self.label.set_text(title)
            self.add_flag(lv.obj.FLAG.CLICKABLE)
            self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)
            # self.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN)  # 设置右对齐
            # right-qc-code
            qr = lv.img(self)
            qr.set_src("A:/res/qr-code-two.png")
            qr.set_style_img_recolor(lv.color_white(), 0)
    def action(self):
        from trezor import workflow        
        workflow.spawn(QrcodeDetail(self.title,self.url).show())
