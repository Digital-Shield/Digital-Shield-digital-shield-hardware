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
from trezor.ui.screen.confirm import SimpleConfirm, WordCheckConfirm
from trezor import workflow

from trezor.crypto import random

from trezor.ui.types import *

class MnemonicDisplay(Modal):

    def __init__(self):
        super().__init__()
        # self.set_title(i18n.Title.backup_mnemonic, "A:/res/app_security.png")
        # self.set_title(i18n.Title.backup_mnemonic)
        self.btn_right.set_text(i18n.Button.continue_)
        self.btn_right.set_style_width(440, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
        self.btn_left.set_text(i18n.Button.redo)
        self.btn_left.delete()

        self.create_content(HStack)
        self.content: HStack
        self.content.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        # self.content.set_style_pad_left(12, lv.PART.MAIN)
        self.content.set_style_pad_row(16, lv.PART.MAIN)
        self.content.add_style(
            Style()
            .pad_top(15),
            0
        )

        self.btn_next = self.btn_right

        # self.btn_redo.add_event_cb(
        #     lambda e: self.channel.publish(Redo()), lv.EVENT.CLICKED, None
        # )
        self.btn_next.add_event_cb(
            lambda e: self.channel.publish(Done()), lv.EVENT.CLICKED, None
        )

        self.items: List[Item] = []

    def update_mnemonics(self, mnemonics: Sequence[str]):
        log.debug(__name__, f"mnemonics: {mnemonics}")

        # mnemonics = list(enumerate(mnemonics))

        # 创建新的顶层容器
        self.invalid_screen = lv.obj(self.content)
        self.invalid_screen.set_size(lv.pct(100), 650)
        self.invalid_screen.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self.invalid_screen.set_style_border_width(0, lv.PART.MAIN)
        self.invalid_screen.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
         # 设置为可滚动容器（关键修改点）
        self.invalid_screen.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)  # 隐藏滚动条
        # self.invalid_screen.set_scroll_dir(lv.DIR.VER)  # 垂直滚动
        self.invalid_screen.set_style_max_height(lv.pct(100), lv.PART.MAIN)
        # #设置边框宽1
        # self.invalid_screen.set_style_border_width(2, lv.PART.MAIN)
        # self.invalid_screen.set_style_border_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        

        # 标题
        title = lv.label(self.invalid_screen)
        title.set_text(i18n.Title.mnemonic_word)
        title.set_size(400, 66)
        title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        title.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        title.align(lv.ALIGN.TOP_LEFT, 40, 6)
        
        # 描述
        desc = lv.label(self.invalid_screen)
        desc.set_text(i18n.Text.mnemonic_word_tips.format(len(mnemonics)))
        # desc.set_width(lv.pct(80))
        desc.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        desc.set_style_text_font(font.Bold.SCS26, lv.PART.MAIN)
        desc.set_size(400, 90)
        #设置行间距10
        desc.set_style_pad_row(10, lv.PART.MAIN)  # 行与行之间的间距
        desc.set_style_text_line_space(10, lv.PART.MAIN)
        desc.set_long_mode(lv.label.LONG.WRAP)
        desc.align(lv.ALIGN.TOP_LEFT, 40, 70)
        # desc.align_to(title, lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
        
        # 单词列表
        word_list = VStack(self)
        #VStack上滑动的时候禁止会弹

        word_list.set_size(440, lv.SIZE.CONTENT)
        #设置行间距10
        word_list.set_style_pad_row(16, lv.PART.MAIN)  # 行与行之间的间距
        #设置边框宽1
        word_list.set_style_border_width(2, lv.PART.MAIN)
        word_list.set_style_border_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        word_list.set_style_border_opa(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT)  # 边框透明
        word_list.align_to(desc, lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
        word_list.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        #设置可下拉显示
        word_list.set_style_max_height(lv.pct(55), lv.PART.MAIN)
        word_list.set_style_pad_bottom(0, lv.PART.MAIN)
        # 添加单词按钮
        for i, word in enumerate(mnemonics):
            btn = word_list.add(lv.btn)
            #设置圆角16
            btn.set_style_radius(16, lv.PART.MAIN)
            btn.set_size(200, 59)
            # #设置btn上下间距16
            # btn.set_style_pad_top(16, lv.PART.MAIN)
            btn.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
            btn.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
            #设置btn不可点击
            btn.add_state(lv.STATE.DISABLED)
            #不可点击状态背景色
            btn.set_style_bg_color(lv.color_hex(0x0D0E17), lv.STATE.DISABLED)

            label = lv.label(btn)
            label.set_text("{:02d}.{}".format(i + 1, word))
            # 设置标签在按钮内左侧居中对齐
            label.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN)
            label.align_to(btn, lv.ALIGN.LEFT_MID, 10, 0)
            label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
            # label.set_long_mode(lv.label.LONG.WRAP)
            # label.center()

    # def on_nav_back(self, event):
    #     from trezor.ui import NavigationBack

    #     # should notify caller
    #     self.channel.publish(NavigationBack())

