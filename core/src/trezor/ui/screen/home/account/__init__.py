import lvgl as lv
from typing import TYPE_CHECKING

from trezor import loop, workflow
from trezor.ui import i18n, Style, theme, colors,font
from trezor.ui.component import HStack, VStack, LabeledText
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate

if TYPE_CHECKING:
    from typing import List, Protocol, Tuple
    from typing import Callable

    class CoinProtocol(Protocol):
        def get_name() -> str:
            ...

        def get_icon() -> str:
            ...

        def get_path() -> str:
            ...

        async def get_address() -> str:
            ...

    class CoinDetailViewProtocol(Protocol, Navigation):
        coin: CoinProtocol
        pass

    CoinConsturctor = Callable[[], CoinProtocol]
    CoinDetailViewConstructor = Callable[[CoinProtocol], CoinDetailViewProtocol]

class AccountApp(Navigate):
    def __init__(self):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        #设置标题
        self.title.set_text(i18n.Title.select_network)
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)
        # self.title.set_text(i18n.App.account)

        # 分页参数
        self.current_page = 0
        self.items_per_page = 6  # 每页显示5个条目
        self.coins_item = []  # 存储所有Coin实例

        # 初始化UI
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.content.set_style_pad_row(4, lv.PART.MAIN)  # 设置条目间距为8像素，可调整
        self.content.set_style_pad_top(10, lv.PART.MAIN)  # 设置内容距离屏幕顶部为68

        # 初始化所有币种
        self.init_coins()
        self.setup_pagination()
        self.render_page()

    def on_nav_backs(self, event):
        from trezor.ui import NavigationBack

        # should notify caller
        self.channel.publish(NavigationBack())
        from ... import manager
        from trezor import workflow

        workflow.spawn(manager.pop(self))
    def init_coins(self):
        from .btcfork import btcfork, BTC_COIN_NAME, LTC_COIN_NAME, DOGE_COIN_NAME
        from .evm import evm_coin, ETH_CHAIN_ID, BSC_CHAIN_ID, MATIC_CHAIN_ID, EvmCoinDetail
        from .solana import Solana
        from .ton import Ton
        from .tron import Tron
        from .polkadot import Polkadot
        from .sui import Sui
        from .aptos import Aptos

        coins: List[Tuple[CoinConsturctor, CoinDetailViewConstructor]] = [
            # btc fork coins
            (btcfork(BTC_COIN_NAME), CoinDetail),
            (btcfork(LTC_COIN_NAME), CoinDetail),
            (btcfork(DOGE_COIN_NAME), CoinDetail),
            # EVM based coins
            (evm_coin(ETH_CHAIN_ID), EvmCoinDetail),
            (evm_coin(BSC_CHAIN_ID), EvmCoinDetail),
            (evm_coin(MATIC_CHAIN_ID), EvmCoinDetail),
            # solana
            (Solana, CoinDetail),
            # ton
            (Ton, CoinDetail),
            # tron
            (Tron, CoinDetail),
            # polkadot
            (Polkadot, CoinDetail),
            # sui
            (Sui, CoinDetail),
            # aptos
            (Aptos, CoinDetail),
        ]
        # 容器（重新设计布局）
        self.a_container = lv.obj(self.content)
        self.a_container.set_size(440, lv.SIZE.CONTENT)
        self.a_container.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        #设置背景色
        self.a_container.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.a_container.set_style_pad_left(20, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 0)

         # 选项
        self.options_container = HStack(self.a_container)
        self.options_container.set_size(440, lv.SIZE.CONTENT)
        self.options_container.set_style_bg_color(lv.color_hex(0x15151E), lv.PART.MAIN)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container.set_style_radius(20, lv.PART.MAIN)#圆角20
        self.options_container.set_width(lv.pct(100))
        self.options_container.align(lv.ALIGN.TOP_LEFT, -8, 0)
        self.options_container.set_style_border_width(0, lv.PART.MAIN)
        self.options_container.set_style_pad_left(10, lv.PART.MAIN)#设置左上角显示
        #设置行间距0
        self.options_container.set_style_pad_row(15, lv.PART.MAIN)

        for (coin_constructor, detail_constructor) in coins:
            print("init coin: ")
            coin = coin_constructor()
            app = Coin(self.options_container, coin, detail_constructor)
            self.coins_item.append(app)

    def setup_pagination(self):
        """重构分页导航布局（适配图片中的UI样式）"""
        # 1. 创建底部导航容器（透明背景）
        self.nav_bar = lv.obj(self)
        self.nav_bar.set_size(450, 90)  # 与屏幕同宽
        self.nav_bar.align(lv.ALIGN.BOTTOM_MID, 0, -20)  # 贴底对齐

        # 设置导航栏样式为完全透明
        self.nav_bar.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.nav_bar.set_style_border_width(0, lv.PART.MAIN)
        self.nav_bar.set_style_outline_width(0, lv.PART.MAIN)
        self.nav_bar.set_style_shadow_width(0, lv.PART.MAIN)
        self.nav_bar.set_style_pad_all(0, lv.PART.MAIN)

        # 2. 直接在导航栏中创建两个按钮，使用精确的定位
        BUTTON_WIDTH = 204
        BUTTON_HEIGHT = 64
        BUTTON_SPACING = 24
        TOTAL_WIDTH = BUTTON_WIDTH * 2 + BUTTON_SPACING

        # 计算起始X坐标，使按钮组居中
        start_x = (432 - TOTAL_WIDTH) // 2

        # 3. 左箭头按钮
        self.left_btn = lv.btn(self.nav_bar)
        self.left_btn.set_size(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.left_btn.set_pos(start_x, 0)  # 使用绝对定位

        # 设置左按钮样式
        self.left_btn.set_style_radius(32, lv.PART.MAIN)  # 完全椭圆
        self.left_btn.set_style_border_width(0, lv.PART.MAIN)
        self.left_btn.set_style_outline_width(0, lv.PART.MAIN)
        self.left_btn.set_style_shadow_width(0, lv.PART.MAIN)
        self.left_btn.set_style_pad_all(0, lv.PART.MAIN)
        self.left_btn.set_style_width(212, lv.PART.MAIN)#新宽高
        self.left_btn.set_style_height(85, lv.PART.MAIN)
        #全透明
        self.left_btn.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        # self.left_btn.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色

        # 添加左箭头图标
        self.left_arrow = lv.img(self.left_btn)
        self.left_arrow.set_src("A:/res/prev_gray_btn.png")
        self.left_arrow.center()

        # 添加点击事件
        self.left_btn.add_event_cb(lambda e: self.prev_page(), lv.EVENT.CLICKED, None)

        # 4. 右箭头按钮
        self.right_btn = lv.btn(self.nav_bar)
        self.right_btn.set_size(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.right_btn.set_pos(start_x + BUTTON_WIDTH + BUTTON_SPACING, 0)  # 使用绝对定位

        # 设置右按钮样式
        # self.right_btn.set_style_bg_color(lv.color_hex(0x2A5CFF), lv.PART.MAIN)
        self.right_btn.set_style_radius(100, lv.PART.MAIN)
        self.right_btn.set_style_border_width(0, lv.PART.MAIN)
        self.right_btn.set_style_outline_width(0, lv.PART.MAIN)
        self.right_btn.set_style_shadow_width(0, lv.PART.MAIN)
        self.right_btn.set_style_pad_all(0, lv.PART.MAIN)
        self.right_btn.set_style_width(212, lv.PART.MAIN)
        self.right_btn.set_style_height(85, lv.PART.MAIN)
        # self.right_btn.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
        #全透明
        self.right_btn.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)

        # 添加右箭头图标
        # right_arrow = lv.label(self.right_btn)
        # right_arrow.set_text(lv.SYMBOL.RIGHT)
        # right_arrow.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.right_arrow = lv.img(self.right_btn)
        self.right_arrow.set_src("A:/res/next_blue_btn.png")
        self.right_arrow.center()

        # 添加点击事件
        self.right_btn.add_event_cb(lambda e: self.next_page(), lv.EVENT.CLICKED, None)

        # # 页面指示器
        # self.page_indicator = lv.label(self)
        # self.page_indicator.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        # self.page_indicator.align(lv.ALIGN.TOP_MID, 0, 0)
        # 5. 调试输出
        # print(f"按钮位置计算 - 左按钮X: {start_x}, 右按钮X: {start_x + BUTTON_WIDTH + BUTTON_SPACING}")
        # print(f"总宽度: {TOTAL_WIDTH}, 屏幕宽度: 432, 边距: {(432 - TOTAL_WIDTH) // 2}")

    def prev_page(self):
        """切换到上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()
            # 可以添加滑动动画效果[1](@ref)
            # lv_scr_load_anim(self.content, LV_SCR_LOAD_ANIM_MOVE_RIGHT, 300, 0, False)

    def next_page(self):
        """切换到下一页"""
        total_pages = (len(self.coins_item) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.render_page()
            # 可以添加滑动动画效果[1](@ref)
            # lv_scr_load_anim(self.content, LV_SCR_LOAD_ANIM_MOVE_LEFT, 300, 0, False)

    def render_page(self):
        """渲染当前页内容"""
        # 隐藏所有coin
        for coin in self.coins_item:
            coin.add_flag(lv.obj.FLAG.HIDDEN)

        # 显示当前页的coin
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.coins_item))

        for i in range(start_idx, end_idx):
            self.coins_item[i].clear_flag(lv.obj.FLAG.HIDDEN)

        # 更新导航状态
        self.update_navigation_state()

    def update_navigation_state(self):
        """更新导航按钮状态"""
        total_pages = (len(self.coins_item) + self.items_per_page - 1) // self.items_per_page

        # 更新箭头状态
        self.left_btn.clear_state(lv.STATE.DISABLED)
        self.right_btn.clear_state(lv.STATE.DISABLED)
        if self.current_page == 0:
            self.left_arrow.set_src("A:/res/prev_gray_btn.png")
            self.right_arrow.set_src("A:/res/next_blue_btn.png")
            self.left_btn.add_state(lv.STATE.DISABLED)
        if self.current_page >= total_pages - 1:
            self.left_arrow.set_src("A:/res/prev_blue_btn.png")
            self.right_arrow.set_src("A:/res/next_gray_btn.png")
            self.right_btn.add_state(lv.STATE.DISABLED)

        # 更新页面指示器
        # self.page_indicator.set_text(f"{self.current_page + 1}/{total_pages}")

class Item(VStack):
    """基础条目类（保持原有VStack结构）"""
    def __init__(self, parent, text, icon):
        super().__init__(parent)
        self.items_center()
        self.add_style(
            Style()
            .radius(16)
            .bg_opa(lv.OPA.COVER)
            .width(400)
            .height(73)
            .pad_right(40)
            # .pad_top(15)
            .pad_column(16)
            .pad_row(0)  # 设置条目之间的间距为0pt
            .bg_color(lv.color_hex(0x15151E))
            ,
            0,
        )
        self.add_style(theme.Styles.disabled, lv.PART.MAIN | lv.STATE.DISABLED)
        # 添加底边灰色边框
        self.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        self.set_style_border_width(2, lv.PART.MAIN)
        self.set_style_border_color(lv.color_hex(0x373737), lv.PART.MAIN)
        self.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_border_opa(lv.OPA._50, lv.PART.MAIN)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)

        self.icon = lv.img(self)
        self.icon.set_src(icon)
        # 推荐使用 set_zoom 或保持原始图片尺寸，避免变形
        self.icon.set_zoom(int(256 *1.4))  # 设置为原尺寸的1.3倍
        self.icon.set_size(65,50)
        self.icon.set_style_pad_left(24, lv.PART.MAIN)
        #下边距13
        self.icon.set_style_pad_bottom(15, lv.PART.MAIN)

        self.label = lv.label(self)
        self.label.set_flex_grow(1)
        self.label.set_text(text)
        self.label.set_width(98)
        self.label.set_height(37)
        self.label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.label.set_style_pad_left(24, lv.PART.MAIN)
        #字号28
        self.label.set_style_text_font(font.Bold.SCS30, lv.PART.MAIN)
        self.label.set_style_pad_top(0, lv.PART.MAIN)
        #下边距10
        self.label.set_style_pad_bottom(10, lv.PART.MAIN)

        # arrow
        self.arrow = lv.img(self)
        #设置箭头背景图
        self.arrow.set_src("A:/res/a_right_arrow.png")
        # self.arrow.set_text(lv.SYMBOL.RIGHT)
        self.arrow.set_width(32)
        self.arrow.set_height(32)
        # self.arrow.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.arrow.set_style_pad_left(10, lv.PART.MAIN)

class Coin(Item):
    """币种条目类（继承Item并扩展功能）"""
    def __init__(self, parent, coin: CoinProtocol, detail_constructor: CoinDetailViewConstructor):
        super().__init__(parent, coin.get_name(), coin.get_icon())
        self.coin = coin
        self.detail_constructor = detail_constructor
        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)

    def action(self):
        from trezor import workflow
        screen = self.detail_constructor(self.coin)
        workflow.spawn(screen.show())

QRCODE_SIZE = 360
class CoinDetail(Navigate):
    def __init__(self, coin: CoinProtocol):
        super().__init__()
        self.coin = coin
        self.show_qrcode = False  # 默认显示地址模式
        self._address = None
        
        # 背景设置（移除白色边框）
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)
        self.set_style_border_width(0, lv.PART.MAIN)  # 移除边框
        self.set_title(self.coin.get_name())

        # 主内容容器（调整布局间距）
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(Style().pad_left(16).pad_right(16).pad_top(10), 0)

        # 二维码容器（居中布局）
        self.qrcode_container = lv.obj(self)
        self.qrcode_container.set_size(QRCODE_SIZE, QRCODE_SIZE)
        self.qrcode_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.qrcode_container.set_style_border_width(1, lv.PART.MAIN)
        self.qrcode_container.set_style_border_color(lv.color_hex(0x141419), lv.PART.MAIN)
        #圆角16
        self.qrcode_container.set_style_radius(16, lv.PART.MAIN)
        self.qrcode_container.align(lv.ALIGN.TOP_MID, 0, 100)  # 调整垂直位置
        self.qrcode_container.set_style_shadow_width(0, lv.PART.MAIN)
        self.qrcode_container.set_style_outline_width(0, lv.PART.MAIN)
        self.qrcode_container.add_flag(lv.obj.FLAG.HIDDEN)
        self._qrcode_view = None

        # 提示文本（调整位置）
        self.tip = lv.label(self)
        self.tip.set_width(400)
        self.tip.set_long_mode(lv.label.LONG.WRAP)
        self.tip.set_text(i18n.Title.receive_tips.format(self.coin.get_name()))
        self.tip.set_style_pad_top(50, lv.PART.MAIN)
        self.tip.set_style_pad_left(40, lv.PART.MAIN)
        self.tip.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.tip.align(lv.ALIGN.BOTTOM_MID, 0, -180)  # 固定在底部
        self.tip.add_flag(lv.obj.FLAG.HIDDEN)

        # 地址容器（重新设计布局）
        self.address_container = lv.obj(self)
        self.address_container.set_size(436, 400)
        self.address_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.address_container.align(lv.ALIGN.TOP_MID, 0, 100)  # 避免与标题重叠
        self.address_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.address_container.set_style_border_width(0, lv.PART.MAIN)

         # 地址显示
        self.address_view = LabeledText(self.address_container)
        self.address_view.set_width(lv.pct(100))
        self.address_view.set_label(i18n.Text.address)
        self.address_view.set_text("")
        self.address_view.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        self.address_view.set_style_pad_bottom(30, lv.PART.MAIN)

        # # 地址文本（使用spangroup分段着色）
        # self.address_span = lv.spangroup(self.address_container)
        # self.address_span.set_width(400)
        # self.address_span.set_mode(lv.SPAN_MODE.BREAK)
        # self.address_span.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        # self.address_span.align_to(self.address_label, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 20)

       # 路径显示
        self.path_view = LabeledText(self.address_container)
        self.path_view.set_label(i18n.Text.path)
        self.path_view.set_text(self.coin.get_path())
        self.path_view.set_style_pad_top(80, lv.PART.MAIN)
        self.path_view.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        self.path_view.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        # self.path_view.align(lv.ALIGN.TOP_MID, 0, 120)
        # 使用 align_to 让 path_view 紧跟 address_view，保持固定间距（如 24 像素）
        self.path_view.align_to(self.address_view, lv.ALIGN.OUT_BOTTOM_MID, 0, 70)

        # 切换按钮（固定位置）
        self.toggle_btn = lv.btn(self)
        self.toggle_btn.set_size(440, 89)
        self.toggle_btn.align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.toggle_btn.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)
        self.toggle_btn.set_style_radius(80, lv.PART.MAIN)
        self.toggle_btn_label = lv.label(self.toggle_btn)
        self.toggle_btn_label.set_text(i18n.Button.qr_code)
        self.toggle_btn_label.center()
        self.toggle_btn.add_event_cb(self.toggle_display, lv.EVENT.CLICKED, None)

    def on_loaded(self):
        super().on_loaded()
        async def load_address():
            await loop.sleep(300)
            self._address = await self.coin.get_address()
            self._update_address_display()
            if self.show_qrcode:
                self.qrcode_view.update(self._address, len(self._address))
        workflow.spawn(load_address())

    def _update_address_display(self):
        """更新地址分段着色"""
        if not self._address:
            return
        # 地址分段显示的spana容器
        self.spans = lv.spangroup(self.address_container)
        self.spans.set_width(lv.pct(100))
        self.spans.set_height(lv.SIZE.CONTENT)
        self.spans.set_mode(lv.SPAN_MODE.BREAK)
        self.spans.add_style(LabeledText.style, lv.PART.MAIN)
        # self.spans.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        # self.spans.set_style_border_width(1, lv.PART.MAIN)
        self.spans.align(lv.ALIGN.TOP_LEFT, 0, 50)
        
        span = self.spans.new_span()
        span.set_text(self._address[:4])
        span.style.set_text_font(font.Bold.SCS38)
        span.style.set_text_color(lv.color_hex(0x2A5CFF))
        span.style.set_text_letter_space(0)
        span.style.set_text_line_space(0)
        span.style.set_text_decor(0)
        span.style.set_text_align(lv.TEXT_ALIGN.LEFT)
        # span.style.set_text_break(0)  # 禁止换行会导致后续span不显示，建议去掉
        if(self.coin.get_name() == "Ton"):
            span = self.spans.new_span()
            span.set_text(self._address[4:18])
            span.style.set_text_font(font.Bold.SCS38)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))

            span = self.spans.new_span()
            span.set_text(self._address[18:37])
            span.style.set_text_font(font.Bold.SCS38)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))

            span = self.spans.new_span()
            span.set_text(self._address[37:-4])
            span.style.set_text_font(font.Bold.SCS38)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))
        else:
            span = self.spans.new_span()
            span.set_text(self._address[4:19])
            span.style.set_text_font(font.Bold.SCS38)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))

            span = self.spans.new_span()
            span.set_text(self._address[19:-4])
            span.style.set_text_font(font.Bold.SCS38)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))

        span = self.spans.new_span()
        span.set_text(self._address[-4:])
        span.style.set_text_font(font.Bold.SCS38)
        span.style.set_text_color(lv.color_hex(0x2A5CFF))

    def toggle_display(self, e):
        """切换显示模式"""
        self.show_qrcode = not self.show_qrcode
        self._update_display()
        self.toggle_btn_label.set_text(i18n.Text.address if self.show_qrcode else i18n.Button.qr_code)

    def _update_display(self):
        """更新界面显示状态"""
        if self.show_qrcode:
            self.qrcode_container.clear_flag(lv.obj.FLAG.HIDDEN)
            self.tip.clear_flag(lv.obj.FLAG.HIDDEN)
            self.address_container.add_flag(lv.obj.FLAG.HIDDEN)
            if self._address:
                self.qrcode_view.update(self._address, len(self._address))
        else:
            self.qrcode_container.add_flag(lv.obj.FLAG.HIDDEN)
            self.tip.add_flag(lv.obj.FLAG.HIDDEN)
            self.address_container.clear_flag(lv.obj.FLAG.HIDDEN)

    @property
    def qrcode_view(self) -> lv.qrcode:
        if self._qrcode_view:
            return self._qrcode_view
            
        # 创建二维码
        self._qrcode_view = lv.qrcode(self.qrcode_container, QRCODE_SIZE-60, 
                                     colors.DS.BLACK, colors.DS.WHITE)
        self._qrcode_view.set_style_border_width(24, lv.PART.MAIN)
        self._qrcode_view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)#lv.color_hex(0x141419)
        self._qrcode_view.set_style_radius(24, lv.PART.MAIN)
        self._qrcode_view.set_style_shadow_width(0, lv.PART.MAIN)
        self._qrcode_view.set_style_outline_width(0, lv.PART.MAIN)
        self._qrcode_view.center()

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
            # 添加白色四方形背景容器（无边框）
            bg_container = lv.obj(self.qrcode_container)
            bg_container.set_size(60, 60)
            bg_container.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
            bg_container.set_style_radius(16, lv.PART.MAIN)  # 四方形，无圆角
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

        return self._qrcode_view