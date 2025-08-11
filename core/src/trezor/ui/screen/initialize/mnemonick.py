import lvgl as lv

from . import *
from trezor import utils, log, loop, wire
from trezor.enums import MessageType, BackupType
from trezor.ui import i18n, Style, colors, Redo, font, Done
from trezor.ui.screen import Modal, Navigation
from trezor.ui.theme import Styles
from trezor.ui.component import HStack, VStack
from trezor.ui.component import MnemonicKeyboard
from trezor.ui import i18n, Cancel, Confirm
from trezor.ui.screen.confirm import SimpleConfirm
from trezor import workflow

from trezor.crypto import random

from trezor.ui.types import *

class MnemonicInputs(Navigation):
    def __init__(self, count, mnemonics):
        super().__init__()
        self.count = count
        self.current_index = 0
        self.come_source = "mnemonic_input"
        self.mnemonics: list[str] = [""] * count
        print("接收到的mnemonics:",mnemonics)
        self.mnemonics = mnemonics.split(" ")
        
        # 设置黑色背景
        self.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)
        
        # 隐藏默认按钮
        self.btn_left.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_right.add_flag(lv.obj.FLAG.HIDDEN)
        
        # 主内容区
        self.create_content(VStack)
        self.content: VStack
        self.content.set_style_pad_all(16, lv.PART.MAIN)
        
        # 单词输入区域
        self.create_word_input()
        
        # 提交按钮
        self.create_submit_button()
        
        # 初始化显示
        self.update_next_status(self.current_index)

        self.show_invalid_mnemonic()

        # self.update_display()

    def create_word_input(self):
        """创建单词输入区域"""
        # 容器
        self.word_container = lv.obj(self.content)
        self.word_container.set_size(lv.pct(100), 400)
        self.word_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        
        # 单词序号
        self.index_label = lv.label(self.word_container)
        self.index_label.set_text("单词 #1")
        self.index_label.align(lv.ALIGN.TOP_LEFT, 0, 0)
        self.index_label.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        self.index_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        
        # 输入框（白色边框）
        self.word_input = lv.textarea(self.word_container)
        self.word_input.set_size(lv.pct(100),90)
        self.word_input.align_to(self.index_label, lv.ALIGN.OUT_BOTTOM_LEFT,0, 20)
        self.word_input.set_placeholder_text("输入单词...")
        self.word_input.set_one_line(True)
        self.word_input.set_style_border_width(1, lv.PART.MAIN)
        self.word_input.set_style_bg_color(lv.color_hex(0x888888), lv.PART.MAIN)
        self.word_input.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        self.word_input.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.word_input.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)  # 禁用滚动条
        self.item = Item_input(self.word_input, index=0)
        self.item.add_style(
            Style()
            .pad_top(0)
            .pad_bottom(0),
            lv.PART.MAIN,
        )
        self.item.clickable = True
        self.word_input.add_event_cb(self.on_click_item, lv.EVENT.CLICKED, None)
        self.input = None
        self._updating = False
        self.success_sign = 0

        # 导航箭头
        self.prev_btn = lv.btn(self.word_container)
        self.prev_btn.set_size(35, 35)
        self.prev_btn.align(lv.ALIGN.RIGHT_MID, -50, -160)
        self.prev_btn.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.prev_btn.set_style_shadow_width(0, lv.PART.MAIN)
        self.prev_img = lv.img(self.prev_btn)
        self.prev_img.set_src("A:/res/prev_grey.png")
        self.prev_img.set_size(44, 44)
        self.prev_img.align(lv.ALIGN.CENTER, 0, 0)
        self.prev_btn.add_event_cb(self.on_prev_clicked, lv.EVENT.CLICKED, None)
        
        self.next_btn = lv.btn(self.word_container)
        self.next_btn.set_size(35, 35)
        self.next_btn.align(lv.ALIGN.RIGHT_MID, 0, -160)
        self.next_btn.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.next_btn.set_style_shadow_width(0, lv.PART.MAIN)
        self.next_img = lv.img(self.next_btn)
        self.next_img.set_src("A:/res/next_grey.png")
        self.next_img.set_size(44, 44)
        self.next_img.align(lv.ALIGN.CENTER, 0, 0)
        self.next_btn.add_event_cb(self.on_next_clicked, lv.EVENT.CLICKED, None)
        
        if self.mnemonics[self.current_index]:
            self.update_next_status(self.current_index)

    def on_click_item(self, event):
        target: Item = event.target
        item = self.item
        item.inputting = True
        self.popup_input(item)

    def popup_input(self, item: 'Item'):
        log.debug(__name__, f"popup input for {item.index}")
        if self.input:
            return

        index = item.index
        self.input = Input(self, index)
        self.input.add_event_cb(lambda e: self.close_input(), lv.EVENT.CANCEL, None)
        self.input.add_event_cb(self.on_input_ready, lv.EVENT.READY, None)

    def on_input_ready(self, event):
        log.debug(__name__, "input ready")
        word = self.input.ta.get_text()
        print("input ready word:", word)
        item = self.item
        assert item is not None
        item.word = word

        index = item.index
        index += 1
        item = self.item
        
        if item.word:
            self.close_input()
            self.update_display(word)
            # return

        lv.event_send(item, lv.EVENT.CLICKED, None)

    def close_input(self):
        log.debug(__name__, "close input")
        if not self.input:
            return

        item = self.item
        if item:
            item.inputting = False

        self.input.delete()
        self.input = None

    def create_submit_button(self):
        """创建提交按钮"""
        self.submit_btn = lv.btn(self.word_container)
        self.submit_btn.set_size(120, 40)
        self.submit_btn.align(lv.ALIGN.TOP_LEFT, 10,180)
        self.submit_btn.set_style_bg_color(lv.color_hex(0x2A5CFF), lv.PART.MAIN)
        submit_label = lv.label(self.submit_btn)
        submit_label.set_text("已提交")
        submit_label.center()
        self.submit_btn.add_flag(lv.obj.FLAG.HIDDEN)  # 初始隐藏

    def update_display(self, word: str = ""):
        """更新界面显示（避免递归）"""
        # if self._updating:
        #     return
            
        self._updating = True
        self.success_sign = 0
        try:
            self.mnemonics[self.current_index] = word
            print("self.current_word:", word)
            print("self.mnemonics:", self.mnemonics)
            
            if self.mnemonics[self.current_index]:
                self.remaining_time = 2
                def update_countdown(timer):
                    self.remaining_time -= 1
                    # if self.remaining_time > 0:
                    #     self.submit_btn.clear_flag(lv.obj.FLAG.HIDDEN)
                    # else:
                    timer._del()
                    if self.current_index < len(self.mnemonics)-1 and self.come_source == "mnemonic_input":
                        self.current_index = self.current_index + 1
                        self.item.word = self.mnemonics[self.current_index] if self.mnemonics[self.current_index] else ""
                        print("self.current_index_id:",self.current_index)
                        self.update_next_status(self.current_index)
                        lv.event_send(self.word_input, lv.EVENT.CLICKED, None)
                        self.mnemonics = ['report', 'deposit', 'grape', 'priority', 'network', 'palm', 'sponsor', 'vivid', 'involve', 'attract', 'source', 'embrace']
                    
                    non_empty_count = sum(1 for item in self.mnemonics if item)
                    if non_empty_count == self.count:# and self.come_source == "mnemonic_input"
                        # 清理可能存在的无效助记词界面
                        if hasattr(self, 'invalid_screen') and self.invalid_screen:
                            self.invalid_screen.delete()
                            self.invalid_screen = None
                        
                        # 检验助记词是否正确
                        from trezor.errors import MnemonicError
                        try:
                            from apps.management.recovery_device import recover
                            mnemonic_str = " ".join(self.mnemonics)
                            # print("mnemonic_str:", mnemonic_str)
                            secret: bytes | None = recover.process_bip39(mnemonic_str)
                            # print("secret:", secret)
                            # print("self.come_source", self.come_source)
                            # from trezor.ui import NavigationBack
                            self.channel.publish(self.mnemonics)
                            # self.btn_right.add_event_cb(lambda _: self.close(Done()), lv.EVENT.CLICKED, None)
                            # lv.event_send(self.btn_right, lv.EVENT.CLICKED, None)
                            # workflow.spawn(self.show_success_screen())
                            self.success_sign = 1
                            return
                        except MnemonicError:
                            print("MnemonicError")
                            # workflow.spawn(self.show_invalid_mnemonic())
                            self.show_invalid_mnemonic()
                            
                        print("success_sign",self.success_sign)
                                
                
                self._timer = lv.timer_create(update_countdown, 500, None)
                
        finally:
            self._updating = False
    
    
    async def show_success_screen(self):
        """错误提示页面"""
        screen = SimpleConfirm("单词正确。")
        screen.btn_confirm.set_text("确认")
        # screen.btn_cancel.delete()
        try:
            await screen.show()
        except Exception as e:
            print("Exception:", e)
        screen.btn_confirm.add_event_cb(self.on_confirm, lv.EVENT.CLICKED, None)
    def on_confirm(self, event):
            from trezor.ui import NavigationBack
            print("on_confirm")
            self.channel.publish(NavigationBack())
            self.channel.publish(Redo())

    def update_next_status(self, current_index: int):
        """更新导航按钮状态"""
        self.item.word = self.mnemonics[self.current_index] if self.mnemonics[self.current_index] else ""
        self.index_label.set_text(f"单词 #{current_index + 1}")
        self.word_input.set_text(self.item.word)  # 确保输入框显示正确内容
        
        non_empty_count = sum(1 for item in self.mnemonics if item)
        self.prev_img.set_src("A:/res/prev_white.png") if current_index > 0 else self.prev_img.set_src("A:/res/prev_grey.png")
        self.next_img.set_src("A:/res/next_white.png") if current_index < non_empty_count else self.next_img.set_src("A:/res/next_grey.png")
        # self.submit_btn.add_flag(lv.obj.FLAG.HIDDEN)
        lv.event_send(self.word_input, lv.EVENT.CLICKED, None)

    def on_prev_clicked(self, e):
        """上一个单词"""
        if self.current_index > 0:
            self.current_index -= 1
            self.item.word = self.mnemonics[self.current_index]
            self.update_next_status(self.current_index)

    def on_next_clicked(self, e):
        if self.current_index == self.count - 1 and self.come_source == "invalid":
            # 清理可能存在的无效助记词界面
            if hasattr(self, 'invalid_screen') and self.invalid_screen:
                self.invalid_screen.delete()
                self.invalid_screen = None
            
            # 检验助记词是否正确
            from trezor.errors import MnemonicError
            try:
                from apps.management.recovery_device import recover
                mnemonic_str = " ".join(self.mnemonics)
                print("mnemonic_str:", mnemonic_str)
                secret: bytes | None = recover.process_bip39(mnemonic_str)
                print("secret:", secret)
                self.channel.publish(self.mnemonics)
            except MnemonicError:
                print("MnemonicError")
                self.show_invalid_mnemonic()
        else:
            if self.current_index < self.count - 1:
                self.current_index += 1
                if self.mnemonics[self.current_index]:
                    self.item.word = self.mnemonics[self.current_index]
                    self.update_next_status(self.current_index)
                else:
                    if self.mnemonics[self.current_index-1]:
                        self.item.word = self.mnemonics[self.current_index]
                        self.update_next_status(self.current_index)

    def on_back_clicked(self, e):
        """返回确认"""
        async def show_confirm():
            screen = SimpleConfirm("确定要终止核对吗？")
            await screen.show()
            r = await screen
            if isinstance(r, Confirm):
                from trezor.ui import NavigationBack
                self.channel.publish(NavigationBack())
        
        # workflow.spawn(show_confirm())

    def show_invalid_mnemonic(self):
        """显示无效助记词界面（改为顶层容器）"""
        # 安全删除已存在的无效界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            self.invalid_screen.delete()
        
        # 创建新的顶层容器
        self.invalid_screen = lv.obj(self)
        self.invalid_screen.set_size(lv.pct(100), lv.pct(100))
        self.invalid_screen.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        # lv.obj_move_foreground(self.invalid_screen)  # 将对象移动到最前面
        
        # 标题
        title = lv.label(self.invalid_screen)
        title.set_text("助记词无效")
        title.set_style_text_color(lv.color_hex(0xFF0000), lv.PART.MAIN)
        title.align(lv.ALIGN.TOP_MID, 0, 20)
        
        # 描述
        desc = lv.label(self.invalid_screen)
        desc.set_text("您输入的助记词无效，点击单词进行编辑，或重新开始。")
        desc.set_width(lv.pct(80))
        desc.set_long_mode(lv.label.LONG.WRAP)
        desc.align_to(title, lv.ALIGN.OUT_BOTTOM_MID, 0, 20)
        
        # 单词列表
        word_list = VStack(self.invalid_screen)
        word_list.set_size(lv.pct(80), lv.pct(50))
        word_list.align_to(desc, lv.ALIGN.OUT_BOTTOM_MID, 0, 20)
        word_list.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        
        # 添加单词按钮
        for i, word in enumerate(self.mnemonics):
            btn = lv.btn(word_list)
            btn.set_size(120, 40)
            btn.set_style_bg_color(lv.color_hex(0x2A5CFF), lv.PART.MAIN)
            label = lv.label(btn)
            label.set_text(f"{i+1} {word}")
            label.center()
            # 创建一个对象
            obj = MyObject(i)
            # 将对象设置为用户数据
            btn.set_user_data(obj)
            btn.add_event_cb(self.on_edit_word, lv.EVENT.CLICKED, None)
        
        # 重新开始按钮
        restart_btn = lv.btn(self.invalid_screen)
        restart_btn.set_size(200, 50)
        restart_btn.align(lv.ALIGN.BOTTOM_MID, 0, -20)
        restart_btn.set_style_bg_color(lv.color_hex(0xFF0000), lv.PART.MAIN)
        restart_label = lv.label(restart_btn)
        restart_label.set_text("重新开始")
        restart_label.center()
        restart_btn.add_event_cb(self.on_restart, lv.EVENT.CLICKED, None)
        

    def on_edit_word(self, e):
        """编辑指定单词"""
        # # 获取点击的按钮
        # btn = e.get_target()
        # # 获取用户数据
        # obj = btn.data
        # if not obj:
        #     return
        #清除ee.get_target()
        # index = obj.data
        self.current_index = 11
        # print("on_edit_index", obj)
        
        # 安全删除无效助记词界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            print("删除无效助记词界面")
            self.invalid_screen.delete()
            self.invalid_screen = None
        # lv.event_send(self.btn_right, lv.EVENT.CLICKED, None)
        self.come_source = "invalid"
        self.update_next_status(self.current_index)
        # workflow.spawn(self.show_success_screen())
        # workflow.spawn(self.show())

    def on_restart(self, e):
        """重新开始输入"""
        # 安全删除无效助记词界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            # for child in self.invalid_screen.get_children():
            #     child.remove_event_cb_all()
            self.invalid_screen.delete()
            self.invalid_screen = None
        
        # 重置主界面状态
        self.mnemonics = [""] * self.count
        self.current_index = 0
        self.item.word = ""
        self.come_source = "mnemonic_input"
        self.update_next_status(self.current_index)
        # self.invalid_screen.delete()
        workflow.spawn(self.show())

