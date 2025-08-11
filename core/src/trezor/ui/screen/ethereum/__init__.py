import lvgl as lv

from typing import TYPE_CHECKING

from trezor import log
from trezor.ui import i18n, theme, colors, font, Style
from trezor.ui import Confirm, Reject, Continue, Cancel, More
from trezor.ui.component import HStack, LabeledText, Button, VStack
from trezor.ui.screen import Modal
from trezor.ui.screen.confirm import HolderConfirm

# import TransactionOverview in `ethereum` namespace
from trezor.ui.screen.template import TransactionOverview
from trezor.ui.screen.template import TransactionOverviewTon

if TYPE_CHECKING:
    from typing import Literal, Iterable

    pass


class TypedHash(Modal):
    def __init__(self, domain_hash: str, message_hash: str, *, coin: str|None = None):
        super().__init__()
        self.set_title(i18n.Title.typed_hash.format(coin or ""))
        self.btn_right.set_text(i18n.Button.continue_)
        self.btn_left.set_text(i18n.Button.cancel)

        self.content: lv.obj
        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            return item

        # domain hash
        labeled(i18n.Text.domain_hash, domain_hash)

        # message hash
        labeled(i18n.Text.message_hash, message_hash)

        # alias nick name for buttons
        self.btn_cancel = self.btn_left
        self.btn_continue = self.btn_right
        self.btn_cancel.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)
        self.btn_continue.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)
        self.btn_cancel.mode('cancel')


    def on_click_button(self, e: lv.event_t):
        target = e.target
        if target == self.btn_continue:
            log.debug(__name__, "clicked continue button")
            self.close(Confirm())
        elif target == self.btn_cancel:
            log.debug(__name__, "clicked cancel button")
            self.close(Cancel())


class Eip712(Modal):
    def __init__(self, title: str, **kwargs):
        super().__init__()
        self.set_title(title)
        self.btn_right.set_text(i18n.Button.continue_)
        self.btn_left.set_text(i18n.Button.cancel)

        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            return item

        for k in ("name", "version", "chainId", "verifyingContract", "salt"):
            if (v := kwargs.get(k)) is not None:
                labeled(f"{k} :", v)

        # alias nick for buttons
        self.btn_reject = self.btn_left
        self.btn_confirm = self.btn_right
        self.btn_reject.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)
        self.btn_confirm.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)
        self.btn_reject.mode('reject')

    def on_click_button(self, e: lv.event_t):
        target = e.target
        if target == self.btn_confirm:
            log.debug(__name__, "clicked confirm button")
            self.close(Confirm())
        elif target == self.btn_reject:
            log.debug(__name__, "clicked reject button")
            self.close(Reject())


class ShowMore(Modal):
    def __init__(self, title: str, param: Iterable[str]):
        super().__init__()
        self.set_title(title)
        self.btn_right.set_text(i18n.Button.confirm)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        # an labeled item and a button

        param = iter(param)
        # use first as label
        label = next(param)
        # use remained as content
        content = "\n".join(param)
        item = self.add(LabeledText)
        item.set_label(label)
        item.set_text(content)

        # view detail button
        self.btn_more = self.add(Button)
        self.btn_more.set_size(lv.pct(100), 96)
        self.btn_more.add_style(
            Style()
            .bg_opa(lv.OPA._10)
            .border_width(1)
            .border_color(colors.DS.PRIMARY)
            .radius(16),
            lv.PART.MAIN
        )
        self.btn_more.set_text(i18n.Button.view_more)
        self.btn_more.text_color(colors.DS.PRIMARY)

        self.btn_more.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)

        # alias nick for buttons
        self.btn_reject = self.btn_left
        self.btn_confirm = self.btn_right
        self.btn_reject.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)
        self.btn_confirm.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)
        self.btn_reject.mode('reject')

    def on_click_button(self, e: lv.event_t):
        target = e.target
        if target == self.btn_confirm:
            log.debug(__name__, "clicked confirm button")
            self.close(Confirm())
        elif target == self.btn_reject:
            log.debug(__name__, "clicked reject button")
            self.close(Reject())
        elif target == self.btn_more:
            log.debug(__name__, "clicked more button")
            self.close(More())

