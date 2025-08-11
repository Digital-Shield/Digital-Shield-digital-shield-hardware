from typing import TYPE_CHECKING
import lvgl as lv

from .helper import parser_path

from trezor import utils, workflow, loop, log
from trezor.ui import i18n, Style, theme, colors, font
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate
from trezor.ui.component import HStack, LabeledText

if TYPE_CHECKING:
    from typing import Literal, List
    from . import CoinProtocol, CoinConsturctor
    AddressState = Literal["receive", "airgap"]

QRCODE_SIZE = 320  # 缩小二维码尺寸

ETH_CHAIN_ID = 60
BSC_CHAIN_ID = 56
MATIC_CHAIN_ID = 137

name_map = {
    ETH_CHAIN_ID: "Ethereum",
    BSC_CHAIN_ID: "BNB Chain",
    MATIC_CHAIN_ID: "Polygon",
}

icon_map = {
    ETH_CHAIN_ID: "A:/res/evm-eth.png",
    BSC_CHAIN_ID: "A:/res/evm-bsc.png",
    MATIC_CHAIN_ID: "A:/res/evm-matic.png",
}

path_map = {
    ETH_CHAIN_ID: "m/44'/60'/0'/0/0",
    BSC_CHAIN_ID: "m/44'/60'/0'/0/0",
    MATIC_CHAIN_ID: "m/44'/60'/0'/0/0",
}

class EvmCoin:
    def __init__(self, chain_id: int):
        self.chain_id = chain_id
        
    def get_name(self) -> str:
        return name_map[self.chain_id]

    def get_icon(self) -> str:
        return icon_map[self.chain_id]

    def get_path(self) -> str:
        return path_map[self.chain_id]

    async def get_address(self) -> str:
        import_manager = utils.unimport()
        with import_manager:
            from trezor.wire import DUMMY_CONTEXT as ctx
            from apps.base import handle_Initialize
            from trezor.messages import Initialize, EthereumGetAddress
            from apps.ethereum.get_address import get_address

            init = Initialize(session_id=b"\x00")
            await handle_Initialize(ctx, init)

            req = EthereumGetAddress(address_n=parser_path(self.get_path()))
            resp = await get_address(ctx, req)
            return resp.address

    async def get_airgap_address(self) -> str:
        import_manager = utils.unimport()
        with import_manager:
            from trezor.wire import DUMMY_CONTEXT as ctx
            from apps.base import handle_Initialize
            from trezor.messages import Initialize, EthereumGetPublicKey
            from apps.ethereum.get_public_key import get_public_key

            init = Initialize(session_id=b"\x00")
            await handle_Initialize(ctx, init)

            address_n = parser_path(self.get_path())
            address_n = address_n[:3]
            req = EthereumGetPublicKey(address_n=address_n)
            resp = await get_public_key(ctx, req)

            address_n = address_n[:1]
            req = EthereumGetPublicKey(address_n=address_n)
            master_key = await get_public_key(ctx, req)

            from trezor.airgap.bc_types.coininfo import (
                CoinInfo,
                COIN_TYPE_ETH,
                NETWORK_MAINNET,
            )
            from trezor.airgap.bc_types.hdkey import HDKey
            from trezor.airgap.bc_types.keypath import KeyPath, PathComponent

            coin_info = CoinInfo(COIN_TYPE_ETH, NETWORK_MAINNET)
            key_data = resp.node.public_key
            chain_code = resp.node.chain_code
            source_fingerprint = resp.node.fingerprint
            paths = PathComponent.parser_path(self.get_path())
            origin = KeyPath(paths[:3], master_key.node.fingerprint, 3)
            children = KeyPath([paths[3], PathComponent()], depth=0)
            hdkey = HDKey.derived(
                key_data,
                chain_code=chain_code,
                origin=origin,
                parent_fingerprint=source_fingerprint,
                children=children,
                use_info=coin_info,
                name="Digitshield",
                note="eth.account.standard",
            )

            from trezor.airgap.ur.ur import UR
            from trezor.airgap.ur.ur_encoder import UREncoder
            ur = UR(hdkey.type(), hdkey.cbor())
            data = UREncoder.encode(ur)
            return data.upper()