class MyObject:
    def __init__(self, data):
        self.data = data

class Item_input(HStack):
    #    <index>
    #    <word>

    def __init__(self, parent, word: str | None = None, index: int | None = None):
        super().__init__(parent)
        self._word = word
        self._index = index
        self.add_style(
            Style()
            .bg_color(lv.color_hex(0x888888))  # 深色背景
            .bg_opa(lv.OPA._90)  # 90% 不透明，避免影响子组件
            .radius(16)
            .width(lv.pct(100))
            .height(96)
            .text_color(colors.DS.WHITE)
            # .border_width(1)
            .bg_opa(lv.OPA.COVER),
            lv.PART.MAIN,
        )

        self.items_center()

        self.add_style(Styles.checked, lv.PART.MAIN | lv.STATE.CHECKED)
        # we use USER_1 to mark inputting
        # not directly use lv.STATE.FOCUSED, because it will changed when `Input` popup
        self.add_style(Styles.focused, lv.PART.MAIN | lv.STATE.USER_1)

        # self.index_label = lv.label(self)
        # self.index_label.add_style(
        #     Style().text_font(font.small).text_color(colors.DS.WHITE), lv.PART.MAIN
        # )
        # self.index_label.set_text("" if index is None else str(index + 1))

        self.word_label = lv.label(self)
        self.word_label.add_style(Style().text_font(font.small), lv.PART.MAIN)
        self.word_label.set_text(word or "")

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, value):
        self._word = value
        self.word_label.set_text(value)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        self.index_label.set_text("" if value is None else str(value+1))

    @property
    def clickable(self):
        return self.has_flag(lv.obj.FLAG.CLICKABLE)

    @clickable.setter
    def clickable(self, value):
        if value:
            self.add_flag(lv.obj.FLAG.CLICKABLE)
            self.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        else:
            self.clear_flag(lv.obj.FLAG.CLICKABLE)
            self.clear_flag(lv.obj.FLAG.EVENT_BUBBLE)

    @property
    def checked(self):
        return self.has_state(lv.STATE.CHECKED)

    @checked.setter
    def checked(self, value):
        if value:
            self.add_state(lv.STATE.CHECKED)
        else:
            self.clear_state(lv.STATE.CHECKED)

    @property
    def inputting(self):
        return self.has_state(lv.STATE.USER_1)

    @inputting.setter
    def inputting(self, value):
        if value:
            self.add_state(lv.STATE.USER_1)
        else:
            self.clear_state(lv.STATE.USER_1)

    def toggle(self):
        self.checked = not self.checked

