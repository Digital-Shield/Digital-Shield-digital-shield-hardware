import lvgl as lv

from . import Modal
from trezor import log, utils, workflow
from trezor.ui import i18n, Cancel, events, colors, Style, theme, font, Done
from trezor.ui.component import ArcHolder, HStack, VStack


class Confirm(Modal):
    """
    Confirm screen have 2 buttons: `cancel` and `ok`

    User can wait this screen to get result
    """

    def __init__(self):
        super().__init__()

        # `cancel` and `confirm` buttons
        self.btn_cancel = self.btn_left
        self.btn_confirm = self.btn_right
        self.btn_cancel.set_text(i18n.Button.cancel)
        self.btn_confirm.set_text(i18n.Button.confirm)

        self.btn_cancel.add_event_cb(
            lambda _: self.on_click_cancel(), lv.EVENT.CLICKED, None
        )

        self.btn_confirm.add_event_cb(
            lambda _: self.on_click_confirm(), lv.EVENT.CLICKED, None
        )

    def on_click_confirm(self):
        log.debug(__name__, "Confirm click ok")
        from trezor.ui import Confirm
        self.close(Confirm())

    def on_click_cancel(self):
        log.debug(__name__, "Confirm click cancel")
        self.close(Cancel())

class SimpleConfirm(Confirm):
    """
    Confirm with a message
    """

    def __init__(self, message: str):
        super().__init__()
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        self.content: lv.obj
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.create_content(lv.obj)
        self.content: lv.obj

        self.content.add_style(theme.Styles.board, lv.PART.MAIN)


        self.text = self.add(lv.label)
        self.text.set_long_mode(lv.label.LONG.WRAP)
        self.text.set_width(lv.pct(90))
        self.text.set_height(lv.SIZE.CONTENT)
        self.text.set_text(message)
        self.text.set_style_text_color(colors.DS.WHITE, 0)
        self.text.set_style_text_line_space(8, 0)
        self.text.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        cur_language = i18n.using.code if i18n.using is not None else None
        #阿拉伯语情况下
        if cur_language == "al":
            self.text.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置显示方向为从右向左
        self.text.center()

    def text_color(self, color):
        self.text.set_style_text_color(color, 0)


