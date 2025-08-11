import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate

if TYPE_CHECKING:
    from typing import List
    pass

class About(Navigate):
    def __init__(self,title):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.title.set_text(title)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .pad_left(16)
            .pad_top(25)
            .pad_right(16),
            0
        )
        #行间距0
        self.content.set_style_pad_row(0, lv.PART.MAIN)
        Item(self.content,i18n.Title.official_website,'A:/res/dunan.png',"https://ds.pro")
        Item(self.content,'X','A:/res/twitter.png',"https://x.com/DigitShield_HQ")
        Item(self.content,'Discord','A:/res/discord.png',"https://discord.gg/digitshield")
        Item(self.content,'Telegram','A:/res/telegram.png',"https://t.me/digitshield")
        Item(self.content,'Medium','A:/res/instagram.png',"https://medium.com/@service_280")
        Item(self.content,'Facebook','A:/res/facebook.png',"https://www.facebook.com/profile.php?id=61571313262914")
        # Item(self.content,'Youtube','A:/res/youtube.png',"https://www.youtube.com/@DigitalShield-s6j")
class Item(VStack):
    """
    Item with an icon and text
    """
    def __init__(self, parent, title, icon_path, url):
        super().__init__(parent)
        self.items_center()
        self.add_style(
            Style()
            .radius(16)
            .bg_color(lv.color_hex(0x0D0E17))
            .bg_opa(lv.OPA._90)  # 90% 不透明，避免影响子组件
            .text_color(lv.color_hex(0xFFFFFF))
            # .bg_opa(lv.OPA.COVER)
            .width(440)
            .height(93)
            .pad_right(32)
            .pad_column(16),
            0,
        )
        
        self.title = title
        self.url = url
        self.icon_path = icon_path  # 保存图片地址
         # 添加底边灰色边框
        self.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        self.set_style_border_width(2, lv.PART.MAIN)
        self.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
        self.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)
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
            
            self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
            self.clear_flag(lv.obj.FLAG.SCROLLABLE)
            self.icon = lv.img(self)
            self.icon.set_src(icon_path)
            # arrow
            self.arrow = lv.img(self)
            self.arrow.set_width(21)
            self.arrow.set_height(32)
            #设置箭头背景图
            self.arrow.set_src("A:/res/a_right_arrow.png")
        else:
            self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
            self.clear_flag(lv.obj.FLAG.SCROLLABLE)
            self.icon = lv.img(self)
            self.icon.set_src(icon_path)

            self.label = lv.label(self)
            self.label.set_flex_grow(1)
            self.label.set_text(title)
            self.add_flag(lv.obj.FLAG.CLICKABLE)
            self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)
            # self.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN)  # 设置右对齐
            # right-qc-code
            # qr = lv.img(self)
            # qr.set_src("A:/res/qr-code-two.png")
            # qr.set_style_img_recolor(lv.color_white(), 0)
            # arrow
            self.arrow = lv.img(self)
            self.arrow.set_width(21)
            self.arrow.set_height(32)
            #设置箭头背景图
            self.arrow.set_src("A:/res/a_right_arrow.png")
    def action(self):
        from trezor import workflow
        # self.icon 在这里是 lv.img 对象，不是图片地址
        # 你应该传递图片地址（即 self.icon 的原始值），而不是 lv.img 对象
        # 可以在 __init__ 里用 self.icon_path 保存图片地址
        workflow.spawn(QrcodeDetail(self.title, self.url, self.icon_path).show())