class TransactionDetail(Modal):
    def __init__(
        self,
        amount: str,
        from_: str,
        to: str,
        fee_max: str,
        gas_price: str,
        total: str | None,
        icon: str | None,
    ):
        super().__init__()

        # self.set_title(i18n.Title.transaction_detail, icon)
        self.btn_right.set_style_width(214, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.set_text(i18n.Button.continue_)
        self.btn_left.set_style_width(214, lv.PART.MAIN)
        self.btn_left.set_style_height(89, lv.PART.MAIN)
        self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
        self.btn_left.set_text(i18n.Button.cancel)
        self.network = ""
        #判断链
        if icon == "A:/res/btc-btc.png":
            self.network = "Bitcoin"
        elif icon == "A:/res/btc-doge.png":
            self.network = "Dogecoin"
        elif icon == "A:/res/btc-ltc.png":
            self.network = "Litecoin"
        elif icon == "A:/res/chain-apt.png":
            self.network = "APTOS"
        elif icon == "A:/res/chain-dot.png":
            self.network = "Polkadot"
        elif icon == "A:/res/chain-sol.png":
            self.network = "SOL"
        elif icon == "A:/res/chain-sui.png":
            self.network = "SUI"
        elif icon == "A:/res/chain-ton.png":
            self.network = "TON"
        elif icon == "A:/res/chain-tron.png":
            self.network = "TRON"
        elif icon == "A:/res/evm-bsc.png":
            self.network = "BNB Smart Chain"
        elif icon == "A:/res/evm-eth.png":
            self.network = "Ethereum"
        elif icon == "A:/res/evm-matic.png":
            self.network = "Polygon"

        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        # def labeled(label: str, text: str):
        #     item = LabeledText(self.content)
        #     item.set_label(label)
        #     item.set_text(text)
        #     #设置颜色为白色
        #     item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        #     return item

        # # amount
        # labeled(i18n.Text.amount, amount)
        # # from
        # labeled(i18n.Text.from_, from_)
        # # to
        # labeled(i18n.Text.receiver, to)
        view = self.add(HStack)
        view.add_style(theme.Styles.board, lv.PART.MAIN)
        view.set_height(lv.SIZE.CONTENT)
        
         # 头部币种显示区域
        self.coin_area = view.add(VStack)
        self.coin_area.set_size(260, 45)
        self.coin_area.align(lv.ALIGN.TOP_LEFT, 10,180)
        print("pic--",icon)
        #显示一个图片，较大尺寸显示
        if icon:
            self.icon = self.coin_area.add(lv.img)
            self.icon.set_src(icon)
            self.icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
            self.icon.set_style_align(lv.ALIGN.LEFT_MID, lv.PART.MAIN)
            self.icon.set_style_pad_all(0, lv.PART.MAIN)
            self.icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
            self.icon.set_zoom(256)  # 1.0x zoom, ensures full image is shown
            self.icon.clear_flag(lv.obj.FLAG.CLICKABLE)
            self.icon.set_style_clip_corner(False, lv.PART.MAIN)
        
        # # Add the coin name
        # submit_label = self.coin_area.add(lv.label)
        # submit_label.set_width(lv.pct(100))
        # submit_label.set_text(self.network)
        # submit_label.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        # submit_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        # submit_label.set_style_pad_all(0, lv.PART.MAIN)
        # submit_label.set_style_pad_left(15, lv.PART.MAIN)
        # submit_label.center()

        # send `amount`
        # 缩小和上边图片的距离
        spans = self.add(lv.spangroup)
        spans.set_width(lv.pct(100))
        spans.set_height(lv.SIZE.CONTENT)
        spans.set_mode(lv.SPAN_MODE.BREAK)
        spans.add_style(LabeledText.style, lv.PART.MAIN)
        spans.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        spans.set_style_border_width(1, lv.PART.MAIN)
        spans.set_style_pad_top(-30, lv.PART.MAIN)  # 调整为更小的上边距

        item = LabeledText(self.content)
        item.set_label(i18n.Text.send)
        item.label.set_style_text_font(font.bold, lv.PART.MAIN)
        item.set_text(amount)
        #字号40
        item.set_style_text_font(font.Medium.SCS40, lv.PART.MAIN)
        item.set_style_text_font(font.bold, lv.PART.MAIN)  # 设置加粗
        item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)#设置颜色为黑色
        

        # to
        # 创建一个带有淡灰色背景的容器，四边超出一些，突出显示为独立区块
        self.to_container = self.add(lv.obj)
        self.to_container.set_size(lv.pct(100), lv.SIZE.CONTENT)
        self.to_container.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)  # 淡灰色
        self.to_container.set_style_bg_opa(lv.OPA._30, lv.PART.MAIN)
        self.to_container.set_style_radius(16, lv.PART.MAIN)
        self.to_container.set_style_pad_all(12, lv.PART.MAIN)
        self.to_container.set_style_pad_row(0, lv.PART.MAIN)
        self.to_container.set_style_pad_column(0, lv.PART.MAIN)
        self.to_container.set_style_border_width(0, lv.PART.MAIN)#边框宽度设置0
        item = lv.label(self.to_container)
        item.set_text(i18n.Text.to)
        item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        # 地址分段显示的spana容器
        self.spans = lv.spangroup(self.to_container)
        self.spans.set_width(lv.pct(100))
        self.spans.set_height(lv.SIZE.CONTENT)
        self.spans.set_mode(lv.SPAN_MODE.BREAK)
        self.spans.add_style(LabeledText.style, lv.PART.MAIN)
        self.spans.align(lv.ALIGN.TOP_LEFT, 0, 30)
        
        span = self.spans.new_span()
        span.set_text(to[:4])
        span.style.set_text_font(font.Medium.SCS40)
        span.style.set_text_color(lv.color_hex(0x2A5CFF))
        span.style.set_text_letter_space(0)
        span.style.set_text_line_space(0)
        span.style.set_text_decor(0)
        span.style.set_text_align(lv.TEXT_ALIGN.LEFT)
        # span.style.set_text_break(0)  # 禁止换行会导致后续span不显示，建议去掉
        if(self.network == "TON"):
            span = self.spans.new_span()
            span.set_text(to[4:18])
            span.style.set_text_font(font.Medium.SCS40)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))

            span = self.spans.new_span()
            span.set_text(to[18:37])
            span.style.set_text_font(font.Medium.SCS40)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))

            span = self.spans.new_span()
            span.set_text(to[37:-4])
            span.style.set_text_font(font.Medium.SCS40)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))
        else:
            span = self.spans.new_span()
            span.set_text(to[4:19])
            span.style.set_text_font(font.Medium.SCS40)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))

            span = self.spans.new_span()
            span.set_text(to[19:-4])
            span.style.set_text_font(font.Medium.SCS40)
            span.style.set_text_color(lv.color_hex(0xFFFFFF))

        span = self.spans.new_span()
        span.set_text(to[-4:])
        span.style.set_text_font(font.Medium.SCS40)
        span.style.set_text_color(lv.color_hex(0x2A5CFF))

        # 折叠项容器
        self.collapsible_container = self.add(HStack)
        self.collapsible_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.collapsible_container.set_style_pad_gap(0, lv.PART.MAIN)
        # 设置宽度为100%，高度自适应内容
        self.collapsible_container.set_size(lv.pct(100), lv.SIZE.CONTENT)
        # 设置淡灰色背景，四边超出一些，突出为独立区块
        self.collapsible_container.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
        self.collapsible_container.set_style_bg_opa(lv.OPA._30, lv.PART.MAIN)
        self.collapsible_container.set_style_radius(16, lv.PART.MAIN)
        self.collapsible_container.set_style_pad_all(12, lv.PART.MAIN)
        self.collapsible_container.set_style_border_width(0, lv.PART.MAIN)
        

        # 折叠内容（初始展开）
        self.collapsible_content = self.collapsible_container.add(lv.obj)
        self.collapsible_content.set_style_pad_all(0, lv.PART.MAIN)
        self.collapsible_content.set_style_bg_opa(0, lv.PART.MAIN)
        self.collapsible_content.set_style_border_width(0, lv.PART.MAIN)
        self.collapsible_content.set_style_pad_gap(0, lv.PART.MAIN)
        self.collapsible_content.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.collapsible_content.set_size(lv.pct(80), lv.SIZE.CONTENT)  # 宽度100%，高度自适应内容
        # 默认展开，不添加 HIDDEN 标志
        # self.collapsible_content.add_flag(lv.obj.FLAG.HIDDEN)
        

        # max fee
        self.item_max_fee = LabeledText(self.collapsible_content)
        self.item_max_fee.set_label(i18n.Text.max_fee)
        self.item_max_fee.set_text(fee_max)
        self.item_max_fee.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)

        # gas price
        self.item_gas_price = LabeledText(self.collapsible_content)
        self.item_gas_price.set_label(i18n.Text.gas_price)
        self.item_gas_price.set_text(gas_price)
        self.item_gas_price.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)

        # total
        if total is not None:
            self.item_total = LabeledText(self.collapsible_content)
            self.item_total.set_label(i18n.Text.total)
            self.item_total.set_text(total)
            self.item_total.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
            self.item_total.label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
            self.item_total.label.set_style_text_font(font.bold, lv.PART.MAIN)

        # # 折叠/展开按钮
        # self.btn_toggle = self.collapsible_container.add(Button)
        # self.btn_toggle.set_size(lv.pct(100), 48)
        # self.btn_toggle.set_style_bg_opa(0, lv.PART.MAIN)
        # self.btn_toggle.set_style_border_width(0, lv.PART.MAIN)
        # self.btn_toggle.set_style_radius(0, lv.PART.MAIN)
        # self.btn_toggle.set_style_pad_all(0, lv.PART.MAIN)
        # self.btn_toggle.set_style_text_color(colors.DS.PRIMARY, lv.PART.MAIN)
        # # self.btn_toggle.set_text("▲ " + i18n.Text.lock)
        # self.btn_toggle.add_event_cb(self.on_toggle_collapse, lv.EVENT.CLICKED, None)
        
        self._collapsed = False  # 默认展开


        self.btn_reject = self.btn_left
        self.btn_continue = self.btn_right

        # reject button
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # continue button
        self.btn_continue.add_event_cb(self.on_click_continue, lv.EVENT.CLICKED, None)
    #展开或折叠
    def on_toggle_collapse(self, e):
        if self._collapsed:
            self.collapsible_content.clear_flag(lv.obj.FLAG.HIDDEN)
            self.btn_toggle.set_text("▲ " + i18n.Text.lock)
            self._collapsed = False
        else:
            self.collapsible_content.add_flag(lv.obj.FLAG.HIDDEN)
            self.btn_toggle.set_text("▼ " + i18n.Button.view_detail)
            self._collapsed = True
    def show_contract_address(self, address: str):
        item = self.add(LabeledText)
        item.set_label(i18n.Text.contract)
        item.set_text(address)

    def show_token_id(self, id: int):
        item = self.add(LabeledText)
        item.set_label("Token ID:")
        item.set_text(str(id))

    def show_chain_id(self, id: int):
        item = self.add(LabeledText)
        item.set_label("Chain ID:")
        item.set_text(str(id))

    def show_raw_data(self, data: bytes):
        item = self.add(LabeledText)
        item.set_label("Raw:")
        from ubinascii import hexlify
        item.set_text(hexlify(data).decode())

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_continue(self, e):
        self.close(Continue())


