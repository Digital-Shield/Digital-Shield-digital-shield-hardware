import lvgl as lv

from trezor import log
from trezor.ui import i18n, font, colors, theme, Style
from trezor.ui import Confirm, Reject, Cancel, Detail
from trezor.ui.screen import Modal, with_title_and_buttons
from trezor.ui.screen.confirm import HolderConfirm
from trezor.ui.component import HStack, LabeledText

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    AddressState = Literal["address", "qrcode"]

class Address(with_title_and_buttons(Modal, i18n.Button.confirm, i18n.Button.qr_code)):
    def __init__(
        self, address: str, path: str, network: str, chain_id: int | None = None
    ):
        super().__init__()
        self.set_title(i18n.Title.address.format(network))

        self.address = address
        self.path = path
        self.network = network
        self.chain_id = chain_id

        self.btn_toggle = self.btn_left
        self.btn_confirm = self.btn_right

        self.btn_toggle.add_event_cb(self.on_click_toggle, lv.EVENT.CLICKED, None)
        self.btn_confirm.add_event_cb(self.on_click_confirm, lv.EVENT.CLICKED, None)

        self.content: lv.obj
        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self._address_view: HStack | None = None
        self._qrcode_view: lv.qrcode | None = None

        # default show address
        self.state: AddressState = "address"
        self.address_view.clear_flag(lv.obj.FLAG.HIDDEN)

    @property
    def address_view(self):
        if self._address_view is not None:
            return self._address_view

        view = self.add(HStack)
        view.add_style(theme.Styles.board, lv.PART.MAIN)
        view.set_height(lv.SIZE.CONTENT)

        # `address`
        label = view.add(lv.label)
        label.set_text(self.address)
        label.set_long_mode(lv.label.LONG.WRAP)
        label.set_width(lv.pct(100))
        label.set_style_text_font(font.mono, lv.PART.MAIN)
        label.add_style(LabeledText.style, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = view.add(LabeledText)
            item.set_label(label)
            item.set_text(text)

        # path
        labeled(i18n.Text.path, self.path)

        if self.chain_id is not None:
            labeled(i18n.Text.chain_id, str(self.chain_id))

        self._address_view = view
        return self._address_view

    @property
    def qrcode_view(self):
        if self._qrcode_view is not None:
            return self._qrcode_view

        view = lv.qrcode(self.content, 400, colors.DS.BLACK, colors.DS.WHITE)
        view.update(self.address, len(self.address))
        view.set_style_border_width(16, lv.PART.MAIN)
        view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
        view.center()
        self._qrcode_view = view
        return self._qrcode_view

    def on_click_toggle(self, e):
        label: lv.label = self.btn_toggle.get_child(0)
        if self.state == "address":
            self.state = "qrcode"
            label.set_text(i18n.Button.address)
            self.qrcode_view.clear_flag(lv.obj.FLAG.HIDDEN)
            self.address_view.add_flag(lv.obj.FLAG.HIDDEN)
        else:
            self.state = "address"
            label.set_text(i18n.Button.qr_code)
            self.address_view.clear_flag(lv.obj.FLAG.HIDDEN)
            self.qrcode_view.add_flag(lv.obj.FLAG.HIDDEN)

    def on_click_confirm(self, e):
        log.debug(__name__, "user click confirm")
        self.close(Confirm())

    def on_click(self, e):
        log.debug(__name__, "user click address screen")
        target = e.target
        if target == self.btn_confirm:
            self.on_click_confirm(e)
        if target == self.btn_toggle:
            self.on_click_toggle(e)

class Blob(with_title_and_buttons(Modal, i18n.Button.continue_, i18n.Button.cancel)):
    """
    A `Modal` contain: `message`, `label`: `blob`
    """
    def __init__(self, title: str, message: str, *, label: str|None = None, blob: str|bytes|None = None):
        super().__init__()

        self.set_title(title)
        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        if message:
            item = self.add(lv.label)
            item.set_width(lv.pct(100))
            item.set_long_mode(lv.label.LONG.WRAP)
            item.set_text(message)

        if label is not None:
            item = self.add(LabeledText)
            item.set_label(label)
            if isinstance(blob,(bytes, bytearray)):
                from ubinascii import hexlify
                blob = '0x'+hexlify(blob).decode()

        item.set_text(blob)

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


class SignMessage(with_title_and_buttons(Modal, i18n.Button.sign, i18n.Button.reject)):
    def __init__(
        self,
        title: str,
        message: str,
        *,
        address: str,
        chain_id: int | None = None,
        icon: str | None = None
    ):
        super().__init__()

        self.set_title(title, icon)
        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            return item

        # chin_id
        if chain_id is not None:
            labeled(i18n.Text.chain_id, str(chain_id))

        # address
        labeled(i18n.Text.address, address)

        # message
        labeled(i18n.Text.message, message)

        self.btn_left.mode('reject')
        self.btn_right.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)
        self.btn_left.add_event_cb(self.on_click_button, lv.EVENT.CLICKED, None)

    def set_mode(self, mode: Literal["sign", "verify"]):
        if mode == "sign":
            self.btn_right.set_text(i18n.Button.sign)
        elif mode == "verify":
            self.btn_right.set_text(i18n.Button.verify)

    def on_click_button(self, e: lv.event_t):
        target = e.target
        if target == self.btn_right:
            log.debug(__name__, "clicked right button")
            self.close(Confirm())
        elif target == self.btn_left:
            log.debug(__name__, "clicked left button")
            self.close(Reject())

