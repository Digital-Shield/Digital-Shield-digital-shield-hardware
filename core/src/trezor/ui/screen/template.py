import lvgl as lv

from trezor import log, workflow
from trezor.ui import i18n, font, colors, theme, Style
from trezor.ui import Confirm, Reject, Cancel, Detail
from trezor.ui.screen import Modal
from trezor.ui.screen.confirm import HolderConfirm
from trezor.ui.component import HStack, LabeledText, VStack

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    AddressState = Literal["address", "qrcode"]

class Address(Modal):
    def __init__(
        self, address: str, path: str, network: str, chain_id: int | None = None
    ):
        super().__init__()
        # self.set_title(i18n.Title.address.format(network))
        self.btn_left.set_style_width(214, lv.PART.MAIN)
        self.btn_left.set_style_height(89, lv.PART.MAIN)
        self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.set_style_width(214, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色

        self.btn_toggle = self.btn_left
        self.btn_confirm = self.btn_right
        self.btn_toggle.set_text(i18n.Button.qr_code)
        self.btn_confirm.set_text(i18n.Button.confirm)

        self.address = address
        self.icon_path = ""
        self.path = path
        self.network = network
        self.chain_id = chain_id

        #判断链的图片路径
        if self.network == "Bitcoin":
            self.icon_path = "A:/res/btc-btc.png"
        elif self.network == "Dogecoin":
            self.icon_path = "A:/res/btc-doge.png"
        elif self.network == "Litecoin":
            self.icon_path = "A:/res/btc-ltc.png"
        elif self.network == "APTOS":
            self.icon_path = "A:/res/chain-apt.png"
        elif self.network == "Polkadot":
            self.icon_path = "A:/res/chain-dot.png"
        elif self.network == "SOL":
            self.icon_path = "A:/res/chain-sol.png"
        elif self.network == "SUI":
            self.icon_path = "A:/res/chain-sui.png"
        elif self.network == "TON":
            self.icon_path = "A:/res/chain-ton.png"
        elif self.network == "TRON":
            self.icon_path = "A:/res/chain-tron.png"
        elif self.network == "BNB Smart Chain":
            self.icon_path = "A:/res/evm-bsc.png"
        elif self.network == "Ethereum":
            self.icon_path = "A:/res/evm-eth.png"
        elif self.network == "Polygon":
            self.icon_path = "A:/res/evm-matic.png"
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

        # 头部币种显示区域
        self.coin_area = view.add(VStack)
        self.coin_area.set_size(260, 45)
        self.coin_area.align(lv.ALIGN.TOP_LEFT, 10,180)
        # Create a horizontal stack container for alignment
        
        # Add the icon
        self.coin_icon = self.coin_area.add(lv.img)
        self.coin_icon.set_src(self.icon_path)
        # Remove fixed size and zoom, let LVGL use image's natural size
        self.coin_icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        self.coin_icon.align(lv.ALIGN.TOP_LEFT, 0, 0)
        self.coin_icon.set_style_clip_corner(False, lv.PART.MAIN)
        self.coin_icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
        self.coin_icon.set_style_pad_bottom(2, lv.PART.MAIN)
        # Remove zoom to avoid cropping, show full image

        # Add the label
        submit_label = self.coin_area.add(lv.label)
        submit_label.set_width(lv.pct(100))
        submit_label.set_text(self.network)
        submit_label.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        submit_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        submit_label.set_style_pad_all(0, lv.PART.MAIN)
        submit_label.set_style_pad_left(15, lv.PART.MAIN)
        submit_label.center()

        label = view.add(lv.label)
        label.set_text(i18n.Button.address)
        label.set_long_mode(lv.label.LONG.WRAP)
        label.set_width(lv.pct(100))
        label.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
        label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN) #地址白色
        label.add_style(LabeledText.style, lv.PART.MAIN)
        #上边距10
        label.set_style_pad_top(10, lv.PART.MAIN)

         # 地址分段显示的spana容器
        self.spans = lv.spangroup(view)
        self.spans.set_width(lv.pct(100))
        self.spans.set_height(lv.SIZE.CONTENT)
        self.spans.set_mode(lv.SPAN_MODE.BREAK)
        self.spans.add_style(LabeledText.style, lv.PART.MAIN)
        # self.spans.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
        # self.spans.set_style_border_width(1, lv.PART.MAIN)
        self.spans.set_style_pad_top(-5, lv.PART.MAIN)

        span = self.spans.new_span()
        span.set_text(self.address[:4])
        span.style.set_text_font(font.Bold.SCS38)
        span.style.set_text_color(lv.color_hex(0x2A5CFF))
        span.style.set_text_letter_space(0)
        span.style.set_text_line_space(0)
        span.style.set_text_decor(0)
        span.style.set_text_align(lv.TEXT_ALIGN.LEFT)

        span = self.spans.new_span()
        span.set_text(self.address[4:19])
        span.style.set_text_font(font.Bold.SCS38)
        span.style.set_text_color(lv.color_hex(0xFFFFFF))

        span = self.spans.new_span()
        span.set_text(self.address[19:-4])
        span.style.set_text_font(font.Bold.SCS38)
        span.style.set_text_color(lv.color_hex(0xFFFFFF))

        span = self.spans.new_span()
        span.set_text(self.address[-4:])
        span.style.set_text_font(font.Bold.SCS38)
        span.style.set_text_color(lv.color_hex(0x2A5CFF))

        # `address`
        # label = view.add(lv.label)
        # label.set_text(self.address)
        # label.set_long_mode(lv.label.LONG.WRAP)
        # label.set_width(lv.pct(100))
        # label.set_style_text_font(font.mono, lv.PART.MAIN)
        # label.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN) #地址白色
        # label.add_style(LabeledText.style, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = view.add(LabeledText)
            item.set_label(label)
            item.set_text(text)
            item.set_style_text_color(colors.STD.WHITE, lv.PART.MAIN) #地址白色
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
        
        view = self.add(HStack)
        view.add_style(theme.Styles.board, lv.PART.MAIN)
        view.set_height(lv.SIZE.CONTENT)
        
         # 头部币种显示区域
        self.coin_area = view.add(VStack)
        self.coin_area.set_size(260, 45)
        self.coin_area.align(lv.ALIGN.TOP_LEFT, 10,180)
        # Create a horizontal stack container for alignment
        
        # Add the icon
        self.coin_icon = self.coin_area.add(lv.img)
        self.coin_icon.set_src(self.icon_path)
        # Remove fixed size and zoom, let LVGL use image's natural size
        self.coin_icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        self.coin_icon.align(lv.ALIGN.TOP_LEFT, 0, 0)
        self.coin_icon.set_style_clip_corner(False, lv.PART.MAIN)
        self.coin_icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
        self.coin_icon.set_style_pad_bottom(2, lv.PART.MAIN)
        # Remove zoom to avoid cropping, show full image

        # Add the label
        submit_label = self.coin_area.add(lv.label)
        submit_label.set_width(lv.pct(100))
        submit_label.set_text(self.network)
        submit_label.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        submit_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        submit_label.set_style_pad_all(0, lv.PART.MAIN)
        submit_label.set_style_pad_left(15, lv.PART.MAIN)
        submit_label.center()

        # 二维码容器（居中布局）
        self.qrcode_container = view.add(lv.obj)
        self.qrcode_container.set_size(360, 360)
        self.qrcode_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.qrcode_container.set_style_shadow_width(0, lv.PART.MAIN)
        self.qrcode_container.set_style_outline_width(0, lv.PART.MAIN)
        self.qrcode_container.align(lv.ALIGN.TOP_LEFT, 50, 184)  # 调整垂直位置
        self.qrcode_container.set_style_border_width(0, lv.PART.MAIN)
        
        view2 = lv.qrcode(self.qrcode_container, 312, colors.DS.BLACK, colors.DS.WHITE)
        view2.set_style_border_width(16, lv.PART.MAIN)
        #去除二维码内部白边
        view2.set_style_shadow_width(0, lv.PART.MAIN)
        view2.set_style_outline_width(0, lv.PART.MAIN)
        view2.set_style_radius(24, lv.PART.MAIN)
        view2.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
        view2.update(self.address, len(self.address))
        view2.center()
        # 在二维码中心添加icon图片
        icon_path = "A:/res/dunan.png"
        self.icon_img = lv.img(self.qrcode_container)
        self.icon_img.set_src(icon_path)
        # 保证图片完整显示
        self.icon_img.set_zoom(300)  # 1.0倍缩放，防止裁剪
        self.icon_img.set_style_img_opa(lv.OPA.COVER, 0)
        self.icon_img.set_style_img_recolor_opa(lv.OPA.TRANSP, 0)
        self.icon_img.set_style_clip_corner(0, 0)
        # 添加白色四方形背景容器（无边框）
        self.bg_container = lv.obj(self.qrcode_container)
        self.bg_container.set_size(60, 60)
        self.bg_container.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.bg_container.set_style_radius(16, lv.PART.MAIN)  # 四方形，无圆角
        self.bg_container.set_style_border_width(0, lv.PART.MAIN)
        self.bg_container.set_style_border_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 彻底隐藏边框
        self.bg_container.set_style_shadow_width(0, lv.PART.MAIN)
        self.bg_container.align_to(view2, lv.ALIGN.CENTER, 0, 0)
        self.bg_container.move_foreground()
        # 将icon图片放到背景容器上方并居中
        self.icon_img.align_to(self.bg_container, lv.ALIGN.CENTER, 0, 0)
        self.icon_img.move_foreground()
        # 居中到二维码中心
        # icon_img.align_to(view, lv.ALIGN.CENTER, 0, 0)
        # 置于二维码之上
        # icon_img.move_foreground()

        # view = lv.qrcode(self.content, 400, colors.DS.BLACK, colors.DS.WHITE)
        # view.update(self.address, len(self.address))
        # view.set_style_border_width(16, lv.PART.MAIN)
        # view.set_style_border_color(colors.DS.WHITE, lv.PART.MAIN)
        # view.center()
        self._qrcode_view = view
        return self._qrcode_view

    def on_click_toggle(self, e):
        label: lv.label = self.btn_toggle.get_child(0)
        # print("address---"+self.state)
        if self.state == "qrcode":
            self.state = "address"
            label.set_text(i18n.Button.qr_code)
            self.address_view.clear_flag(lv.obj.FLAG.HIDDEN)
            self.qrcode_view.add_flag(lv.obj.FLAG.HIDDEN)
        else:
            self.state = "qrcode"
            label.set_text(i18n.Button.address)
            self.qrcode_view.clear_flag(lv.obj.FLAG.HIDDEN)
            self.address_view.add_flag(lv.obj.FLAG.HIDDEN)

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