class HolderConfirm(Confirm):
    """
    Confirm with a message with a holder button, when user press `holder` button enough time,
    `ok` button will be enabled
    """

    def __init__(self,title, msg=None, chain_name=None):
        super().__init__()
        self.icon_path = None
        #判断链的图片路径
        if chain_name == "Bitcoin":
            self.icon_path = "A:/res/btc-btc.png"
        elif chain_name == "Dogecoin":
            self.icon_path = "A:/res/btc-doge.png"
        elif chain_name == "Litecoin":
            self.icon_path = "A:/res/btc-ltc.png"
        elif chain_name == "APTOS":
            self.icon_path = "A:/res/chain-apt.png"
        elif chain_name == "Polkadot":
            self.icon_path = "A:/res/chain-dot.png"
        elif chain_name == "SOL":
            self.icon_path = "A:/res/chain-sol.png"
        elif chain_name == "SUI":
            self.icon_path = "A:/res/chain-sui.png"
        elif chain_name == "TON":
            self.icon_path = "A:/res/chain-ton.png"
        elif chain_name == "TRON":
            self.icon_path = "A:/res/chain-tron.png"
        elif chain_name == "BNB Smart Chain":
            self.icon_path = "A:/res/evm-bsc.png"
        elif chain_name == "Ethereum":
            self.icon_path = "A:/res/evm-eth.png"
        elif chain_name == "Polygon":
            self.icon_path = "A:/res/evm-matic.png"

        self.set_title("")
        # disable `ok` button, user need hold sometime on to enable `ok` button
        self.btn_left.set_style_width(400, lv.PART.MAIN)
        self.btn_left.set_style_height(89, lv.PART.MAIN)
        self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
        # self.btn_confirm.add_state(lv.STATE.DISABLED)
        # self.btn_left.add_event_cb(
        #     lambda _: self.on_click_cancel(), lv.EVENT.CLICKED, None
        # )
        self.set_style_pad_left(16, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content : HStack
        self.content.items_center()
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)
        self.content.reverse()
        self.content.set_style_pad_top(100, lv.PART.MAIN)

        #滑块效果
        self.set_style_pad_left(16, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)
        

        # 容器（重新设计布局）
        self.a_container = lv.obj(self.content)
        self.a_container.set_size(460, 700)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_pad_left(0, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 80)

        if self.icon_path:

            # 头部币种显示区域
            self.coin_area = VStack(self.a_container)
            self.coin_area.set_size(260, 45)
            # 直接对 coin_area 进行绝对定位到左上角
            self.coin_area.align(lv.ALIGN.TOP_LEFT, 0, 0)

            # Add the icon
            self.coin_icon = self.coin_area.add(lv.img)
            self.coin_icon.set_src(self.icon_path)
            self.coin_icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
            self.coin_icon.align(lv.ALIGN.LEFT_MID, 0, 0)
            self.coin_icon.set_style_clip_corner(False, lv.PART.MAIN)
            self.coin_icon.set_style_img_recolor_opa(0, lv.PART.MAIN)

            # # Add the network
            # submit_label = self.coin_area.add(lv.label)
            # submit_label.set_width(lv.pct(100))
            # submit_label.set_text(chain_name)
            # submit_label.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
            # submit_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
            # submit_label.set_style_pad_all(0, lv.PART.MAIN)
            # submit_label.set_style_pad_left(15, lv.PART.MAIN)
            # submit_label.align_to(self.coin_icon, lv.ALIGN.OUT_RIGHT_MID, 10, 0)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(400)
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(title)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        self.text1.align_to(self.coin_area, lv.ALIGN.OUT_BOTTOM_MID, 80, 30)
        
        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(msg)
        self.text2.set_style_text_line_space(10, lv.PART.MAIN)
        self.text2.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
        self.text2.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 50)

        # 替换为滑动滑块确认
        # self.btn_confirm.add_state(lv.STATE.DISABLED)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)

        self.slider = lv.slider(self.a_container)
        self.slider.set_width(260)
        self.slider.set_height(66)
        self.slider.set_range(0, 280)
        self.slider.set_value(0, lv.ANIM.OFF)
       
        self.slider.set_pos(100, 460)  # 距离左边100px，距离上方150px（可根据实际UI调整）
        self.slider.set_style_border_width(0, lv.PART.MAIN)
        # 设置滑动条背景为灰色
        self.slider.add_style(Style().bg_color(colors.DS.GRAY).radius(60), lv.PART.MAIN)
        # 设置滑块为白色
        self.slider.add_style(Style().bg_color(colors.DS.WHITE).radius(60), lv.PART.KNOB)
        self.slider.add_style(Style().bg_img_src("A:/res/wipe_button.png"), lv.PART.KNOB)
        #滑过的轨道的颜色设置蓝色
        self.slider.add_style(Style().bg_color(lv.color_hex(0x0062CE)), lv.PART.INDICATOR)
        # self.slider.add_event_cb(self.on_slider_changed, lv.EVENT.VALUE_CHANGED, None)

        # 新增：松开时如果没滑到头就回弹
        def on_slider_released(event):
            slider = event.get_target()
            value = slider.get_value()
            def update_confirm(timer):
                timer._del()
                print("执行了确认")
                # 滑到头，触发确认按钮的回调
                lv.event_send(self.btn_confirm, lv.EVENT.CLICKED, None)
            if value >= 260:
                if value >= 200:
                    #改变slider背景图片
                    print("改变slider背景图片")
                    self.slider.set_style_bg_img_src("A:/res/wipe_button_ok.png", lv.PART.KNOB)
                    #暂停1秒
                    self._timer = lv.timer_create(update_confirm, 500, None)
            else:
                slider.set_value(0, lv.ANIM.ON)
                self.slider_label.set_style_text_opa(255, lv.PART.MAIN)
    
        self.slider.add_event_cb(on_slider_released, lv.EVENT.RELEASED, None)

        # 添加提示文本
        self.slider_label = lv.label(self.slider)
        self.slider_label.set_text(i18n.Button.hold_to_sign)
        self.slider_label.add_style(
            Style().bg_color(colors.DS.GRAY).radius(60).text_color(lv.color_hex(0xFFFFFF)),
            lv.PART.MAIN
        )
        self.slider_label.add_style(Style().text_opa(255), lv.PART.MAIN)
        def on_slider_value_changed(event):
            slider = event.get_target()
            value = slider.get_value()
            opa = max(0, 255 - round(value / 230) * 255)  # 计算不透明度，使文本在滑动块向右滑动时淡出
            self.slider_label.set_style_text_opa(opa, lv.PART.MAIN)

        self.slider.add_event_cb(on_slider_value_changed, lv.EVENT.VALUE_CHANGED, None)
        # 滑块弹回后文字淡入
        def on_slider_anim_end(event):
            slider = event.get_target()
            if slider.get_value() == 0:
                self.slider_label.set_style_text_opa(255, lv.PART.MAIN)

        self.slider.add_event_cb(on_slider_anim_end, lv.EVENT.VALUE_CHANGED, None)
        self.slider_label.center()
        # `content` is remained, for draw all other ui components
        # self.create_content(lv.obj)
        # self.content.set_flex_grow(1)
    # def on_click_cancel(event):
    #     from .template import mLart
    #     screen = mLart(i18n.Button.cancel)
    #     workflow.spawn(screen.show())
    # def on_slider_changed(self, event):
    #         slider = event.get_target()
    #         value = slider.get_value()
    #         if value >= 100:
    #             self.btn_confirm.clear_state(lv.STATE.DISABLED)
    #         else:
    #             self.btn_confirm.add_state(lv.STATE.DISABLED)
                
