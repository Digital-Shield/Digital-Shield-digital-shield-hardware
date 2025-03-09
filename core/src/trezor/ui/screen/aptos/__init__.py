import lvgl as lv

from typing import TYPE_CHECKING

from ubinascii import hexlify


from trezor.ui import i18n, theme, Style, colors
from trezor.ui import Continue, Reject, Detail, Confirm
from trezor.ui.component import HStack, LabeledText
from trezor.ui.screen import Modal, with_title_and_buttons

if TYPE_CHECKING:
    from typing import List
    pass

class TransactionDetail(
    with_title_and_buttons(Modal, i18n.Button.continue_, i18n.Button.reject)
):
    def __init__(
        self,
        amount: str,
        to: str,
        sender: str,
        sequence_number: int,
        max_gas_amount: int,
        gas_unit_price: str,
        expiration_time: str,
        chain_id: int,
        icon: str,
    ):
        super().__init__()

        self.set_title(i18n.Title.transaction_detail, icon)
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
        labeled(i18n.Text.from_, sender)
        # to
        labeled(i18n.Text.to, to)
        # max gas amount
        labeled(i18n.Text.max_gas_limit, str(max_gas_amount))
        # gas price
        labeled(i18n.Text.gas_unit_price, str(gas_unit_price))
        # sequence number
        labeled(i18n.Text.sequence_number, str(sequence_number))
        # expiration time
        labeled(i18n.Text.expiration_time, str(expiration_time))
        # chain id
        labeled(i18n.Text.chain_id, str(chain_id))

        self.btn_reject = self.btn_left
        self.btn_continue = self.btn_right

        # reject button
        self.btn_reject.mode("reject")
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # continue button
        self.btn_continue.add_event_cb(self.on_click_continue, lv.EVENT.CLICKED, None)

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_continue(self, e):
        self.close(Continue())


class EntryFunctionOverview(
    with_title_and_buttons(Modal, i18n.Button.confirm, i18n.Button.reject)
):
    def __init__(self, network: str, icon: str, function: str, args: List[bytes]):
        super().__init__()
        self.set_title(i18n.Title.transaction.format(network), icon)
        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            return item

        # function name
        labeled(i18n.Text.unknown_function, function)

        if args:
            for index, arg in enumerate(args):
                arg = "0x" + hexlify(arg).decode()
                labeled(i18n.Text.argument_x.format(index), arg)

        # view detail button
        self.btn_detail = lv.btn(self.content)
        self.btn_detail.add_style(
            Style()
            .bg_opa(lv.OPA._10)
            .width(lv.pct(100))
            .border_width(1)
            .border_color(colors.DS.PRIMARY)
            .height(96)
            .radius(16),
            lv.PART.MAIN,
        )
        label = lv.label(self.btn_detail)
        label.set_text(i18n.Button.view_detail)
        label.set_style_text_color(colors.DS.PRIMARY, lv.PART.MAIN)
        label.center()
        self.btn_detail.add_event_cb(self.on_click_detail, lv.EVENT.CLICKED, None)

        # reject button
        self.btn_reject = self.btn_left
        self.btn_reject.mode("reject")
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # confirm button
        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

    def on_click_detail(self, e):
        self.close(Detail())

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_confirm(self, e):
        self.close(Confirm())


class EntryFunctionDetail(
    with_title_and_buttons(Modal, i18n.Button.continue_, i18n.Button.reject)
):
    def __init__(
        self,
        sender: str,
        sequence_number: int,
        max_gas_amount: int,
        gas_unit_price: str,
        expiration_time: str,
        chain_id: int,
        icon: str,
        function: str,
        args: List[bytes]
    ):
        super().__init__()
        self.set_title(i18n.Title.transaction_detail, icon)
        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            return item

        # function name
        labeled(i18n.Text.unknown_function, function)

        if args:
            for index, arg in enumerate(args):
                arg = "0x" + hexlify(arg).decode()
                labeled(i18n.Text.argument_x.format(index), arg)

        # from
        labeled(i18n.Text.from_, sender)
        # max gas amount
        labeled(i18n.Text.max_gas_limit, str(max_gas_amount))
        # gas price
        labeled(i18n.Text.gas_unit_price, str(gas_unit_price))
        # sequence number
        labeled(i18n.Text.sequence_number, str(sequence_number))
        # expiration time
        labeled(i18n.Text.expiration_time, str(expiration_time))
        # chain id
        labeled(i18n.Text.chain_id, str(chain_id))

        self.btn_reject = self.btn_left
        self.btn_continue = self.btn_right

        # reject button
        self.btn_reject.mode("reject")
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # continue button
        self.btn_continue.add_event_cb(self.on_click_continue, lv.EVENT.CLICKED, None)

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_continue(self, e):
        self.close(Continue())
