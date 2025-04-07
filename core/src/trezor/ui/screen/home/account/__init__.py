import lvgl as lv

from typing import TYPE_CHECKING

from trezor import loop, workflow
from trezor.ui import i18n, Style, theme, colors,font
from trezor.ui.component import HStack, VStack, LabeledText
from trezor.ui.screen import Navigation
from .evm import EVM, ETH_CHAIN_ID,BSC_CHAIN_ID,MATIC_CHAIN_ID

__USE_BACKGROUND_IMAGE__ = False
class AccountApp(Navigation):
    def __init__(self):
        super().__init__()
        self.set_style_bg_img_src(None, lv.PART.MAIN)  # 取消背景图
        # self.set_style_bg_img_src("A:/res/background_six.png", lv.PART.MAIN)
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色
        # self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 设置背景颜色的透明度为完全不透明

        self.title.set_text(i18n.App.account)

        # use HStack as content
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)


        from .btcfork import BTCFork, BTC_COIN_NAME, LTC_COIN_NAME, DOGE_COIN_NAME
        # coin
        Coin(self.content, BTCFork(BTC_COIN_NAME))
        # coin
        Coin(self.content, BTCFork(LTC_COIN_NAME))
        # coin
        Coin(self.content, BTCFork(DOGE_COIN_NAME))

        # eth
        Coin(self.content, EVM(ETH_CHAIN_ID))

        # bsc
        Coin(self.content, EVM(BSC_CHAIN_ID))

        # matic
        Coin(self.content, EVM(MATIC_CHAIN_ID))

        # from .eos import Eos
        # Coin(self.content, Eos)

        from .solana import Solana
        Coin(self.content, Solana)

        # tron
        from .tron import Tron
        Coin(self.content, Tron)

        from .polkadot import Polkadot
        Coin(self.content, Polkadot)

        from .sui import Sui
        Coin(self.content, Sui)

        from .aptos import Aptos
        Coin(self.content, Aptos)


class Item(VStack):
    """
    Item with an icon and text
    """
    def __init__(self, parent, text, icon):
        super().__init__(parent)
        self.items_center()
        self.add_style(
            Style()
            .radius(16)
            .bg_opa(lv.OPA.COVER)
            .width(432) #lv.pct(100)
            .height(80)
            .pad_right(32)
            .pad_column(16)
            .bg_color(lv.color_hex(0x111126)),
            0,
        )
        self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)

        self.icon = lv.img(self)
        self.icon.set_src(icon)
        self.icon.set_zoom(128)

        self.label = lv.label(self)
        self.label.set_flex_grow(1)
        self.label.set_text(text)
        self.label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        # self.label.set_style_pad_all(28, lv.PART.MAIN)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        # right-arrow
        self.arrow = lv.label(self)
        self.arrow.set_text(lv.SYMBOL.RIGHT)
        self.arrow.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)
    def action(self):
        pass



if TYPE_CHECKING:
    from typing import List, Protocol, Type

    class CoinDetailView(Protocol):
        """A `Coin` which take a `path` as argument and show something."""

        def __init__(self): ...
        async def show(self): ...

        @staticmethod
        def get_name():
            """return name of the coin"""

        @staticmethod
        def get_icon():
            """return icon of the coin"""

class Coin(Item):
    def __init__(self, parent, detail_cls: Type[CoinDetailView]):
        super().__init__(parent, detail_cls.get_name(), detail_cls.get_icon())
        self.detail_cls = detail_cls

    def action(self):
        from trezor import workflow
        workflow.spawn(
            self.detail_cls().show()
        )

QRCODE_SIZE = 400
class DetailBase(Navigation):
    @staticmethod
    def get_name() -> str:
        raise NotImplementedError
    @staticmethod
    def get_icon() -> str:
        raise NotImplementedError

    @staticmethod
    def get_path() -> str:
        raise NotImplementedError

    @classmethod
    async def get_address(cls) -> str:
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self.set_style_bg_img_src(None, lv.PART.MAIN)  # 取消背景图
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色
        # self.set_style_bg_img_src("A:/res/coin_background.png", lv.PART.MAIN)
        # self.set_style_pad_bottom(20, lv.PART.MAIN)
        # background = lv.obj(self)
        # # background.set_style_bg_img_src("A:/res/coin_background.png", lv.PART.MAIN)
        # background.set_width(432)
        # background.set_height(708)
        # background.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)  # 设置背景颜色
        # # background.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN)  # 设置边框颜色为黑色
        # background.set_style_border_width(0, lv.PART.MAIN)  # 设置边框宽度为0
        # background.align(lv.ALIGN.TOP_MID, 0, 25)
        # # 将背景图移动到最底层
        # background.move_background()
        self.set_title(self.get_name())

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(Style().pad_left(16).pad_right(16), 0)

        # 二维码图片
        self.container = self.add(lv.obj)
        self.container.add_style(theme.Styles.container, 0)
        self.container.set_size(QRCODE_SIZE + 40, QRCODE_SIZE + 40)  # 增加容器的大小
        self.container.set_height(QRCODE_SIZE + 70)
        self.container.set_style_pad_bottom(30, lv.PART.MAIN)
        self._qrcode_view: lv.qrcode = None

        # address
        self.address_view = self.add(LabeledText)
        self.address_view.set_label(i18n.Text.address)
        self.address_view.set_text("")
        # self.address_view.set_style_align(lv.ALIGN.TOP_LEFT, lv.PART.MAIN)
        self.address_view.set_style_pad_top(0, lv.PART.MAIN)
        self.address_view.set_style_pad_left(20, lv.PART.MAIN)
        self.address_view.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        #self.address_view.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        # set_text later

        # path
        path_view = self.add(LabeledText)
        path_view.set_label(i18n.Text.path)
        path_view.set_text(self.get_path())
        path_view.set_style_pad_top(0, lv.PART.MAIN)
        path_view.set_style_pad_left(20, lv.PART.MAIN)
        path_view.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        path_view.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    def on_loaded(self):
        super().on_loaded()
        # default is `receive` address
        async def load_address():
            # wait a while, not block the UI
            await loop.sleep(300)
            await self.do_update_address()
        workflow.spawn(load_address())

    @property
    def qrcode_view(self) -> lv.qrcode:
        if self._qrcode_view:
            return self._qrcode_view
        self._qrcode_view = lv.qrcode(self.container, 380, colors.DS.BLACK, colors.DS.WHITE)
        self._qrcode_view.set_style_border_width(16, lv.PART.MAIN)
        self._qrcode_view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
        self._qrcode_view.set_style_radius(25, lv.PART.MAIN)
        self._qrcode_view.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)  # 添加这一行来设置背景颜色
        # self._qrcode_view.set_style_pad_all(20, lv.PART.MAIN)
        # self._qrcode_view.set_style_pad_bottom(20, lv.PART.MAIN)  # 设置下边距为20像素
        self._qrcode_view.center()
        return self._qrcode_view

    async def do_update_address(self):
        address = await self.get_address()
        self.qrcode_view.update(address, len(address))
        self.address_view.set_text(address)
        self.address_view.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