class WordCheckConfirm(Confirm):
    """
    Confirm with a message
    """

    def __init__(self, title: str, message: str, icon: str|None=None,left_btn_hidden=True,right_word=i18n.Button.continue_):
        super().__init__()
        self.set_title("")
        # self.title = title
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        self.btn_left.set_text(i18n.Button.cancel)
        self.btn_left.set_style_width(214, lv.PART.MAIN)
        self.btn_left.set_style_height(89, lv.PART.MAIN)
        self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.set_text(right_word)
        self.btn_right.set_style_width(214, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
         # 隐藏原有的btn_right按钮
        if left_btn_hidden:
            self.btn_left.add_flag(lv.obj.FLAG.HIDDEN)
            self.btn_right.set_style_width(440, lv.PART.MAIN)
            self.btn_right.set_style_height(89, lv.PART.MAIN)
        
        # #判断self.btn_left是否隐藏
        # if left_btn_hidden:
        #     self.btn_right.set_width(lv.pct(90))
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
            self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 160)
        else:
            self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 30)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(title)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        # self.text1.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        # self.text1.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(message)
        self.text2.set_style_text_line_space(10, lv.PART.MAIN)
        self.text2.set_style_text_font(font.Bold.SCS30, lv.PART.MAIN)
        self.text2.set_style_text_color(colors.DS.WHITE, 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 90)

        # self.text.set_text("")
        # view = self.add(Text)
        # view.set_label(title)
        # view.set_text(desc)
        self.btn_confirm.add_event_cb(
            lambda _: self.on_click_confirm(), lv.EVENT.CLICKED, None
        )
        # self.btn_left.add_event_cb(
        #     lambda _: self.on_click_cancel(), lv.EVENT.CLICKED, None
        # )
    #     #点击确认
    def on_click_confirm(self):
        print("on_click_confirm")
        if self.title == i18n.Title.stop_checking:
            from trezor.ui.screen import manager
            manager.mark_dismissing(self)
            from trezor.ui import NavigationBack
            self.channel.publish(NavigationBack())
        else:
            from trezor.ui import Confirm
            self.close(Confirm())
            self.close(Done())
    # # #点完成则返回
    # def on_click_cancel(self):
    #     # self.close(Cancel())
    #     from trezor.ui import NavigationBack
    #     self.channel.publish(NavigationBack())