class TransactionDetail1559(Modal):
    def __init__(
        self,
        amount: str,
        from_: str,
        to: str,
        fee_max: str,
        max_priority_fee_per_gas: str,
        max_fee_per_gas: str,
        total: str,
        icon: str | None,
    ):
        super().__init__()
        self.set_title(i18n.Title.transaction_detail, icon)
        self.btn_right.set_text(i18n.Button.confirm)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            #设置颜色为白色
            item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
            return item

        # amount
        labeled(i18n.Text.amount, amount)

        # from
        labeled(i18n.Text.from_, from_)

        # to
        labeled(i18n.Text.receiver, to)

        # max fee
        labeled(i18n.Text.max_fee, fee_max)

        # max priority fee per gas
        labeled(i18n.Text.max_priority_fee_per_gas, max_priority_fee_per_gas)

        # max fee per gas
        labeled(i18n.Text.max_fee_per_gas, max_fee_per_gas)

        # total
        if total is not None:
            item = labeled(i18n.Text.total, total)
            item.label.set_style_text_color(colors.DS.BLACK, lv.PART.MAIN)
            item.label.set_style_text_font(font.bold, lv.PART.MAIN)

        self.btn_reject = self.btn_left
        self.btn_continue = self.btn_right

        # reject button
        self.btn_reject.color(colors.DS.WHITE)
        self.btn_reject.text_color(colors.DS.DANGER)
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # continue button
        self.btn_continue.add_event_cb(self.on_click_continue, lv.EVENT.CLICKED, None)

    def show_contract_address(self, address: str):
        item = self.add(LabeledText)
        item.set_label(i18n.Text.contract)
        item.set_text(address)
        #设置颜色为白色
        item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)

    def show_token_id(self, id: int):
        item = self.add(LabeledText)
        item.set_label("Token ID:")
        item.set_text(str(id))

    def show_chain_id(self, id: int):
        item = self.add(LabeledText)
        item.set_label("Chain ID:")
        item.set_text(str(id))

    def show_raw_data(self, data: bytes):
        item = self.add(LabeledText)
        item.set_label("Raw:")
        from ubinascii import hexlify
        item.set_text(hexlify(data).decode())

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_continue(self, e):
        self.close(Continue())
