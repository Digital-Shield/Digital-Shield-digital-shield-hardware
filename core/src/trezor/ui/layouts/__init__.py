# from trezor import utils
# import storage
# import storage.recovery
from typing import TYPE_CHECKING
import lvgl as lv
from trezor import log, wire, workflow, loop
from trezor import ui, wire
from trezor.enums import ButtonRequestType
from trezor.messages import ButtonAck, ButtonRequest
from trezor.ui import i18n, colors
from trezor.ui import NavigationBack
from .common import button_request, interact2, raise_if_cancelled

if TYPE_CHECKING:
    from typing import Any, Awaitable, TypeVar, Sequence

    T = TypeVar("T")
    LayoutType = Awaitable[Any]

from .helper import *

# import `show` function for easy use
from .bitcoin import show_xpub, show_pubkey


# messages functions
async def show_popup(
    operation: str,
    timeout_ms: int = 3000,
    icon: str | None = None,
) -> None:
    from trezor.ui.screen.popup import Popup

    screen = Popup(operation, icon)
    await screen.show()
    screen.auto_close_timeout = timeout_ms
    await screen

#蓝牙连接失败弹窗
async def show_popup_connection_failed(
    operation: str,
    timeout_ms: int = 3000,
    icon: str | None = None,
) -> None:
    from trezor.ui.screen.confirm import WordCheckConfirm
    screen = WordCheckConfirm(operation,i18n.Title.connect_again,icon,True)
    screen.btn_confirm.set_text(i18n.Button.done)
    await screen.show()
    screen.auto_close_timeout = timeout_ms
    await screen

async def show_trans_popup(
    operation: str,
    timeout_ms: int = 3000,
    icon: str | None = None,
) -> None:
    
    print("show transaction signed")
    from trezor.ui.screen.confirm import WordCheckConfirm
    screen = WordCheckConfirm(i18n.Text.transaction_signed,i18n.Text.sign_success,"A:/res/wallet_ready.png",True)
    screen.btn_confirm.set_text(i18n.Button.done)
    await screen.show()
    await screen

async def load_popup(
    operation: str,
    timeout_ms: int = 2000,
    icon: str | None = None,
) -> None:
    from trezor.ui.screen.popup import LoadingPopup

    screen = LoadingPopup(operation, icon)
    await screen.show()
    screen.auto_close_timeout = timeout_ms
    await screen
#蓝牙连接失败
async def show_pairing_error() -> None:
    await show_popup_connection_failed(
        i18n.Text.bluetooth_pair_failed,
        timeout_ms=2000,
        icon="A:/res/word_error.png",
    )


async def show_app_guide() -> None:
    # TODO: implement
    pass


async def show_airgap_signature(sig: str):
    from trezor.ui.screen.airgap import EthSignature

    screen = EthSignature(sig)
    await screen.show()
    await screen

async def show_success_create(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Success",
    button: str = i18n.Button.done,
) -> Awaitable[None]:
    from trezor.ui.screen.confirm import WordCheckConfirm
    screen = WordCheckConfirm(title, msg,"A:/res/wallet_ready.png",True,i18n.Button.done)
    screen.btn_confirm.set_text(i18n.Button.done)
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Success))

async def show_success_pin(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Success",
    button: str = i18n.Button.done,
) -> Awaitable[None]:
    from trezor.ui.screen.confirm import WordCheckConfirm
    screen = WordCheckConfirm(title, msg,"A:/res/wallet_ready.png",True,i18n.Button.done)
    screen.btn_confirm.set_text(i18n.Button.done)
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Success))

async def show_success(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Success",
    button: str = i18n.Button.done,
) -> Awaitable[None]:
    # from trezor.ui.screen.message import Success
    # screen = Success(title, msg)
    # screen.button_text(button)
    from trezor.ui.screen.confirm import WordCheckConfirm
    screen = WordCheckConfirm(title, msg,"A:/res/wallet_ready.png",True,i18n.Button.done)
    screen.btn_confirm.set_text(i18n.Button.done)
    await screen.show()
    if msg == i18n.Text.correct_words:#核对钱包成功
        # 延迟发布消息，确保界面状态稳定 await loop.sleep(200)
        return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Success))
    else:
        await interact(
            ctx,
            screen,
            ButtonRequestType.ResetDevice,
        )
        # await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Success))
        await wallet_download_tip(ctx,i18n.Title.download_digital, i18n.Text.download_digital_tips)
        await wallet_connect_tip(ctx,i18n.Title.connect_wallets, "")
