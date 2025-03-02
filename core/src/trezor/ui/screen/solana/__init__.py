import lvgl as lv

from trezor.ui import i18n, theme, colors, font
from trezor.ui import Continue, Reject
from trezor.ui.component import HStack, LabeledText
from trezor.ui.screen import with_title_and_buttons
from trezor.ui.screen import Modal


class TransactionDetail(
    with_title_and_buttons(Modal, i18n.Button.continue_, i18n.Button.reject)
):
    def __init__(self, amount: str, from_: str, to: str, total: str | None):
        super().__init__()
        self.set_title(i18n.Title.transaction_detail)
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

        # total
        if total is not None:
            labeled(i18n.Text.total, total)

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


class SPLTokenTransactionDetail(
    with_title_and_buttons(Modal, i18n.Button.continue_, i18n.Button.reject)
):
    def __init__(self, from_addr: str, to_addr: str, amount: str, source_owner: str, fee_payer: str, token_mint: str = None):
        super().__init__()
        self.set_title(i18n.Title.transaction_detail)
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
        labeled(i18n.Solana.ata_sender, from_addr)

        # to
        labeled(i18n.Solana.ata_reciver, to_addr)

        # source_owner
        labeled(i18n.Solana.source_owner, source_owner)

        # fee_payer
        labeled(i18n.Solana.fee_payer, fee_payer)

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