class EvmCoinDetail(Navigate):
    def __init__(self, coin: "EvmCoin"):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        
        self.coin = coin
        self._receive_address = None
        self._airgap_address = None
        self.current_tab = "receive"
        self.show_qrcode = False  # 默认显示地址
        
        # 背景设置
        background = lv.obj(self)
        background.set_width(432)
        background.set_height(708)
        background.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)
        background.set_style_border_width(0, lv.PART.MAIN)
        background.align(lv.ALIGN.TOP_MID, 0, 45)
        background.move_background()

        self.title.set_text(self.coin.get_name())

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(Style().pad_left(16).pad_right(16), 0)

        # 顶部tab栏容器 - 只在二维码模式下显示
        self.tab_container = lv.obj(self)
        self.tab_container.set_size(432, 100)
        self.tab_container.align(lv.ALIGN.TOP_MID, 0, 70)
        self.tab_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.tab_container.set_style_border_width(0, lv.PART.MAIN)
        self.tab_container.add_flag(lv.obj.FLAG.HIDDEN)
        # 去掉右侧轮廓线
        self.tab_container.set_style_border_side(lv.BORDER_SIDE.RIGHT, 0)
        
        # 外部椭圆背景
        self.tab_bg = lv.obj(self.tab_container)
        self.tab_bg.set_size(330, 60)
        self.tab_bg.align(lv.ALIGN.CENTER, 0, 0)
        # self.tab_bg.set_style_bg_color(lv.color_hex(0x333344), lv.PART.MAIN)
        # self.tab_bg.set_style_border_width(2, lv.PART.MAIN)
        self.tab_bg.set_style_radius(30, lv.PART.MAIN)
        self.tab_bg.set_style_border_width(0, lv.PART.MAIN)  # 去掉轮廓线
        
        # 内部选中状态椭圆
        self.tab_active = lv.obj(self.tab_container)
        self.tab_active.set_size(180, 60)
        self.tab_active.align(lv.ALIGN.LEFT_MID, 30, 0)
        self.tab_active.set_style_bg_color(lv.color_hex(0x2A5CFF), lv.PART.MAIN)
        self.tab_active.set_style_radius(30, lv.PART.MAIN)
        self.tab_active.set_style_border_width(0, lv.PART.MAIN)
        
        # 地址tab按钮 - 可点击区域
        self.receive_tab_btn = lv.btn(self.tab_container)
        self.receive_tab_btn.set_size(180, 60)
        self.receive_tab_btn.align(lv.ALIGN.LEFT_MID, 32, 0)
        self.receive_tab_btn.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.receive_tab_btn.set_style_border_width(0, lv.PART.MAIN)
        self.receive_tab_btn.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.receive_tab_btn.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.receive_tab_btn.add_event_cb(lambda e: self.switch_tab("receive"), lv.EVENT.CLICKED, None)
        
        # AirGap tab按钮 - 可点击区域
        self.airgap_tab_btn = lv.btn(self.tab_container)
        self.airgap_tab_btn.set_size(180, 60)
        self.airgap_tab_btn.align(lv.ALIGN.RIGHT_MID, -32, 0)
        self.airgap_tab_btn.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.airgap_tab_btn.set_style_border_width(0, lv.PART.MAIN)
        self.airgap_tab_btn.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.airgap_tab_btn.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.airgap_tab_btn.add_event_cb(lambda e: self.switch_tab("airgap"), lv.EVENT.CLICKED, None)
        
        # 地址tab标签
        self.receive_tab_label = lv.label(self.tab_container)
        self.receive_tab_label.set_text(i18n.Text.address)
        self.receive_tab_label.align(lv.ALIGN.LEFT_MID,80, 0)
        self.receive_tab_label.set_style_border_width(0, lv.PART.MAIN)
        self.receive_tab_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        
        # AirGap tab标签
        self.airgap_tab_label = lv.label(self.tab_container)
        self.airgap_tab_label.set_text("AirGap")
        self.airgap_tab_label.align(lv.ALIGN.RIGHT_MID, -80, 0)
        self.airgap_tab_label.set_style_border_width(0, lv.PART.MAIN)
        self.airgap_tab_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)


        # 二维码容器
        self.qrcode_container = lv.obj(self)
        self.qrcode_container.set_size(400, 400)  # 去掉额外尺寸
        # self.qrcode_container.set_style_pad_bottom(30, lv.PART.MAIN)
        self.qrcode_container.align(lv.ALIGN.TOP_MID, 0, 170)  # 增加20px间距
        self.qrcode_container.add_flag(lv.obj.FLAG.HIDDEN)
        self.qrcode_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.qrcode_container.set_style_border_width(0, lv.PART.MAIN)  # 
         # 去掉右侧轮廓线
        self.qrcode_container.set_style_border_side(lv.BORDER_SIDE.RIGHT, 0)
        self._qrcode_view: lv.qrcode = None

        # 提示文本
        self.tip = lv.label(self)
        self.tip.set_width(450)
        self.tip.set_long_mode(lv.label.LONG.WRAP)
        self.tip.set_text(i18n.Title.receive_tips.format(self.coin.get_name()))
        self.tip.set_style_pad_top(50, lv.PART.MAIN)
        self.tip.set_style_pad_left(40, lv.PART.MAIN)
        self.tip.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.tip.align(lv.ALIGN.TOP_MID, 0, 520)  # 增加20px间距
        self.tip.add_flag(lv.obj.FLAG.HIDDEN)

        # 地址显示区域
        self.address_container = lv.obj(self)
        self.address_container.set_size(432, 400)
        self.address_container.align(lv.ALIGN.TOP_MID, 0, 100)
        self.address_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.address_container.set_style_border_width(0, lv.PART.MAIN)
        
        # 地址显示
        self.address_view = LabeledText(self.address_container)
        self.address_view.set_width(lv.pct(100))
        self.address_view.set_label(i18n.Text.address)
        self.address_view.set_text("")
        self.address_view.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        self.address_view.set_style_pad_bottom(30, lv.PART.MAIN)

       

        # 路径显示
        self.path_view = LabeledText(self.address_container)
        self.path_view.set_label(i18n.Text.path)
        self.path_view.set_text(self.coin.get_path())
        self.path_view.set_style_pad_top(80, lv.PART.MAIN)
        self.path_view.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        self.path_view.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.path_view.align(lv.ALIGN.TOP_MID, 0, 150)

        # 底部切换按钮
        self.toggle_btn = lv.btn(self)
        self.toggle_btn.set_size(440, 89)
        self.toggle_btn.align(lv.ALIGN.BOTTOM_MID, 0, -10)  # 向上移动10px
        self.toggle_btn.set_style_bg_color(lv.color_hex(0x2A5CFF), lv.PART.MAIN)
        self.toggle_btn.set_style_radius(80, lv.PART.MAIN)  # 椭圆角
        self.toggle_btn_label = lv.label(self.toggle_btn)
        self.toggle_btn_label.set_text(i18n.Button.qr_code)
        self.toggle_btn_label.center()
        self.toggle_btn.add_event_cb(self.toggle_display, lv.EVENT.CLICKED, None)

        # 默认显示地址
        self.update_display()

    def on_loaded(self):
        super().on_loaded()
        async def load_address():
            await loop.sleep(300)
            self._receive_address = await self.coin.get_address()
            print(f"Loaded receive address: {self._receive_address}")
            if self._receive_address:
                # 地址分段显示的spana容器
                self.spans = lv.spangroup(self.address_container)
                self.spans.set_width(lv.pct(100))
                self.spans.set_height(lv.SIZE.CONTENT)
                self.spans.set_mode(lv.SPAN_MODE.BREAK)
                self.spans.add_style(LabeledText.style, lv.PART.MAIN)
                # self.spans.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
                # self.spans.set_style_border_width(1, lv.PART.MAIN)
                self.spans.set_style_pad_top(50, lv.PART.MAIN)

                span = self.spans.new_span()
                span.set_text(self._receive_address[:4])
                span.style.set_text_font(font.Bold.SCS38)
                span.style.set_text_color(lv.color_hex(0x2A5CFF))
                span.style.set_text_letter_space(0)
                span.style.set_text_line_space(0)
                span.style.set_text_decor(0)
                span.style.set_text_align(lv.TEXT_ALIGN.LEFT)
                # span.style.set_text_break(0)  # 禁止换行会导致后续span不显示，建议去掉

                span = self.spans.new_span()
                span.set_text(self._receive_address[4:19])
                span.style.set_text_font(font.Bold.SCS38)
                span.style.set_text_color(lv.color_hex(0xFFFFFF))

                span = self.spans.new_span()
                span.set_text(self._receive_address[19:-4])
                span.style.set_text_font(font.Bold.SCS38)
                span.style.set_text_color(lv.color_hex(0xFFFFFF))

                span = self.spans.new_span()
                span.set_text(self._receive_address[-4:])
                span.style.set_text_font(font.Bold.SCS38)
                span.style.set_text_color(lv.color_hex(0x2A5CFF))
            if self.show_qrcode:
                self.qrcode_view.update(self._receive_address, len(self._receive_address))
        workflow.spawn(load_address())

    def toggle_display(self, e):
        self.show_qrcode = not self.show_qrcode
        self.update_display()
        
        # 更新按钮文本
        if self.show_qrcode:
            self.toggle_btn_label.set_text(i18n.Text.address)
            # 确保二维码已加载
            if self._receive_address and self.current_tab == "receive":
                self.qrcode_view.update(self._receive_address, len(self._receive_address))
            elif self._airgap_address and self.current_tab == "airgap":
                self.qrcode_view.update(self._airgap_address, len(self._airgap_address))
        else:
            self.toggle_btn_label.set_text(i18n.Button.qr_code)

    def update_display(self):
        if self.show_qrcode:
            # 显示二维码模式
            self.tab_container.clear_flag(lv.obj.FLAG.HIDDEN)
            self.qrcode_container.clear_flag(lv.obj.FLAG.HIDDEN)
            self.tip.clear_flag(lv.obj.FLAG.HIDDEN)
            self.address_container.add_flag(lv.obj.FLAG.HIDDEN)
            # self.receive_tab_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
            # self.airgap_tab_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        else:
            # 显示地址模式
            self.tab_container.add_flag(lv.obj.FLAG.HIDDEN)
            self.qrcode_container.add_flag(lv.obj.FLAG.HIDDEN)
            self.tip.add_flag(lv.obj.FLAG.HIDDEN)
            self.address_container.clear_flag(lv.obj.FLAG.HIDDEN)

    def switch_tab(self, tab: str):
        if self.current_tab == tab:
            return
            
        self.current_tab = tab
        
        # 更新tab按钮样式
        if tab == "receive":
            self.tab_active.align(lv.ALIGN.LEFT_MID, 30, 0)
            self.receive_tab_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
            self.airgap_tab_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
            self.tip.set_text(i18n.Title.receive_tips.format(self.coin.get_name()))
            if self._receive_address:
                self.qrcode_view.update(self._receive_address, len(self._receive_address))
            else:
                workflow.spawn(self.load_receive_address())
        else:
            self.tab_active.align(lv.ALIGN.RIGHT_MID, -30, 0)
            self.airgap_tab_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
            self.receive_tab_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
            self.tip.set_text(i18n.Title.receive_tips.format(self.coin.get_name()))
            if self._airgap_address:
                self.qrcode_view.update(self._airgap_address, len(self._airgap_address))
            else:
                workflow.spawn(self.load_airgap_address())

    async def load_receive_address(self):
        self._receive_address = await self.coin.get_address()
        if self.current_tab == "receive" and self.show_qrcode:
            self.qrcode_view.update(self._receive_address, len(self._receive_address))

    async def load_airgap_address(self):
        self._airgap_address = await self.coin.get_airgap_address()
        if self.current_tab == "airgap" and self.show_qrcode:
            self.qrcode_view.update(self._airgap_address, len(self._airgap_address))

    @property
    def qrcode_view(self) -> lv.qrcode:
        if self._qrcode_view:
            return self._qrcode_view
        self._qrcode_view = lv.qrcode(self.qrcode_container, QRCODE_SIZE, colors.DS.BLACK, colors.DS.WHITE)
        self._qrcode_view.set_style_border_width(16, lv.PART.MAIN)
        self._qrcode_view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
        self._qrcode_view.set_style_radius(25, lv.PART.MAIN)
        self._qrcode_view.set_style_bg_color(colors.DS.WHITE, lv.PART.MAIN)
        self._qrcode_view.set_style_shadow_width(0, lv.PART.MAIN)
        self._qrcode_view.set_style_outline_width(0, lv.PART.MAIN)

        # 在二维码中心添加icon图片
        icon_path = self.coin.get_icon()
        try:
            icon_img = lv.img(self.qrcode_container)
            icon_img.set_src(icon_path)
            # 保证图片完整显示
            icon_img.set_zoom(200)  # 1.0倍缩放，防止裁剪
            icon_img.set_style_img_opa(lv.OPA.COVER, 0)
            icon_img.set_style_img_recolor_opa(lv.OPA.TRANSP, 0)
            icon_img.set_style_clip_corner(0, 0)
            # 添加白色四方形背景容器
            bg_container = lv.obj(self.qrcode_container)
            bg_container.set_size(80, 80)
            bg_container.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
            bg_container.set_style_radius(0, lv.PART.MAIN)  # 四方形，无圆角
            bg_container.set_style_border_width(0, lv.PART.MAIN)
            bg_container.set_style_border_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 彻底隐藏边框
            bg_container.set_style_shadow_width(0, lv.PART.MAIN)
            bg_container.align_to(self._qrcode_view, lv.ALIGN.CENTER, 0, 0)
            bg_container.move_foreground()

            # 将icon图片放到背景容器上方并居中
            icon_img.align_to(bg_container, lv.ALIGN.CENTER, 0, 0)
            icon_img.move_foreground()
            # 居中到二维码中心
            icon_img.align_to(self._qrcode_view, lv.ALIGN.CENTER, 0, 0)
            # 置于二维码之上
            icon_img.move_foreground()
            self._qrcode_icon = icon_img
        except Exception as e:
            log.error(f"Failed to load icon for QRCode: {e}")

        self._qrcode_view.center()
        return self._qrcode_view

def evm_coin(chain_id: int) -> CoinConsturctor:
    return lambda: EvmCoin(chain_id)