async def show_warning(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Warning",
    button: str = i18n.Button.try_again,
) -> Awaitable[None]:
    from trezor.ui.screen.message import Warning

    # screen = Warning(title, msg)
    # screen.button_text(button)
    # await screen.show()
    # from trezor.ui.screen.confirm import WordCheckConfirm
    # screen = WordCheckConfirm(title,msg,"A:/res/word_error.png",False)
    # screen.btn_confirm.delete()
    # screen.btn_cancel.set_text(i18n.Button.try_again)
    # screen.btn_cancel.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
    from trezor.ui.screen.alerts import Alerts
    screen = Alerts(title, msg, "A:/res/word_error.png")
    screen.btn_right.set_text(i18n.Button.try_again)
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Warning))

async def show_notmatch_warning(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Warning",
    button: str = i18n.Button.try_again,
) -> Awaitable[None]:
    from trezor.ui.screen.message import Warning

    from trezor.ui.screen.confirm import WordCheckConfirm
    screen = WordCheckConfirm(title,msg,"A:/res/word_error.png",False)
    screen.btn_confirm.delete()
    screen.btn_cancel.set_text(i18n.Button.try_again)
    screen.btn_cancel.set_style_width(440, lv.PART.MAIN)
    screen.btn_cancel.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Warning))

async def show_mnemonics_warning(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Warning",
    button: str = i18n.Button.try_again,
    words: str = ""
) -> Awaitable[None]:
    from trezor.ui.screen.initialize.mnemonick import MnemonicInputs
    screen = MnemonicInputs(len(words.split()), words)
    await screen.show()
    print("show success - after show, screen displayed")
    from trezor.enums import ButtonRequestType
    r = await interact(ctx, screen, ButtonRequestType.Other)
    if isinstance(r, NavigationBack):
        print("back----")
        raise wire.ActionCancelled()
    log.debug(__name__, f"checked words: {r}")
    return r
    # return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Warning))
    # from trezor.ui.screen.message import Warning

    # screen = Warning(title, msg)
    # screen.button_text(button)
    # await screen.show()
    # return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Warning))


async def show_error(
    ctx: wire.GenericContext,
    msg: str,
    title: str = "Error",
    button: str = i18n.Button.try_again,
) -> Awaitable[None]:
    from trezor.ui.screen.message import Error

    screen = Error(title, msg)
    screen.button_text(button)
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Warning))


async def show_address(
    ctx: wire.GenericContext,
    address: str,
    path: str,
    network: str,
    chain_id: int | None = None,
):
    from trezor.ui.screen.template import Address
    print("show address")
    screen = Address(address, path, network, chain_id)
    await screen.show()
    return await interact(ctx, screen, ButtonRequestType.Address)


# confirm functions
async def hold_confirm_action(
    ctx: wire.GenericContext, title: str, msg: str, br_code=ButtonRequestType.Other, chain_name: str = ""
):
    from trezor.ui.screen.template import HoldConfirmAction

    screen = HoldConfirmAction(title, msg, chain_name)
    # icon = None
    # if hasattr(ctx, "icon_path"):
    #     icon = ctx,icon_path
    # screen.set_title(title, icon)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, br_code))


async def confirm_action(
    ctx: wire.GenericContext, title: str, msg: str, br_code=ButtonRequestType.Other, names: str=""
):
    from trezor.ui.screen.confirm import SimpleConfirm, UpdateCheckConfirm

    screen = UpdateCheckConfirm(title, msg, names, False)
    # screen.title.set_text(title)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, br_code))


async def confirm_final(ctx: wire.GenericContext, chain_name: str) -> None:
    # confirm
    await hold_confirm_action(
        ctx,
        i18n.Title.confirm_transaction,
        i18n.Text.do_sign_this_transaction.format(chain_name),
        ButtonRequestType.SignTx,
        chain_name
    )
    # show success
    await show_trans_popup(
        i18n.Text.transaction_signed, timeout_ms=3000, icon="A:/res/success.png"
    )


