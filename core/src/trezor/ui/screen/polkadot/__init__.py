import lvgl as lv

from trezor.ui import i18n, theme, font, colors
from trezor.ui import Reject, Continue
from trezor.ui.screen import Modal
from trezor.ui.component import HStack, LabeledText

class Balance(Modal):
    def __init__(
        self,
        amount: str,
        to: str,
        chain_name: str,
        sender: str,
        source: str | None = None,
        tip: str | None = None,
        keep_alive: str | None = None
    ):
        super().__init__()

        self.set_title(i18n.Title.x_transaction.format(chain_name))
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
            #设置颜色为白色
            item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
            return item

        # amount
        labeled(i18n.Text.amount, amount)

        # to
        labeled(i18n.Text.receiver, to)

        # sender
        labeled(i18n.Text.sender, sender)

        # source
        if source:
            labeled(i18n.Text.source, source)

        # tip
        if tip:
            labeled(i18n.Text.tip, tip)

        # keep alive
        if keep_alive:
            labeled(i18n.Text.keep_alive, keep_alive)


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