from trezor import io
import ujson as json

WORDLIST: list[str] = []
with io.fatfs.open("0:/res/english.json", "rb") as f:
    description = bytearray(30000)
    n = f.read(description)  # 读取整个文件内容
    try:
        WORDLIST = json.loads(
            (description[:n]).decode("utf-8")
        )
        # print("metadata_load: ", WORDLIST)
        print("length", len(WORDLIST))
    except BaseException as e:
        if __debug__:
            print(f"Invalid json {e}")
# 加载词库
from trezor.ui.screen.navaigate import Navigate
class MnemonicCheck(Navigate):
    def __init__(self,rnd_words=[]):
        super().__init__()
         #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        # self.set_title(i18n.Title.check_mnemonic)
        
        # 状态管理
        self.current_index = 0  # 当前验证序号
        self.mnemonics =  rnd_words # 待验证的助记词列表
        print("收到mnemonics",self.mnemonics)
        self.wordlist = WORDLIST  # 完整词库
        self.correct_count = 0  # 正确计数
        
       # UI组件初始化
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_all(20, lv.PART.MAIN)
        self.content.set_style_pad_top(60, lv.PART.MAIN)
        self.content.set_size(440, 500)
        #行间距0
        self.content.set_style_pad_row(0, lv.PART.MAIN)  # 行与行之间的间距
        # self.content.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        #新建容器1
        self.a_container = lv.obj(self.content)
        self.a_container.set_size(470, 150)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        #设置背景色
        # self.a_container.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.a_container.set_style_pad_left(20, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 20)

        # 序号显示
        self.index_label = lv.label(self.a_container)
        self.index_label.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        self.index_label.set_style_text_color(colors.DS.WHITE, lv.PART.MAIN)
        self.index_label.align(lv.ALIGN.TOP_LEFT, 20, 20)

        # 提示文字
        self.hint_label = lv.label(self.a_container)
        self.hint_label.set_style_text_font(font.Bold.SCS26, lv.PART.MAIN)
        self.hint_label.set_style_text_color(colors.DS.WHITE, lv.PART.MAIN)
        self.hint_label.set_text(i18n.Text.select_words)
        #自动换行
        self.hint_label.set_long_mode(lv.label.LONG.WRAP)
        #自动换行
        self.hint_label.set_long_mode(lv.label.LONG.WRAP)
        self.hint_label.align_to(self.index_label, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 20)
        
        #选项容器
        self.a_container2 = lv.obj(self.content)
        self.a_container2.set_size(430, 300)
        self.a_container2.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        #设置背景色
        self.a_container2.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.a_container2.set_style_pad_left(30, lv.PART.MAIN)
        #圆角16
        self.a_container2.set_style_radius(16, lv.PART.MAIN)
        self.a_container2.set_style_border_width(0, lv.PART.MAIN)
        self.a_container2.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container2.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container2.align(lv.ALIGN.TOP_LEFT, 20, 0)

        # 选项
        self.options_container = HStack(self.a_container2)
        self.options_container.set_size(440, 300)
        self.options_container.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        # self.options_container.set_style_pad_row(5, lv.PART.MAIN)
        self.options_container.set_width(lv.pct(80))
        self.options_container.align(lv.ALIGN.TOP_LEFT, 20, 0)
        self.options_container.set_style_border_width(0, lv.PART.MAIN)
        #设置左上角显示
        self.options_container.set_style_pad_left(20, lv.PART.MAIN)
        # self.options_container.align_to(self.hint_label, lv.ALIGN.OUT_BOTTOM_MID, 50, 30)

        self.result_area = VStack(self.a_container2)
        self.result_area.set_size(160, 40)
        self.result_area.align(lv.ALIGN.TOP_LEFT, 50,230)
        # # Create a horizontal stack container for alignment
        # # Add the icon
        self.result_icon = lv.img(self.result_area)
        self.result_icon.set_size(32, 32)
        #默认隐藏
        self.result_icon.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        # Add the label
        self.result_label = lv.label(self.result_area)
        self.result_label.set_text("")
        self.result_label.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        self.result_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.result_label.set_style_pad_all(0, lv.PART.MAIN)

        

        # 初始化选项按钮
        self.option_buttons = []
        for _ in range(3):
            btn = lv.btn(self.options_container)
            btn.set_width(lv.pct(100))
            btn.set_height(60)
            btn.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.INDICATOR)
            btn.set_style_radius(2, lv.PART.MAIN)
            btn.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
            btn.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
            #全透明
            btn.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
            #边宽为0
            btn.set_style_border_width(0, lv.PART.MAIN)
            # 添加底边灰色边框
            btn.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
            btn.set_style_border_width(2, lv.PART.MAIN)
            btn.set_style_border_color(lv.color_hex(0x333344), lv.PART.MAIN)
            btn.set_style_border_opa(lv.OPA.COVER, lv.PART.MAIN)

            btn.set_style_text_color(colors.DS.WHITE, lv.PART.MAIN)
            btn.add_event_cb(self.on_option_click, lv.EVENT.CLICKED, None)
            
            label = lv.label(btn)
            label.set_style_text_font(font.Medium.SCS28, lv.PART.MAIN)
            #靠左对齐
            label.align(lv.ALIGN.LEFT_MID, 0, 0)
            # label.center()
            
            self.option_buttons.append((btn, label))
        #默认第一页数据显示
        self.update_screen()

    def on_option_click(self, event):
        
        """处理选项点击事件"""
        btn = event.get_target()
        click_word = btn.data
        is_correct = 1 if self.mnemonics[self.current_index] == click_word else 0
        print("is_correct",is_correct)
        # 显示结果
        if is_correct:
            # 正确：显示对勾图标 + 绿色文字
            self.result_icon.set_src("A:/res/ok_icon.png")  # 替换实际正确图标路径
            self.result_icon.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)
            self.result_label.set_text(i18n.Title.right_word)
            self.correct_count += 1
            # 延迟进入下一个
            lv.timer_create(self.next_word, 1000, None)
        else:
            # 错误：显示叉号图标 + 红色文字
            self.result_icon.set_src("A:/res/error_icon.png")  # 替换实际错误图标路径
            self.result_icon.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)
            self.result_label.set_text(i18n.Title.wrong_word)
            # 显示错误页面
            lv.timer_create(self.show_error, 1000, None)

    def next_word(self, timer):
        """进入下一个单词验证"""
        timer._del()
        self.current_index += 1
        self.update_screen()

    # def set_mnemonics(self, mnemonics: list[str]):
    #     """设置待验证的助记词列表"""
    #     self.mnemonics = mnemonics
    #     self.reset()

    def reset(self):
        """重置验证状态"""
        self.current_index = 0
        self.correct_count = 0
        self.update_screen()

    def update_screen(self):
        #暂时完成
        self.channel.publish(self.mnemonics)#验证完成
        """更新当前序号的验证界面"""
        if self.current_index >= len(self.mnemonics):
            self.channel.publish(self.mnemonics)#验证完成
            return
            
        # 更新序号显示
        word_desc = i18n.Title.words_num.format(self.current_index + 1)
        self.index_label.set_text(word_desc)

        # 生成选项
        correct_word = self.mnemonics[self.current_index]
        options = self.generate_options(correct_word)
        print("selecte_option",options)
        # 更新选项按钮
        for i, (btn, label) in enumerate(self.option_buttons):
            label.set_text(options[i])
            # 创建一个对象
            obj = MyObject(options[i])
            # 将对象设置为用户数据
            btn.set_user_data(obj)
            # btn.set_user_data(correct_word)  # 存储是否正确
            btn.clear_state(lv.STATE.CHECKED)
            btn.set_style_bg_color(colors.DS.GRAY, lv.PART.MAIN)
        
        # 清空结果提示（图标 + 文字）
        self.result_icon.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.result_label.set_text("")

    def generate_options(self, correct_word: str) -> list[str]:
        """生成包含一个正确选项的三个随机选项"""
        # 过滤词库
        filtered = [w for w in self.wordlist if w != correct_word]
        # 使用自定义函数选择两个错误选项
        wrong_options = self.select_random_elements(filtered, 2)
        print("wrong_options",wrong_options)
        # 组合并打乱顺序
        options = [correct_word] + wrong_options
        random.shuffle(options)
        return options
    #随意抽取两个选项
    def select_random_elements(self, lst, num):
        if num > len(lst):
            raise ValueError("Sample larger than population or is negative")
        selected = []
        while len(selected) < num:
            index = random.uniform(len(lst))
            # print("index----",index)
            element = lst[index]
            if element not in selected:
                selected.append(element)        
        return selected

    def show_error(self, timer):
        """显示错误页面"""
        timer._del()
        # self.channel.publish(Redo())
        workflow.spawn(self.show_error_screen())

    async def show_error_screen(self):
        from trezor.ui.screen.alerts import Alerts
        screen = Alerts(i18n.Title.error_mnemonic_word, i18n.Text.error_mnemonic_word, "A:/res/word_error.png")
        await screen.show()
        screen.btn_right.set_text(i18n.Button.try_again)
        screen.btn_right.add_event_cb(self.on_confirm, lv.EVENT.CLICKED, None)
    def on_confirm(self, event):
            from trezor.ui import NavigationBack
            print("on_confirm")
            self.channel.publish(NavigationBack())
            # self.channel.publish(Redo())    
    # def show_success(self):
    #     """显示成功页面"""
    #     screen = SimpleConfirm("已验证\n您已完成助记词验证。")
    #     screen.btn_confirm.delete()
    #     screen.btn_cancel.set_text("完成")
    #     workflow.spawn(screen.show())
    #     screen.add_event_cb(lambda e, x, y, z: self.channel.publish(True), lv.EVENT.CANCEL)
    # def on_nav_back(self, event):
    #     from trezor.ui import NavigationBack

    #     # should notify caller
    #     self.channel.publish(NavigationBack())
    def on_unloaded(self):
        from trezor.ui.screen import manager
        manager.mark_dismissing(self)

