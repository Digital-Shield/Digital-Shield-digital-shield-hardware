import lvgl as lv

from trezor.ui import i18n, theme, log, font, colors, Style
from trezor.ui import Confirm, Reject
from trezor.ui.component import HStack, LabeledText
from trezor.ui.screen import Modal

class PublicKey(Modal):
    def __init__(self, pubkey: str, path: str, network: str):
        super().__init__()
        self.set_title(i18n.Title.public_key.format(network))
        self.btn_right.set_text(i18n.Button.confirm)

        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        # `path`
        item = self.add(LabeledText)
        item.set_label(i18n.Text.path)
        item.set_text(path)

        # `public key`
        item = self.add(LabeledText)
        item.set_label(i18n.Text.public_key)
        item.set_text(pubkey)

    def on_click_confirm(self, e):
        log.debug(__name__, "user click confirm")
        self.close(Confirm())

    def on_click(self, e):
        log.debug(__name__, "user click address screen")
        target = e.target
        if target == self.btn_confirm:
            self.on_click_confirm(e)


# move `xPub` to bitcoin
class XPub(Modal):
    def __init__(self, xpub: str, path: str, network: str):
        super().__init__()
        self.set_title(i18n.Title.xpub.format(network))
        self.btn_right.set_text(i18n.Button.confirm)

        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

        self.create_content(HStack)
        self.content: HStack

        # `path`
        item = self.add(LabeledText)
        item.set_label(i18n.Text.path)
        item.set_text(path)

        # `public key`
        item = self.add(LabeledText)
        item.set_label(i18n.Text.xpub)
        item.set_text(xpub)

    def on_click_confirm(self, e):
        log.debug(__name__, "user click confirm")
        self.close(Confirm())

    def on_click(self, e):
        log.debug(__name__, "user click address screen")
        target = e.target
        if target == self.btn_confirm:
            self.on_click_confirm(e)

class PaymentRequest(Modal):
    def __init__(self, amount: str, to: str, *, message: str|None = None):
        super().__init__()
        self.set_title(i18n.Title.view_transaction)
        self.btn_right.set_text(i18n.Button.confirm)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        if message:
            item = self.add(lv.label)
            item.set_text(message)
        # send `amount`
        spans = self.add(lv.spangroup)
        spans.set_width(lv.pct(100))
        spans.set_height(lv.SIZE.CONTENT)
        spans.set_mode(lv.SPAN_MODE.BREAK)
        spans.add_style(LabeledText.style, lv.PART.MAIN)
        spans.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        spans.set_style_border_width(1, lv.PART.MAIN)

        span = spans.new_span()
        span.set_text(i18n.Text.send)
        span.style.set_text_font(font.bold)
        span.style.set_text_color(colors.STD.WHITE)

        span = spans.new_span()
        span.set_text(amount)
        span.style.set_text_font(font.bold)
        span.style.set_text_color(colors.DS.DANGER)

        # to
        item = self.add(LabeledText)
        item.set_label(i18n.Text.to)
        item.set_text(to)
        item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
        
        # reject button
        self.btn_reject = self.btn_left
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # confirm button
        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_confirm(self, e):
        self.close(Confirm())


class Output(Modal):
    def __init__(self, amount: str, to: str):
        super().__init__()
        self.set_title(i18n.Title.view_transaction)
        self.btn_right.set_text(i18n.Button.confirm)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        # send `amount`
        spans = self.add(lv.spangroup)
        spans.set_width(lv.pct(100))
        spans.set_height(lv.SIZE.CONTENT)
        spans.set_mode(lv.SPAN_MODE.BREAK)
        spans.add_style(LabeledText.style, lv.PART.MAIN)
        spans.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        spans.set_style_border_width(1, lv.PART.MAIN)

        span = spans.new_span()
        span.set_text(i18n.Text.send)
        span.style.set_text_font(font.bold)
        span.style.set_text_color(colors.STD.WHITE)

        span = spans.new_span()
        span.set_text(amount)
        span.style.set_text_font(font.bold)
        span.style.set_text_color(colors.DS.DANGER)

        # to
        item = self.add(LabeledText)
        item.set_label(i18n.Text.to)
        item.set_text(to)
        item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)

        # reject button
        self.btn_reject = self.btn_left
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # confirm button
        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_confirm(self, e):
        self.close(Confirm())

class Total(Modal):
    def __init__(self, amount: str, fee: str, total: str, coin: str):
        super().__init__()
        self.set_title(i18n.Title.x_transaction.format(coin))
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

        # fee
        labeled(i18n.Text.fee, fee)

        # total
        labeled(i18n.Text.total, total)

        # reject button
        self.btn_reject = self.btn_left
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # confirm button
        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_confirm(self, e):
        self.close(Confirm())

class JointAmount(Modal):
    def __init__(self, amount: str, total: str, coin: str):
        super().__init__()
        self.set_title(i18n.Title.x_joint_transaction.format(coin))
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
            item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)
            return item

        # your spend
        labeled(i18n.Text.your_spend, amount)

        # total
        labeled(i18n.Text.total, total)

        # reject button
        self.btn_reject = self.btn_left
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # confirm button
        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_confirm(self, e):
        self.close(Confirm())


class OutputChange(Modal):
    def __init__(self, amount: str, to: str, amount_changed: str, amount_changed_label: str):
        super().__init__()
        self.set_title(i18n.Title.view_transaction)
        self.btn_right.set_text(i18n.Button.confirm)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        item = self.add(LabeledText)
        item.set_label(amount_changed_label)
        item.set_text(amount_changed)

        # send `amount`
        spans = self.add(lv.spangroup)
        spans.set_width(lv.pct(100))
        spans.set_height(lv.SIZE.CONTENT)
        spans.set_mode(lv.SPAN_MODE.BREAK)
        spans.add_style(LabeledText.style, lv.PART.MAIN)
        spans.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        spans.set_style_border_width(1, lv.PART.MAIN)

        span = spans.new_span()
        span.set_text(i18n.Text.send)
        span.style.set_text_font(font.bold)
        span.style.set_text_color(colors.STD.WHITE)

        span = spans.new_span()
        span.set_text(amount)
        span.style.set_text_font(font.bold)
        span.style.set_text_color(colors.DS.DANGER)

        # to
        item = self.add(LabeledText)
        item.set_label(i18n.Text.to)
        item.set_text(to)
        item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN)

        # reject button
        self.btn_reject = self.btn_left
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # confirm button
        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_confirm(self, e):
        self.close(Confirm())

class FeeChange(Modal):
    def __init__(self, fee: str, fee_changed: str, fee_changed_label: str):
        super().__init__()
        self.set_title(i18n.Title.view_transaction)
        self.btn_right.set_text(i18n.Button.confirm)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        # changed
        item = self.add(LabeledText)
        item.set_label(fee_changed_label)
        item.set_text(fee_changed)

        # fee
        item = self.add(LabeledText)
        item.set_label(i18n.Text.fee)
        item.set_text(fee)
        item.item.set_style_text_color(colors.DS.DANGER, lv.PART.MAIN)
        item.item.set_style_text_font(font.bold, lv.PART.MAIN)


        # reject button
        self.btn_reject = self.btn_left
        self.btn_reject.mode('reject')
        self.btn_reject.add_event_cb(self.on_click_reject, lv.EVENT.CLICKED, None)

        # confirm button
        self.btn_confirm = self.btn_right
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_confirm(self, e):
        self.close(Confirm())