async def confirm_set_homescreen(ctx, replace: bool = False):
    msg = i18n.Text.set_as_homescreen
    if replace:
        msg = i18n.Text.replace_homescreen
    await confirm_action(
        ctx,
        i18n.Title.set_as_homescreen,
        msg,
    )

async def confirm_collect_nft(ctx, replace: bool = False):
    msg = i18n.Text.collect_nft
    if replace:
        msg = i18n.Text.replace_nft
    await confirm_action(
        ctx,
        i18n.Title.collect_nft,
        msg,
    )

async def confirm_verify_device(ctx):
    await confirm_action(ctx, i18n.Title.verify_device, i18n.Text.verify_device)

async def confirm_update_res(ctx, update_boot:bool):
    if update_boot:
        title = i18n.Title.update_bootloader
        msg = i18n.Text.update_bootloader
    else:
        title = i18n.Title.update_resource
        msg = i18n.Text.update_resource

    from trezor.ui.screen.confirm import SimpleConfirm
    screen = SimpleConfirm(msg)
    screen.title.set_text(title)
    screen.btn_right.set_text(i18n.Button.update)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen))

## wipe device
async def confirm_wipe_device(ctx: wire.GenericContext):
    # from trezor.ui.screen.confirm import SimpleConfirm

    # screen = SimpleConfirm(i18n.Text.wipe_device)
    # screen.btn_confirm.color(colors.DS.DANGER)
    # screen.btn_confirm.set_text(i18n.Button.continue_)
    # screen.text_color(colors.DS.DANGER)
    # await screen.show()
    from trezor.ui.screen.confirm import SimpleConfirm, WordCheckConfirm
    screen = WordCheckConfirm(i18n.Title.wipe_device,i18n.Text.wipe_device,"A:/res/warning_tip.png",False)
    screen.btn_confirm.set_text(i18n.Button.confirm)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.WipeDevice))


async def confirm_wipe_device_tips(ctx: wire.GenericContext):
    from trezor.ui.screen.management.wipe_device import WipeDeviceTips

    screen = WipeDeviceTips()
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.WipeDevice))


async def confirm_wipe_device_success(ctx: wire.GenericContext):
    # from trezor.ui.screen.message import Info

    # screen = Info(None, i18n.Text.wipe_device_success)
    # screen.button_text(i18n.Button.continue_)
    # await screen.show()
    from trezor.ui.screen.confirm import SimpleConfirm, WordCheckConfirm
    screen = WordCheckConfirm(i18n.Title.has_wipe,i18n.Text.has_wipe,"A:/res/warning_tip.png",True)
    screen.btn_confirm.set_text(i18n.Setting.restart_tip)
    await screen.show()
    return await interact(ctx, screen, ButtonRequestType.WipeDevice)
#钱包创建相关提示
async def wallet_colleted_tip(ctx: wire.GenericContext,title:str,msg:str,icon: str = "A:/res/success.png") -> bool:
    # from trezor.ui.screen.alerts import Alerts
    # screen = Alerts(title, msg, icon)
    # await screen.show()
    from trezor.ui.screen.confirm import WordCheckConfirm
    screen = WordCheckConfirm(title, msg,icon,True,i18n.Button.continue_)
    # screen.btn_confirm.set_text(i18n.Button.done)
    await screen.show()
    await interact(
        ctx,
        screen,
        ButtonRequestType.ResetDevice,
    )
#钱包导入相关提示
async def wallet_import_tip(ctx: wire.GenericContext,title:str,msg:str,icon: str,left_btn_hidden: bool) -> bool:
    from trezor.ui.screen.alerts import Alerts
    screen = Alerts(title, msg, icon, left_btn_hidden)
    screen.btn_left.clear_flag(lv.obj.FLAG.HIDDEN)
    await screen.show()

    return await interact(
        ctx,
        screen,
        ButtonRequestType.ResetDevice,
    )