class Blob(Modal):
    """
    A `Modal` contain: `message`, `label`: `blob`
    """
    def __init__(self, title: str, message: str, *, label: str|None = None, blob: str|bytes|None = None):
        super().__init__()

        self.set_title(title)
        # self.btn_right.set_text(i18n.Button.continue_)
        # self.btn_right.set_text(i18n.Button.cancel)
        self.btn_right.set_text(i18n.Button.continue_)  # 设置“继续”按钮
        self.btn_left.set_text(i18n.Button.cancel)      # 设置“取消”按钮
        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        if message:
            item = self.add(lv.label)
            item.set_width(lv.pct(100))
            item.set_long_mode(lv.label.LONG.WRAP)
            item.set_text(message)
            item.set_style_text_color(colors.DS.WHITE, lv.PART.MAIN)
        if label is not None:
            item = self.add(LabeledText)
            item.set_label(label)
            if isinstance(blob,(bytes, bytearray)):
                from ubinascii import hexlify
                blob = '0x'+hexlify(blob).decode()

        item.set_text(blob)
        item.set_style_text_color(colors.DS.WHITE, lv.PART.MAIN)
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


class SignMessage(Modal):
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
        self.btn_right.set_text(i18n.Button.sign)
        self.btn_left.set_text(i18n.Button.reject)

        self.content.set_style_pad_all(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        def labeled(label: str, text: str):
            item = LabeledText(self.content)
            item.set_label(label)
            item.set_text(text)
            item.set_style_text_color(colors.STD.RED, lv.PART.MAIN) 
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

class TransactionOverview(Modal):
    def __init__(self, network: str, amount: str, to: str, icon: str):
        super().__init__()
        self.set_title(i18n.Title.transaction.format(network), icon)
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
        self.btn_reject.mode('reject')
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

class TransactionOverviewTon(Modal):
    def __init__(self, network: str, amount: str, to: str, icon: str):
        super().__init__()
        self.set_title(i18n.Title.transaction.format(network), icon)
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

    def on_click_detail(self, e):
        self.close(Detail())

    def on_click_reject(self, e):
        self.close(Reject())

    def on_click_confirm(self, e):
        self.close(Confirm())

class HoldConfirmAction(HolderConfirm):
    def __init__(self, title:str, msg: str, chain_name:str=""):
        super().__init__(title, msg, chain_name)
        label = lv.label(self.content)
        label.set_width(lv.pct(100))
        label.set_long_mode(lv.label.LONG.WRAP)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        label.set_text("")
        label.align(lv.ALIGN.TOP_MID, 0, 16)

        # self.holder.set_text(i18n.Button.hold_to_sign)
        self.btn_cancel.set_text(i18n.Button.cancel)
        # self.btn_cancel.mode('reject')
        # 添加事件回调，拒绝后跳转到某UI页面
        # def on_cancel(e):
        #     from trezor.ui.screen import manager
        #     manager.mark_dismissing(self)
        #     screen = mLart(i18n.Title.sign_fail,i18n.Text.sign_fail,"A:/res/word_error.png")
        #     workflow.spawn(screen.show())
        #     #关闭Scan页面
        # self.btn_cancel.add_event_cb(on_cancel, lv.EVENT.CLICKED, None)

#拒绝确认页
class mLart(Modal):

    def __init__(self, title: str, message: str, icon: str|None=None):
        super().__init__()
        # 隐藏原有的btn_right按钮
        self.btn_right.add_flag(lv.obj.FLAG.HIDDEN)

        # 新建一个底部居中的按钮
        self.btn_bottom = self.add(lv.btn)
        self.btn_bottom.set_width(400)
        self.btn_bottom.set_height(89)
        self.btn_bottom.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self.btn_bottom.set_style_radius(60, lv.PART.MAIN)
        self.btn_bottom.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)
        self.btn_bottom_label = lv.label(self.btn_bottom)
        self.btn_bottom_label.set_text(i18n.Button.done)
        self.btn_bottom_label.center()
        self.btn_bottom.add_event_cb(
            lambda _: self.on_click_ok(), lv.EVENT.CLICKED, None
        )

        if icon:
            self.icon = self.add(lv.img)
            self.icon.set_src(icon)
            self.icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
            # 使用绝对定位到左上角
            # self.icon.align(lv.ALIGN.TOP_LEFT, 10, 0)
            self.icon.set_style_pad_left(40, lv.PART.MAIN)
            self.icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
            self.icon.set_zoom(256)  # 1.0x zoom, ensures full image is shown
            self.icon.clear_flag(lv.obj.FLAG.CLICKABLE)
            self.icon.set_style_clip_corner(False, lv.PART.MAIN)
        
         # 容器（重新设计布局）
        self.a_container = lv.obj(self)
        self.a_container.set_size(460, 400)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_pad_left(40, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        if icon:
            self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 100)
        else:
            self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 30)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(title)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_text_font(font.Medium.SCS40, lv.PART.MAIN)
        # self.text1.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        # self.text1.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(message)
        self.text2.set_style_text_line_space(10, lv.PART.MAIN)
        self.text2.set_style_text_font(font.Medium.SCS28, lv.PART.MAIN)
        self.text2.set_style_text_color(colors.DS.WHITE, 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 60)
        # self.text.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
    #点完成则返回
    def on_click_ok(self):
        from trezor.ui import NavigationBack
        self.channel.publish(NavigationBack())
        from . import manager
        from trezor import workflow
        workflow.spawn(manager.pop(self))

class UnImplemented(Modal):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Title.unimplemented)
        self.btn_right.set_text(i18n.Button.continue_)
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
