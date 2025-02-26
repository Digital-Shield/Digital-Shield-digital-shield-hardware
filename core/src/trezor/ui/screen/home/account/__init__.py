import lvgl as lv

from typing import TYPE_CHECKING

from trezor import loop, workflow
from trezor.ui import i18n, Style, theme, colors
from trezor.ui.component import HStack, VStack, LabeledText
from trezor.ui.screen import Navigation, with_title

class AccountApp(with_title(Navigation)):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.App.account)
        # use HStack as content
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)

        # coin
        from .bitcion import Bitcoin
        Coin(self.content, Bitcoin)

        from .ethereum import Ethereum
        Coin(self.content, Ethereum)

        from .eos import Eos
        Coin(self.content, Eos)

        from .solana import Solana
        Coin(self.content, Solana)


        from .tron import Tron
        Coin(self.content, Tron)

        # Coin(self.content,'BTC','A:/res/btc-btc.png',"44'/0'/0'/0/0")
        # Coin(self.content,'LTC','A:/res/btc-ltc.png',"44'/0'/0'/0/0")
        # Coin(self.content,'DOGE','A:/res/btc-doge.png',"44'/0'/0'/0/0")

        # Coin(self.content,'ETH','A:/res/evm-bnb.png',"44'/60'/0'/0/0", Ethereum)
        # Coin(self.content,'BSC','A:/res/evm-eth.png',"44'/0'/0'/0/0")
        # Coin(self.content,'POLYGON','A:/res/evm-matic.png',"44'/0'/0'/0/0")
        # Coin(self.content,'TRX','A:/res/chain-tron.png',"44'/0'/0'/0/0")

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
            .width(lv.pct(100))
            .height(72)
            .pad_right(32)
            .pad_column(16),
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
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        # right-arrow
        self.arrow = lv.label(self)
        self.arrow.set_text(lv.SYMBOL.RIGHT)
        self.arrow.set_style_text_color(colors.DS.GRAY, lv.PART.MAIN)

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
class DetailBase(with_title(Navigation)):
    @staticmethod
    def get_name() -> str:
        raise NotImplementedError
    @staticmethod
    def get_icon() -> str:
        raise NotImplementedError

    @staticmethod
    def get_path() -> str:
        raise NotImplementedError

    @staticmethod
    async def get_address() -> str:
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self.set_title(self.get_name())

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(Style().pad_left(16).pad_right(16), 0)

        # qr code
        self.container = self.add(lv.obj)
        self.container.add_style(theme.Styles.container, 0)
        self.container.set_height(QRCODE_SIZE + 32)
        self._qrcode_view: lv.qrcode = None

        # address
        self.address_view = self.add(LabeledText)
        self.address_view.set_label(i18n.Text.address)
        self.address_view.set_text("")
        # set_text later

        # path
        path_view = self.add(LabeledText)
        path_view.set_label(i18n.Text.path)
        path_view.set_text(self.get_path())

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
        self._qrcode_view = lv.qrcode(self.container, 400, colors.DS.BLACK, colors.DS.WHITE)
        self._qrcode_view.set_style_border_width(16, lv.PART.MAIN)
        self._qrcode_view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
        self._qrcode_view.center()
        return self._qrcode_view

    async def do_update_address(self):
        address = await self.get_address()
        self.qrcode_view.update(address, len(address))
        self.address_view.set_text(address)