#下载钱包提示
async def wallet_download_tip(ctx: wire.GenericContext,title:str,msg:str) -> bool:
    from trezor.ui.screen.qrcode import Qrcode
    screen = Qrcode(title, msg, True) 
    # screen.btn_left.clear_flag(lv.obj.FLAG.HIDDEN)
    await screen.show()

    return await interact(
        ctx,
        screen,
        ButtonRequestType.ResetDevice,
    )
#连接钱包提示
async def wallet_connect_tip(ctx: wire.GenericContext,title:str,msg:str) -> bool:
    from trezor.ui.screen.qrcode import Qrcode
    screen = Qrcode(title, msg, False, i18n.DownloadDigital)
    screen.btn_right.set_text(i18n.Button.done)
    # screen.btn_left.clear_flag(lv.obj.FLAG.HIDDEN)
    await screen.show()

    return await interact(
        ctx,
        screen,
        ButtonRequestType.ResetDevice,
    )
async def mnemonic_security_tip(ctx: wire.GenericContext) -> bool:
    from trezor.ui.screen.initialize.xsecurity import MnemonicSecurity

    screen = MnemonicSecurity()
    await screen.show()
    await interact(
        ctx,
        screen,
        ButtonRequestType.ResetDevice,
    )

async def request_pin_on_device(
    ctx: wire.GenericContext,
    prompt: str,
    attempts_remaining: int | None,
    allow_cancel: bool,
) -> str:
    await button_request(ctx, code=ButtonRequestType.PinEntry)
    from storage import device

    if attempts_remaining is None or attempts_remaining == device.PIN_MAX_ATTEMPTS:
        subprompt = ""
    elif attempts_remaining == 1:
        subprompt = i18n.Text.incorrect_pin_last_time
    else:
        subprompt = i18n.Text.incorrect_pin_times_left.format(attempts_remaining)
    from trezor.ui.screen.pin import InputPinScreen
    #输入pin码超了次数，进行跳转页面，含有倒计时重启
    if attempts_remaining == 0:
        from trezor.ui.screen.tips import Tips
        screen = Tips(i18n.Title.has_reset,i18n.Text.has_reset)
        await screen.show()
    else:    
        screen = InputPinScreen(prompt)
        screen.warning(subprompt)
        await screen.show()
    result = await ctx.wait(screen)
    if not result:
        if not allow_cancel:
            loop.clear()
        raise wire.PinCancelled
    #超次数重启
    if attempts_remaining == 0:
        async def restart_delay():
            from trezor import utils
            utils.reset()
        from trezor import workflow
        workflow.spawn(restart_delay())
        
    assert isinstance(result, str)
    return result

async def request_word_count(ctx: wire.GenericContext, dry_run: bool) -> int | NavigationBack:
    from trezor.ui.screen.initialize.wordcount import WordcountScreen
    from trezor.ui.screen import manager
    screen = manager.try_switch_to(WordcountScreen)
    if not screen:
        screen = WordcountScreen(dry_run)
        await screen.show()

    r = await interact(ctx, screen, ButtonRequestType.MnemonicWordCount)
    if isinstance(r, NavigationBack):
        return r
    
    return int(r)

async def request_mnemonic(ctx, word_count: int) -> str | NavigationBack:
    
    from trezor.ui.screen.initialize.mnemonic import MnemonicInput
    screen = MnemonicInput(word_count)
    await screen.show()
    r = await interact(ctx, screen, ButtonRequestType.MnemonicInput)
    if isinstance(r, NavigationBack):
        await screen.wait_unloaded()
        return r
    # words = screen.mnemonics
    words = [str(w) if w is not None else "" for w in screen.mnemonics]
    print(f"response_mnemonic: {words}")
    return ' '.join(words)

async def request_strength(ctx,label: str) -> int:
    word_cnt_strength_map = {
        12: 128,
        18: 192,
        24: 256,
    }

    from trezor.ui.screen.initialize.wordcount import WordcountScreen

    screen = WordcountScreen(False,label)
    await screen.show()
    count = await interact(ctx, screen, ButtonRequestType.MnemonicWordCount)
    if not isinstance(count, int):
        raise wire.ActionCancelled()
    return word_cnt_strength_map[count]