class MnemonicInput(Navigate):
    def __init__(self, count):
        super().__init__()
        self.count = count
        self.current_index = 0
        self.come_source = "mnemonic_input"
        self.mnemonics: list[str] = [""] * count
        
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

        # self.mnemonics = ['report', 'deposit', 'grape', 'priority', 'network', 'palm', 'sponsor', 'vivid', 'involve', 'attract', 'source', 'embraces']
        # self.show_invalid_mnemonic()

    def create_word_input(self):
        """创建单词输入区域"""
        # 容器
        self.word_container = lv.obj(self.content)
        self.word_container.set_size(470, 400)
        self.word_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.word_container.set_style_bg_color(lv.color_hex(0x00010B), lv.PART.MAIN)
        self.word_container.set_style_border_width(0, lv.PART.MAIN)
        
        # 单词序号
        self.index_label = lv.label(self.word_container)
        word_desc = i18n.Title.words_num.format(self.current_index + 1)
        self.index_label.set_text(word_desc)
        self.index_label.align(lv.ALIGN.TOP_LEFT, 0, 7)
        self.index_label.set_style_text_font(font.Medium.SCS28, lv.PART.MAIN)
        self.index_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        
        # 输入框（白色边框）
        self.word_input = lv.textarea(self.word_container)
        # self.word_input.align(lv.ALIGN.TOP_MID, 0, 20)
        self.word_input.set_size(440,102)
        # self.word_input.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.word_input.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.word_input.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.word_input.set_style_pad_left(20, lv.PART.MAIN)
        self.word_input.align_to(self.index_label, lv.ALIGN.OUT_BOTTOM_LEFT,-20, 20)
        # self.word_input.set_placeholder_text("输入单词...")
        # 设置圆角30
        self.word_input.set_style_radius(16, lv.PART.MAIN)
        # self.word_input.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT)  # 主部件完全透明[7,8](@ref)
        self.word_input.set_style_border_opa(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT)  # 边框透明
        self.word_input.set_style_border_opa(lv.OPA.TRANSP, lv.PART.CURSOR)  # 禁用光标闪烁
        #设置输入框的颜色为0x0D0E17
        self.word_input.set_style_bg_color(lv.color_hex(0x202129), lv.PART.MAIN | lv.STATE.DEFAULT)  # 主部件背景色 lv.color_hex(0x0D0E17)
        self.word_input.set_style_text_font(font.Medium.SCS40, lv.PART.MAIN)
        self.word_input.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self.word_input.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)  # 禁用滚动条
        
        self.item = Item_input(self.word_input, index=0)
        self.item.add_style(
            Style()
            .pad_top(0)
            .pad_bottom(20),
            lv.PART.MAIN,
        )
        self.item.clickable = True
        self.word_input.add_event_cb(self.on_click_item, lv.EVENT.CLICKED, None)
        self.input = None
        self._updating = False
        self.success_sign = 0
        #默认弹出键盘
        lv.event_send(self.word_input, lv.EVENT.CLICKED, None)
        # 导航箭头
        self.prev_btn = lv.btn(self.word_container)
        # self.prev_btn.set_size(35, 35)
        # self.prev_btn.align(lv.ALIGN.RIGHT_MID, -50, -160)
        self.prev_btn.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.prev_btn.set_style_shadow_width(0, lv.PART.MAIN)
        self.prev_btn.align(lv.ALIGN.TOP_RIGHT, -90, -10)
        self.prev_img = lv.img(self.prev_btn)
        self.prev_img.set_src("A:/res/prev_grey.png")
        self.prev_img.set_size(44, 44)
        self.prev_img.align(lv.ALIGN.CENTER, 0, 0)
        self.prev_btn.add_event_cb(self.on_prev_clicked, lv.EVENT.CLICKED, None)
        
        self.next_btn = lv.btn(self.word_container)
        # self.next_btn.set_size(35, 35)
        self.next_btn.align(lv.ALIGN.TOP_RIGHT, -50, -10)
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
        self.input.add_event_cb(self.on_input_show, lv.EVENT.CLICKED, None)
    #即时的输入显示到输入框
    def on_input_show(self, event):
        log.debug(__name__, "input ready")
        
        word = self.input.kbd.textarea.get_text()
        print("input show word:", word)
        item = self.item
        assert item is not None
        item.word = word

    
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

        # lv.event_send(item, lv.EVENT.CLICKED, None)

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
        self.submit_area = VStack(self.word_container)
        self.submit_area.set_size(160, 40)
        self.submit_area.align(lv.ALIGN.TOP_LEFT, 10,180)
        # Create a horizontal stack container for alignment
        # Add the icon
        self.sun_icon = lv.img(self.submit_area)
        self.sun_icon.set_src("A:/res/has_sub.png")  # 替换为实际太阳图标路径
        self.sun_icon.set_size(32, 32)
        self.sun_icon.set_style_pad_bottom(2, lv.PART.MAIN)

        # Add the label
        submit_label = lv.label(self.submit_area)
        submit_label.set_text(i18n.Title.has_sub)
        submit_label.set_style_text_font(font.Regular.SCS24, lv.PART.MAIN)
        submit_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        submit_label.set_style_pad_all(0, lv.PART.MAIN)
        # submit_label.set_style_pad_left(4, lv.PART.MAIN)
        submit_label.center()
        self.submit_area.add_flag(lv.obj.FLAG.HIDDEN)  # 初始隐藏

    def update_next_status(self, current_index: int):
        #隐藏导航Navigation
        # self.obj.clear_flag(lv.obj.FLAG.HIDDEN)
        """更新导航按钮状态"""
        self.item.word = self.mnemonics[self.current_index] if self.mnemonics[self.current_index] else ""
        word_desc = i18n.Title.words_num.format(self.current_index + 1)
        self.index_label.set_text(word_desc)
        # self.word_input.set_text(self.item.word)  # 确保输入框显示正确内容
        
        non_empty_count = sum(1 for item in self.mnemonics if item)
        self.prev_img.set_src("A:/res/prev_white.png") if current_index > 0 else self.prev_img.set_src("A:/res/prev_grey.png")
        self.next_img.set_src("A:/res/next_white.png") if current_index < non_empty_count else self.next_img.set_src("A:/res/next_grey.png")
        self.submit_area.add_flag(lv.obj.FLAG.HIDDEN)

    def on_prev_clicked(self, e):
        self.close_input()
        """上一个单词"""
        if self.current_index > 0:
            self.current_index -= 1
            self.item.word = self.mnemonics[self.current_index]
            self.update_next_status(self.current_index)

    def on_next_clicked(self, e):
        self.close_input()
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

    def on_nav_back(self, event):
        """返回确认"""
        async def show_confirm():
            screen = WordCheckConfirm(i18n.Title.stop_checking,i18n.Text.stop_checking,"A:/res/stop_check.png",False,i18n.Button.confirm)
            # screen = SimpleConfirm("确定要终止核对吗？")
            await screen.show()
            r = await screen
            if isinstance(r, Confirm):
                # print("终止核对")
                from trezor.ui import NavigationBack
                self.channel.publish(NavigationBack())
                # from trezor.ui.screen import manager
                # manager.mark_dismissing(self)
        
        workflow.spawn(show_confirm())

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
                    if self.remaining_time > 0:
                        self.submit_area.clear_flag(lv.obj.FLAG.HIDDEN)
                    else:
                        timer._del()
                        if self.current_index < len(self.mnemonics)-1 and self.come_source == "mnemonic_input":
                            self.current_index = self.current_index + 1
                            self.item.word = self.mnemonics[self.current_index] if self.mnemonics[self.current_index] else ""
                            print("self.current_index_id:",self.current_index)
                            self.update_next_status(self.current_index)
                            lv.event_send(self.word_input, lv.EVENT.CLICKED, None)
                            self.mnemonics = ['report', 'deposit', 'grape', 'priority', 'network', 'palm', 'sponsor', 'vivid', 'involve', 'attract', 'source', 'embrace']
                            # self.mnemonics = ['display','street','pole','friend','dilemma','lock','tomorrow','online','occur','way','valve','edge']
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
                                print("mnemonic_str:", mnemonic_str)
                                secret: bytes | None = recover.process_bip39(mnemonic_str)
                                print("secret:", secret)
                                print("self.come_source", self.come_source)
                                # self.channel.publish(self.mnemonics)
                                # workflow.spawn(self.show_success_screen())
                                self.success_sign = 1
                            except MnemonicError:
                                print("MnemonicError")
                                self.show_invalid_mnemonic()
                                
                            print("success_sign",self.success_sign)
                            if self.success_sign:
                                # from trezor import workflow
                                # workflow.spawn(manager.pop(self))
                                # from trezor.ui.screen import manager
                                # manager.mark_dismissing(self)
                                self.channel.publish(self.mnemonics)
                                
                
                self._timer = lv.timer_create(update_countdown, 500, None)
                
        finally:
            self._updating = False
    # async def show_success_screen(self):
    #     """错误提示页面"""
    #     screen = SimpleConfirm("单词正确。")
    #     screen.btn_confirm.set_text("确认")
    #     # screen.btn_cancel.delete()
    #     try:
    #         await screen.show()
    #     except Exception as e:
    #         print("Exception:", e)
    #     screen.btn_confirm.add_event_cb(self.on_confirm, lv.EVENT.CLICKED, None)
    # def on_confirm(self, event):
    #         from trezor.ui import NavigationBack
    #         print("on_confirm")
    #         self.channel.publish(NavigationBack()) 
    
    # def on_unloaded(self):
    #     from trezor.ui.screen import manager
    #     manager.mark_dismissing(self)

    def show_invalid_mnemonic(self):
        """显示无效助记词界面（改为顶层容器）"""
        # 安全删除已存在的无效界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            self.invalid_screen.delete()
        #隐藏导航Navigation
        # self.obj.add_flag(lv.obj.FLAG.HIDDEN)
        # content
        # self.create_content(HStack)
        # self.content: HStack
        # self.content.add_style(
        #     Style()
        #     .pad_top(5)
        #     .pad_left(6)
        #     .pad_right(16),
        #     0
        # )
        # 创建新的顶层容器
        self.invalid_screen = lv.obj(self)
        self.invalid_screen.set_size(lv.pct(100), lv.pct(100))
        self.invalid_screen.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self.invalid_screen.set_style_border_width(0, lv.PART.MAIN)
        self.invalid_screen.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
         # 设置为可滚动容器（关键修改点）
        self.invalid_screen.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)  # 隐藏滚动条
        self.invalid_screen.set_scroll_dir(lv.DIR.VER)  # 垂直滚动
        self.invalid_screen.set_style_max_height(lv.pct(100), lv.PART.MAIN)
        #左上角图标
        self.icon = lv.img(self.invalid_screen)
        self.icon.set_src("A:/res/word_error.png")
        self.icon.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
        # 使用绝对定位到左上角
        #设置水平右移20
        # self.icon.align(lv.ALIGN.TOP_LEFT, 20, 0)
        self.icon.set_style_pad_left(20, lv.PART.MAIN)
        self.icon.set_style_img_recolor_opa(0, lv.PART.MAIN)
        self.icon.set_zoom(256)  # 1.0x zoom, ensures full image is shown
        self.icon.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.icon.set_style_clip_corner(False, lv.PART.MAIN)
        
        # 标题
        title = lv.label(self.invalid_screen)
        title.set_text(i18n.Title.invalid_words)
        title.set_size(400, 66)
        title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        title.align(lv.ALIGN.TOP_LEFT, 40, 116)
        
        # 描述
        desc = lv.label(self.invalid_screen)
        desc.set_text(i18n.Text.invalid_words)
        # desc.set_width(lv.pct(80))
        desc.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        desc.set_size(400, lv.SIZE.CONTENT)
        #设置行间距10
        desc.set_style_pad_row(10, lv.PART.MAIN)  # 行与行之间的间距
        desc.set_style_text_line_space(10, lv.PART.MAIN)
        desc.set_long_mode(lv.label.LONG.WRAP)
        desc.align(lv.ALIGN.TOP_LEFT, 40, 170)
        # desc.set_style_pad_bottom(30, lv.PART.MAIN)
        # desc.align_to(title, lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
        
        # 单词列表
        word_list = VStack(self.invalid_screen)
        #VStack上滑动的时候禁止会弹

        word_list.set_size(450, 800)
        #设置行间距10
        word_list.set_style_pad_row(16, lv.PART.MAIN)  # 行与行之间的间距
        #设置边框宽1
        word_list.set_style_border_width(0, lv.PART.MAIN)
        word_list.set_style_border_opa(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT)  # 边框透明
        word_list.align_to(desc, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
        word_list.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        #设置可下拉显示
        word_list.set_style_max_height(lv.pct(55), lv.PART.MAIN)
        word_list.set_style_pad_bottom(180, lv.PART.MAIN)
        #列间距为5
        word_list.set_style_pad_column(5, lv.PART.MAIN)
        word_list.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN)
        # 添加单词按钮
        for i, word in enumerate(self.mnemonics):
            btn = word_list.add(lv.btn)
            #设置圆角16
            btn.set_style_radius(16, lv.PART.MAIN)
            btn.set_size(200, 59)
            # #设置btn间距6
            btn.set_style_pad_left(10, lv.PART.MAIN)
            btn.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
            btn.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
            btn.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)

            label = lv.label(btn)
            label.set_text("{:02d}.{}".format(i + 1, word))
            # 设置标签在按钮内左侧居中对齐
            label.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN)
            label.align_to(btn, lv.ALIGN.LEFT_MID, 10, 0)
            # 创建一个对象
            num = i+1
            obj = MyObject(num)
            # 将对象设置为用户数据
            btn.set_user_data(obj)
            btn.add_event_cb(self.on_edit_word, lv.EVENT.CLICKED, None)
        
        # 重新开始按钮
        restart_btn = lv.btn(self.invalid_screen)
        restart_btn.set_size(440, 89)
        restart_btn.align(lv.ALIGN.BOTTOM_MID, 0, -20)
        restart_btn.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)
        restart_label = lv.label(restart_btn)
        restart_label.set_text(i18n.Title.reatart)
        restart_label.center()
        restart_btn.add_event_cb(self.on_restart, lv.EVENT.CLICKED, None)
        
        # 记录当前状态
        self.main_screen_state = {
            "current_index": self.current_index,
            "mnemonics": self.mnemonics.copy()
        }

    def on_edit_word(self, e):
        """编辑指定单词"""
        # 获取点击的按钮
        btn = e.get_target()
        # 获取用户数据
        obj = btn.data
        print("obj",obj)
        if not obj:
            return
        index = obj - 1
        self.current_index = index
        print("on_edit_index", index)
        
        # 安全删除无效助记词界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            print("删除无效助记词界面")
            self.invalid_screen.delete()
            self.invalid_screen = None
        
        # 恢复主界面状态
        self.mnemonics = self.main_screen_state["mnemonics"].copy()
        self.come_source = "invalid"
        self.update_next_status(self.current_index)
        # workflow.spawn(self.show())

    def on_restart(self, e):
        """重新开始输入"""
        # 安全删除无效助记词界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            self.invalid_screen.delete()
            self.invalid_screen = None
        
        # 重置主界面状态
        self.mnemonics = [""] * self.count
        self.current_index = 0
        self.item.word = ""
        self.come_source = "mnemonic_input"
        self.update_next_status(self.current_index)
        # workflow.spawn(self.show())

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
            .bg_color(lv.color_hex(0x202129))  # 深色背景
            #完全不透明，避免影响子组件
            .bg_opa(lv.OPA.TRANSP)#COVER
            .radius(16)
            .width(lv.pct(100))
            .height(102)
            .text_color(colors.DS.WHITE)
            ,
            # .border_width(1),
            lv.PART.MAIN,
        )

        self.items_center()

        self.add_style(Styles.checked, lv.PART.MAIN | lv.STATE.CHECKED)
        # we use USER_1 to mark inputting
        # not directly use lv.STATE.FOCUSED, because it will changed when `Input` popup
        # self.add_style(Styles.focused, lv.PART.MAIN | lv.STATE.USER_1)

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

