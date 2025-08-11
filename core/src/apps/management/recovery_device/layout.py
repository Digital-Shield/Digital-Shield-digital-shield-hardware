from typing import TYPE_CHECKING
import lvgl as lv
import storage.recovery
from trezor import wire
from trezor.ui import i18n
from trezor.ui.layouts import (
    show_success,
    show_warning,
    show_notmatch_warning,
    show_mnemonics_warning
)

from trezor.ui.layouts.common import button_request
# from trezor.ui.layouts.lvgl.lite import backup_with_lite
# from trezor.ui.layouts.lvgl.recovery import (  # noqa: F401
#     continue_recovery,
#     request_word,
#     request_word_count,
#     show_group_share_success,
#     show_remaining_shares,
# )

# from .. import backup_types
# from . import word_validity
# from .recover import RecoveryAborted

if TYPE_CHECKING:
    from trezor.enums import BackupType
    pass


async def request_mnemonic(
    ctx: wire.GenericContext, word_count: int, backup_type: BackupType | None
):
    from trezor.ui.layouts import request_mnemonic
    return await request_mnemonic(ctx, word_count)

async def show_dry_run_result(
    ctx: wire.GenericContext, result: bool
) -> None:
    if result:
        # titles = "助记词正确",
        msg = i18n.Text.correct_words
        icon = "A:/res/wallet_ready.png"
        await show_success(
            ctx,
            msg,#i18n.Text.backup_verified,
            i18n.Title.correct_words,
        )
        
    else:
        text = i18n.Text.check_recovery_not_match
        titles = i18n.Title.mnemonic_not_match
        txt = i18n.Text.mnemonic_not_match
        await show_notmatch_warning(
            ctx,
            txt,
            button=i18n.Button.continue_,
            title=titles,
        )


async def show_dry_run_different_type(ctx: wire.GenericContext) -> None:
    await show_warning(
        ctx,
        title="Dry run failure",
        msg="Seed in the device was\ncreated using another\nbackup mechanism.",
    )


async def show_invalid_mnemonic(ctx: wire.GenericContext,words: str) -> None:
    title = i18n.Title.invalid_mnemonic
    text = i18n.Text.invalid_recovery_mnemonic
    await show_warning(
        ctx,
        text,
        title= title,
        button=i18n.Button.try_again
    )
    
    # from trezor.ui import NavigationBack
    # r = await interact(ctx, screen, ButtonRequestType.MnemonicInput)
    # if isinstance(r, NavigationBack):
    #     await screen.wait_unloaded()
    #     return r
    # print("调用了---")
    # screen.show()

from trezor.ui.component import Title, Button, HStack, VStack
from trezor import workflow
from trezor.ui.screen.initialize.mnemonic import MnemonicInput
class MyObject:
    def __init__(self, data):
        self.data = data
from trezor.ui.screen.message import Message
class SomeClass(Message):
    def __init__(self, title, words):
        super().__init__(title, words, "")
        self.count = len(words.split())
        """显示无效助记词界面（改为顶层容器）"""
        # 安全删除已存在的无效界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            self.invalid_screen.delete()
        print("接收到words", words)
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
        for i, word in enumerate(words):
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
        # 获取点击的按钮
        btn = e.get_target()
        # 获取用户数据
        obj = btn.data
        if not obj:
            return
        #清除ee.get_target()
        # index = obj.data
        self.current_index = obj
        print("on_edit_index", obj)
        
        # 安全删除无效助记词界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            # for child in self.invalid_screen.get_children():
            print("删除无效助记词界面")
            self.invalid_screen.delete()
            self.invalid_screen = None
        workflow.spawn(MnemonicInput(self.count).show())

    def on_restart(self, e):
        """重新开始输入"""
        # 安全删除无效助记词界面
        if hasattr(self, 'invalid_screen') and self.invalid_screen:
            # for child in self.invalid_screen.get_children():
            #     child.remove_event_cb_all()
            self.invalid_screen.delete()
            self.invalid_screen = None
        
            # self.invalid_screen.delete()
        workflow.spawn(MnemonicInput(self.count).show())


async def show_share_already_added(ctx: wire.GenericContext) -> None:
    await show_warning(
        ctx,
        "Share already entered,\nplease enter\na different share.",
    )


async def show_identifier_mismatch(ctx: wire.GenericContext) -> None:
    await show_warning(
        ctx,
        "You have entered\na share from another\nShamir Backup.",
    )


async def show_group_threshold_reached(ctx: wire.GenericContext) -> None:
    await show_warning(
        ctx,
        "Threshold of this\ngroup has been reached.\nInput share from\ndifferent group.",
    )