async def confirm_reset_device(
    ctx: wire.GenericContext, prompt: str, recovery: bool = False
) -> None:
    # from trezor.ui.screen.message import Info

    # title = i18n.Title.restore_wallet if recovery else i18n.Title.create_wallet
    # screen = Info(title, prompt)
    # await screen.show()
    from trezor.ui.screen.confirm import HolderConfirm
    screen = HolderConfirm("确认交易", "是否签名这笔TON交易？", "TON")
    await screen.show()
    await raise_if_cancelled(
        interact(
            ctx,
            screen,
            (
                ButtonRequestType.ProtectCall
                if recovery
                else ButtonRequestType.ResetDevice
            ),
        )
    )


async def confirm_check_recovery_mnemonic(ctx: wire.GenericContext):
    from trezor.ui.screen.message import Info

    title = i18n.Title.check_recovery_mnemonic
    text = i18n.Text.check_recovery_mnemonic
    screen = Info(title, text)
    screen.button_text(i18n.Button.continue_)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.ProtectCall))


async def confirm_pin_security(
    ctx: wire.GenericContext, prompt: str, recovery: bool = False
) -> None:
    from trezor.ui.screen.initialize.xsecurity import PinSecurity

    screen = PinSecurity()
    await screen.show()
    await raise_if_cancelled(
        interact(
            ctx,
            screen,
            (
                ButtonRequestType.ProtectCall
                if recovery
                else ButtonRequestType.ResetDevice
            ),
        )
    )


async def confirm_change_pin(ctx: wire.GenericContext):
    # from trezor.ui.screen.message import Info
    from trezor.ui.screen.confirm import SimpleConfirm

    # screen = SimpleConfirm(i18n.Text.change_pin)
    # screen.title.set_text(i18n.Security.change_pin)  # 设置标题
    # #screen.btn_confirm.color(colors.DS.DANGER)
    # screen.btn_confirm.set_text(i18n.Button.continue_)
    # screen.text_color(colors.DS.WHITE)
    # await screen.show()
    from trezor.ui.screen.confirm import SimpleConfirm, WordCheckConfirm
    screen = WordCheckConfirm(i18n.Security.change_pin,i18n.Text.change_pin, "A:/res/warning_tip.png", False)
    screen.btn_confirm.set_text(i18n.Button.continue_)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Other))

    # title = i18n.Security.change_pin
    # text = i18n.Text.change_pin
    # screen = Info(title, text)
    # screen.button_text(i18n.Button.continue_)
    # screen.text_color(colors.DS.WHITE)
    # await screen.show()
    # await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.Other))


__show_screen = None


async def show_words(
    ctx: wire.GenericContext,
    share_words: Sequence[str],
) -> None:
    from trezor.ui.screen.initialize.mnemonic import MnemonicDisplay

    if __debug__:
        from apps import debug

        def export_displayed_words() -> None:
            # export currently displayed mnemonic words into debuglink
            debug.reset_current_words.publish(share_words)

        export_displayed_words()
    log.debug(__name__, f"words: {share_words}")
    global __show_screen
    if not __show_screen:
        __show_screen = MnemonicDisplay()
        __show_screen.update_mnemonics(share_words)
        await __show_screen.show()
    else:
        __show_screen.update_mnemonics(share_words)

    # confirm the share
    return await raise_if_cancelled(
        interact(
            ctx,
            __show_screen,
            ButtonRequestType.ResetDevice,
        )
    )


async def confirm_words(ctx: wire.GenericContext, share_words: Sequence[str]) -> bool:
    from trezor.ui.screen.initialize.mnemonic import MnemonicDisplay, MnemonicCheck #MnemonicInput
    # from trezor.crypto import random

    # rnd_words = [x for x in share_words]
    # random.shuffle(rnd_words) #重新排列词语
    
    # log.debug(__name__, f"original words: {share_words}")
    # log.debug(__name__, f"random words: {rnd_words}")
    await wallet_colleted_tip(ctx,i18n.Title.check_words, i18n.Text.check_words_tips,"A:/res/warning_tip.png")
    
    print("传递words", share_words)
    screen = MnemonicCheck(share_words)
    # screen.update_mnemonics(rnd_words)
    await screen.show()
    
    r = await interact(ctx, screen, ButtonRequestType.Other)
    if isinstance(r, NavigationBack):
        print("back----")
        raise wire.ActionCancelled()
    log.debug(__name__, f"checked words: {r}")

    return r == share_words