class CompleteConfirm(Confirm):
    """
    Confirm with a message
    """

    def __init__(self, title: str, message: str, icon: str|None=None,left_btn_hidden=True,right_word=i18n.Button.continue_):
        super().__init__()
        self.set_title("")
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        self.btn_left.set_text(i18n.Button.cancel)
        self.btn_left.set_style_width(214, lv.PART.MAIN)
        self.btn_left.set_style_height(89, lv.PART.MAIN)
        self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.set_text(right_word)
        self.btn_right.set_style_width(214, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
         # 隐藏原有的btn_right按钮
        if left_btn_hidden:
            self.btn_left.add_flag(lv.obj.FLAG.HIDDEN)
            self.btn_right.set_style_width(440, lv.PART.MAIN)
            self.btn_right.set_style_height(89, lv.PART.MAIN)
        
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
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_pad_left(40, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        if icon:
            self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 160)
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
    # 点击完成
    def on_click_confirm(self):
        # self.close(Done())
        from trezor import workflow
        from .home.security import SecurityApp
        workflow.spawn(SecurityApp().show())

class UpdateCheckConfirm(Confirm):

    def __init__(self, title: str, message: str, names: str|None=None,left_btn_hidden=True):
        super().__init__()
        self.set_title("")
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        self.btn_left.set_text(i18n.Button.cancel)
        self.btn_left.set_style_width(214, lv.PART.MAIN)
        self.btn_left.set_style_height(89, lv.PART.MAIN)
        self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.set_text(i18n.Button.confirm)
        self.btn_right.set_style_width(214, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
         # 隐藏原有的btn_right按钮
        if left_btn_hidden:
            self.btn_left.add_flag(lv.obj.FLAG.HIDDEN)
            self.btn_right.set_style_width(440, lv.PART.MAIN)
            self.btn_right.set_style_height(89, lv.PART.MAIN)
        # if icon:
        #     self.icon = self.add(lv.img)
        #     self.icon.set_src(icon)
        #     self.icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        #     # 使用绝对定位到左上角
        #     # self.icon.align(lv.ALIGN.TOP_LEFT, 10, 0)
        #     self.icon.set_style_pad_left(40, lv.PART.MAIN)
        #     self.icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
        #     self.icon.set_zoom(256)  # 1.0x zoom, ensures full image is shown
        #     self.icon.clear_flag(lv.obj.FLAG.CLICKABLE)
        #     self.icon.set_style_clip_corner(False, lv.PART.MAIN)
        
         # 容器（重新设计布局）
        self.a_container = lv.obj(self)
        self.a_container.set_size(460, 260)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_pad_left(40, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        # if icon:
        #     self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 160)
        # else:
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 10)

        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(title)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        # self.text1.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        # self.text1.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        # self.text.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(400)
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(message)
        self.text2.set_style_text_line_space(10, lv.PART.MAIN)
        self.text2.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
        self.text2.set_style_text_color(colors.DS.WHITE, 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 60)

        if names:
            self.text3 = lv.label(self.a_container)
            self.text3.set_long_mode(lv.label.LONG.WRAP)
            self.text3.set_width(400)
            self.text3.set_height(lv.SIZE.CONTENT)
            self.text3.set_text(names)
            self.text3.set_style_text_line_space(10, lv.PART.MAIN)
            self.text3.set_style_text_font(font.Regular.SCS30, lv.PART.MAIN)
            self.text3.set_style_text_color(colors.DS.WHITE, 0)
            self.text3.align_to(self.text2,lv.TEXT_ALIGN.LEFT, 0, 40)