class Input(lv.obj):
    def on_click_blank(self, e: lv.event_t):
        if e.get_target() != self:
            return

        lv.event_send(self, lv.EVENT.CANCEL, None)

    def __init__(self, parent, index):
        super().__init__(parent)
        self.add_flag(lv.obj.FLAG.EVENT_BUBBLE)

        self.add_style(
            Style()
            .pad_left(0)
            .pad_right(0)
            .pad_bottom(0)
            .bg_color(colors.DS.GRAY)
            .bg_opa(lv.OPA._20)
            .border_width(0)
            .width(lv.pct(100))
            .height(lv.pct(100)),
            0
        )
        self.set_pos(0, 0)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(self.on_click_blank, lv.EVENT.CLICKED, None)
        self.set_style_text_color(colors.DS.BLACK, 0)

        self.content = HStack(self)
        self.content.add_style(
            Style()
            .pad_left(0)
            .pad_right(0)
            .pad_bottom(0)
            .pad_top(0)
            .width(lv.pct(100))
            .height(lv.SIZE.CONTENT)
            .text_color(colors.DS.BLACK)  # 设置文本颜色为黑色
            .bg_color(colors.DS.WHITE)
            .bg_opa(),
            lv.PART.MAIN
        )
        self.content.items_center()
        self.content.align(lv.ALIGN.BOTTOM_MID, 0, 0)

        # <index> and `textarea`
        container = VStack(self.content)
        container.add_style(
            Style()
            .width(lv.pct(100))
            .height(80)
            .pad_left(16)
            .pad_right(16)
            .text_color(colors.DS.BLACK)
            .pad_column(16),

            lv.PART.MAIN
        )
        container.set_style_flex_cross_place(lv.FLEX_ALIGN.END, lv.PART.MAIN)

        # a label for index
        self.index = lv.label(container)
        self.index.add_style(Styles.title_text, lv.PART.MAIN)
        self.index.set_text(f"#{index + 1}")
        self.index.set_style_text_color(colors.DS.BLACK, 0)
        
        self.ta = lv.textarea(container)
        self.ta.set_one_line(True)
        self.ta.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        # self.ta.set_style_text_color(colors.DS.BLACK , lv.PART.MAIN)
        self.ta.add_style(
            Style()
            .bg_opa(lv.OPA.TRANSP)
            
            .width(lv.pct(100))  # 使用百分比宽度
            .height(lv.SIZE.CONTENT)  # 高度自适应内容
            .text_font(font.Bold.SCS38)
            .border_width(0)
            .text_align_center(),
            # .border_width(3)
            # .border_color(colors.DS.BLACK)
            # .border_side(lv.BORDER_SIDE.BOTTOM)
            lv.PART.MAIN,
        )
        self.ta.set_flex_grow(1)
        self.kbd = MnemonicKeyboard(self.content)
        self.kbd.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.kbd.set_width(lv.pct(100))  # 设置键盘宽度为父容器的 100%
        self.kbd.set_height(300)  # 设置键盘高度为 300 像素
        self.kbd.add_style(
            Style()
            .text_font(font.Bold.SCS38)  # 增大键盘字体
            .text_color(colors.DS.BLACK)  # 设置字体颜色为黑色
            .pad_row(11),  # 增大键盘字母的行间距（16像素，可根据需要调整）
            lv.PART.MAIN,
        )
        # self.kbd.set_style_text_color(colors.DS.BLACK , lv.PART.MAIN)
        self.kbd.textarea = self.ta
        

    def reset(self):
        self.ta.set_text("")
        self.kbd.default_state()

    def set_index(self, index):
        self.index.set_text(f"#{index + 1}")