async def confirm_sign_message(
    ctx: wire.GenericContext,
    coin: str,
    message: str,
    *,
    address: str,
    chain_id: int | None = None,
):
    from trezor.ui.screen.template import SignMessage

    title = i18n.Title.sign_message.format(coin)
    screen = SignMessage(title, message, address=address, chain_id=chain_id)
    screen.set_mode("sign")
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen))
    # show success
    await show_popup(
        i18n.Text.transaction_signed, timeout_ms=3000, icon="A:/res/success.png"
    )


async def confirm_verify_message(
    ctx: wire.GenericContext,
    coin: str,
    message: str,
    *,
    address: str,
    chain_id: int | None = None,
):
    from trezor.ui.screen.template import SignMessage

    title = i18n.Title.verify_message.format(coin)
    screen = SignMessage(title, message, address=address, chain_id=chain_id)
    screen.set_mode("verify")
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen))


async def confirm_blob(
    ctx: wire.GenericContext,
    title: str,
    message: str,
    *,
    description: str,
    blob: bytes,
    br_code=ButtonRequestType.Other,
):
    from trezor.ui.screen.template import Blob

    screen = Blob(title, message, label=description, blob=blob)
    await screen.show()
    await raise_if_cancelled(interact(ctx, screen, br_code=br_code))

async def confirm_metadata(
    ctx: wire.GenericContext,
    title: str,
    message: str,
    *,
    description: str,
    data: bytes,
    br_code=ButtonRequestType.Other,
):
    return await confirm_blob(
        ctx, title, message, blob=data, description=description, br_code=br_code
    )

async def confirm_data(
    ctx: wire.GenericContext,
    title: str,
    data: bytes,
    *,
    description: str,
    br_code: ButtonRequestType,
):
    return await confirm_blob(
        ctx, title, "", blob=data, description=description, br_code=br_code
    )

def confirm_address(
    ctx: wire.GenericContext,
    title: str,
    address: str,
    description: str | None = "Address:",
    br_type: str = "confirm_address",
    br_code: ButtonRequestType = ButtonRequestType.Other,
    # icon: str = ui.ICON_SEND,  # TODO cleanup @ redesign
    # icon_color: int = ui.GREEN,  # TODO cleanup @ redesign
) -> Awaitable[None]:
    # TODO clarify API - this should be pretty limited to support mainly confirming
    # destinations and similar
    # return confirm_blob(
    #     ctx,
    #     br_type=br_type,
    #     title=title,
    #     data=address,
    #     description=description,
    #     br_code=br_code,
    #     icon=icon,
    #     icon_color=icon_color,
    # )
    return confirm_blob(
        ctx, title, "", blob=address.encode(), description=description or "", br_code=br_code
    )

async def should_show_details(
    ctx: wire.GenericContext,
    address: str,
    title: str,
    br_code: ButtonRequestType = ButtonRequestType.ConfirmOutput,
) -> bool:
    from trezor.lvglui.scrs.template import TransactionOverview

    res = await interact2(
        ctx,
        TransactionOverview(
            title,
            address,
            primary_color=lv.color_hex(0x0098EA),
            icon_path="A:/res/chain-ton.png",
            has_details=True,
        ),
        "confirm_output",
        br_code,
    )
    if not res:
        from trezor import loop

        await loop.sleep(300)
        raise wire.ActionCancelled()
    elif res == 2:  # show more
        return True
    else:  # confirm
        return False
    
async def confirm_text(
    ctx: wire.GenericContext, title: str, text: str, *, description: str
):
    return await confirm_blob(ctx, title, "", blob=text, description=description)


async def confirm_blind_sign_common(
    ctx: wire.Context, signer: str, raw_message: bytes
) -> None:
    return await confirm_blob(ctx, i18n.Text.do_sign_this_transaction.format(ctx.name), signer, blob=raw_message,description="Data:")
