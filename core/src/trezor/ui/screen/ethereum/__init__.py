import lvgl as lv

from typing import TYPE_CHECKING

from trezor import log
from trezor.ui import i18n, theme, colors, font, Style
from trezor.ui import Confirm, Reject, Continue, Cancel, More
from trezor.ui.component import HStack, LabeledText, Button
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

        self.set_title(i18n.Title.transaction_detail, icon)
        self.btn_right.set_text(i18n.Button.continue_)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            return item

        # amount
        labeled(i18n.Text.amount, amount)

        # from
        labeled(i18n.Text.from_, from_)

        # to
        labeled(i18n.Text.receiver, to)

        # max fee
        labeled(i18n.Text.max_fee, fee_max)

        # gas price
        labeled(i18n.Text.gas_price, gas_price)

        # total
        if total is not None:
            item = labeled(i18n.Text.total, total)
            item.label.set_style_text_color(colors.DS.BLACK, lv.PART.MAIN)
            item.label.set_style_text_font(font.bold, lv.PART.MAIN)

        self.btn_reject = self.btn_left
        self.btn_continue = self.btn_right

        # reject button
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # continue button
        self.btn_continue.add_event_cb(self.on_click_continue, lv.EVENT.CLICKED, None)

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