class TransactionOverview(with_title_and_buttons(Modal, i18n.Button.confirm, i18n.Button.reject)):
    def __init__(self, network: str, amount: str, to: str, icon: str):
        super().__init__()
        self.set_title(i18n.Title.transaction.format(network), icon)
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

        span = spans.new_span()
        span.set_text(amount)
        span.style.set_text_font(font.bold)
        span.style.set_text_color(colors.DS.DANGER)

        # to
        item = self.add(LabeledText)
        item.set_label(i18n.Text.to)
        item.set_text(to)

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
            lv.PART.MAIN
        )
        label = lv.label(self.btn_detail)
        label.set_text(i18n.Button.view_detail)
        label.set_style_text_color(colors.DS.PRIMARY, lv.PART.MAIN)
        label.center()
        self.btn_detail.add_event_cb(self.on_click_detail, lv.EVENT.CLICKED, None)

        # reject button
        self.btn_reject = self.btn_left
        self.btn_reject.color(colors.DS.WHITE)
        self.btn_reject.text_color(colors.DS.DANGER)
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

class HoldConfirmAction(HolderConfirm):
    def __init__(self, msg: str):
        super().__init__()
        label = lv.label(self.content)
        label.set_width(lv.pct(100))
        label.set_long_mode(lv.label.LONG.WRAP)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        label.set_text(msg)
        label.align(lv.ALIGN.TOP_MID, 0, 16)

        self.holder.set_text(i18n.Button.hold_to_sign)
        self.btn_cancel.set_text(i18n.Button.reject)
        self.btn_cancel.mode('reject')

class UnImplemented(with_title_and_buttons(Modal, i18n.Button.continue_)):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.unimplemented)
        self.content.set_style_pad_all(16, lv.PART.MAIN)
        label = lv.label(self.content)
        label.set_long_mode(lv.label.LONG.WRAP)
        label.set_text(i18n.Title.unimplemented)
        label.set_width(lv.pct(100))
        label.set_style_text_font(font.mono, lv.PART.MAIN)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        label.set_style_text_color(colors.DS.DANGER, lv.PART.MAIN)


       # confirm button
        self.btn_continue = self.btn_right
        self.btn_continue.add_event_cb(self.on_btn_continue, lv.EVENT.CLICKED, None)

    def on_btn_continue(self, e):
        self.close(Confirm())
