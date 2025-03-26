import lvgl as lv

from trezor.ui import i18n, theme, colors, font
from trezor.ui import Continue, Reject
from trezor.ui.component import HStack, LabeledText
from trezor.ui.screen import Modal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
    AssetMode = Literal['freeze', 'unfreeze', 'delegate', 'undelegate']


class Asset(Modal):
    def __init__(
        self,
        sender: str,
        *,
        mode: AssetMode,
        resource: str|None = None,
        balance: str|None = None,
        duration: str|None = None,
        receiver: str|None = None,
        lock: str|None = None,
    ):
        super().__init__()

        self.set_title(i18n.Title.asset, None)
        self.btn_right.set_text(i18n.Button.continue_)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        item = self.add(lv.label)
        if mode == 'freeze':
            item.set_text(i18n.Text.you_are_freezing)
        elif mode == 'unfreeze':
            item.set_text(i18n.Text.you_are_unfreezing)
        elif mode == 'delegate':
            item.set_text(i18n.Text.you_are_delegating)
        elif mode == 'undelegate':
            item.set_text(i18n.Text.you_are_undelegating)

        def labeled(label, text):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            return item

        labeled(i18n.Text.sender, sender)

        if resource is not None:
            labeled(i18n.Text.resource, resource)

        if balance is not None:
            if mode == 'freeze':
                label = i18n.Text.frozen_balance
            elif mode == 'unfreeze':
                label = i18n.Text.unfrozen_balance
            elif mode == 'delegate':
                label = i18n.Text.delegated_balance
            elif mode == 'undelegate':
                label = i18n.Text.undelegated_balance
            else:
                label = i18n.Text.amount
            labeled(label, balance)

        if duration is not None:
            labeled(i18n.Text.duration, duration)

        if receiver is not None:
            labeled(i18n.Text.receiver, receiver)

        if lock is not None:
            labeled(i18n.Text.lock, lock)


        self.btn_reject = self.btn_left
        self.btn_continue = self.btn_right
        # reject button
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # continue button
        self.btn_continue.add_event_cb(self.on_click_continue, lv.EVENT.CLICKED, None)
    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_continue(self, e):
        self.close(Continue())

class TransactionDetail(Modal):
    def __init__(
        self,
        amount: str,
        from_: str,
        to: str,
        fee_max: str,
        total: str | None,
    ):
        super().__init__()

        self.set_title(i18n.Title.transaction_detail)
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