class Item(HStack):
    #    <index>
    #    <word>

    def __init__(self, parent, word: str | None = None, index: int | None = None):
        super().__init__(parent)
        self._word = word
        self._index = index
        self.add_style(
            Style()
            .bg_color(lv.color_hex(0x111126))  # 深色背景
            .bg_opa(lv.OPA._90)  # 90% 不透明，避免影响子组件
            .text_font(font.Medium.SCS40)
            .radius(16)
            .width(140)
            .height(96)
            .text_color(colors.DS.WHITE)
            .border_width(1)
            .bg_opa(lv.OPA.COVER),
            lv.PART.MAIN,
        )

        self.items_center()

        self.add_style(Styles.checked, lv.PART.MAIN | lv.STATE.CHECKED)
        # we use USER_1 to mark inputting
        # not directly use lv.STATE.FOCUSED, because it will changed when `Input` popup
        self.add_style(Styles.focused, lv.PART.MAIN | lv.STATE.USER_1)

        self.index_label = lv.label(self)
        self.index_label.add_style(
            Style().text_font(font.small).text_color(colors.DS.WHITE), lv.PART.MAIN
        )
        self.index_label.set_text("" if index is None else str(index + 1))

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
            .bg_opa(lv.OPA._0)#全透明
            .border_width(0)
            .width(lv.pct(100))
            .height(lv.pct(100)),
            0
        )
        self.set_pos(0, 0)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(self.on_click_blank, lv.EVENT.CLICKED, None)
        self.set_style_text_color(lv.color_hex(0xFFFFFF), 0)

        self.content = HStack(self)
        self.content.add_style(
            Style()
            .pad_left(0)
            .pad_right(0)
            .pad_bottom(0)
            .pad_top(10)
            .width(lv.pct(100))
            .height(lv.SIZE.CONTENT)
            .border_width(0)
            .text_color(lv.color_hex(0xFFFFFF))  # 设置文本颜色为白色
            .bg_color(lv.color_hex(0x00010B))
            .bg_opa(),
            lv.PART.MAIN
        )
        # self.content.set_style_text_color(lv.color_hex(0x#1AB72A), 0)
        self.content.items_center()
        self.content.align(lv.ALIGN.BOTTOM_MID, 0, 0)

        
        self.ta = lv.textarea(self)
        #隐藏self.ta
        self.ta.add_flag(lv.obj.FLAG.HIDDEN)
        
        self.kbd = MnemonicKeyboard(self.content)
        self.kbd.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.kbd.set_width(lv.pct(100))  # 设置键盘宽度为父容器的 100%
        self.kbd.set_height(300)  # 设置键盘高度为 300 像素
        self.kbd.add_style(
            Style()
            .text_font(font.Bold.SCS38)  # 增大键盘字体
            # .bg_color(lv.color_hex(0x7F7F7F))
            .text_color(colors.DS.WHITE)  # 设置字体颜色为白色
            .pad_row(11)
            .pad_bottom(0)
            .border_width(0),  # 增大键盘字母的行间距（16像素，可根据需要调整）
            lv.PART.MAIN,
        )
        # self.kbd.add_style(Style().bg_color(colors.DS.GRAY).radius(60), lv.PART.KNOB)
        # self.kbd.set_style_text_color(colors.DS.WHITE , 0)
        self.kbd.textarea = self.ta
        

    def reset(self):
        self.ta.set_text("")
        self.kbd.default_state()

    def set_index(self, index):
        self.index.set_text(f"#{index + 1}")
