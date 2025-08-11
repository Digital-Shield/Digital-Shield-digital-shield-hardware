import lvgl as lv
import utime
from typing import Any, NoReturn

import storage.cache
import storage.sd_salt
from trezor import config, loop, wire

from .sdcard import request_sd_salt

from trezor.ui import i18n

def can_lock_device() -> bool:
    """Return True if the device has a PIN set or SD-protect enabled."""
    return config.has_pin() or storage.sd_salt.is_enabled()

async def request_pin(
    ctx: wire.GenericContext,
    prompt: str = "",
    attempts_remaining: int | None = None,
    allow_cancel: bool = True,
    **kwargs: Any,
) -> str:
    from trezor.ui.layouts import request_pin_on_device

    return await request_pin_on_device(ctx, prompt, attempts_remaining, allow_cancel)


async def request_pin_confirm(ctx: wire.Context, *args: Any, **kwargs: Any) -> str:
    while True:
        pin1 = await request_pin(
            ctx, i18n.Title.enter_new_pin, *args, **kwargs
        )
        pin2 = await request_pin(
            ctx, i18n.Title.enter_pin_again, *args, **kwargs
        )
        if pin1 == pin2:
            return pin1

        await pin_mismatch(ctx)


async def pin_mismatch(ctx) -> None:
    from trezor.ui.layouts import show_warning
    title = i18n.Title.pin_not_match
    msg = i18n.Text.pin_not_match
    from trezor.ui.screen.confirm import SimpleConfirm, WordCheckConfirm
    screen = WordCheckConfirm(i18n.Title.pin_not_match,i18n.Text.pin_not_match,"A:/res/mach_error.png",False)
    # screen = SimpleConfirm("确定要终止核对吗？")
    screen.btn_confirm.delete()
    screen.btn_cancel.set_text(i18n.Button.try_again)
    screen.btn_cancel.set_style_width(440, lv.PART.MAIN)
    screen.btn_cancel.set_style_height(89, lv.PART.MAIN)
    screen.btn_cancel.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
    await screen.show()
    r = await screen
    # if isinstance(r, Confirm):
    #     from trezor.ui import NavigationBack
    #     ctx.publish(NavigationBack())
    
    # await show_warning(
    #     ctx,
    #     title=title,
    #     msg=msg,
    #     button=i18n.Button.try_again,
    # )
async def request_pin_and_sd_salt(
    ctx: wire.Context,
    prompt: str = "",
    allow_cancel: bool = True,
) -> tuple[str, bytearray | None]:
    if config.has_pin():
        pin = await request_pin(ctx, prompt, config.get_pin_rem(), allow_cancel)
        config.ensure_not_wipe_code(pin)
    else:
        pin = ""

    salt = await request_sd_salt(ctx)

    return pin, salt


def _set_last_unlock_time() -> None:
    now = utime.ticks_ms()
    storage.cache.set_int(storage.cache.APP_COMMON_REQUEST_PIN_LAST_UNLOCK, now)


def _get_last_unlock_time() -> int:
    return storage.cache.get_int(storage.cache.APP_COMMON_REQUEST_PIN_LAST_UNLOCK) or 0


async def verify_user_pin(
    ctx: wire.GenericContext = wire.DUMMY_CONTEXT,
    prompt: str = i18n.Title.enter_pin, #请输入pin码
    allow_cancel: bool = True,
    retry: bool = True,
    cache_time_ms: int = 0,
    re_loop: bool = False,
    callback=None,
) -> None:
    last_unlock = _get_last_unlock_time()
    if (
        cache_time_ms
        and last_unlock
        and utime.ticks_ms() - last_unlock <= cache_time_ms
        and config.is_unlocked()
    ):
        return
    if config.has_pin():
        from trezor.ui.layouts import request_pin_on_device

        pin = await request_pin_on_device(
            ctx, prompt, config.get_pin_rem(), allow_cancel
        )

        config.ensure_not_wipe_code(pin)
    else:
        pin = ""
    salt = await request_sd_salt(ctx)
    if config.unlock(pin, salt):
        if re_loop:
            loop.clear()
        elif callback:
            callback()
        _set_last_unlock_time()
        return
    elif not config.has_pin():
        raise RuntimeError
    while retry:
        pin_rem = config.get_pin_rem()
        pin = await request_pin_on_device(  # type: ignore ["request_pin_on_device" is possibly unbound]
            ctx, i18n.Title.enter_pin, pin_rem, allow_cancel
        )
        if config.unlock(pin, salt):
            if re_loop:
                loop.clear()
            elif callback:
                callback()
            _set_last_unlock_time()
            return

    raise wire.PinInvalid


async def error_pin_invalid(ctx: wire.Context) -> NoReturn:
    from trezor.ui.layouts import show_error

    await show_error(
        ctx,
        title= i18n.Title.wrong_pin,
        msg= i18n.Text.wrong_pin,
    )
    raise wire.PinInvalid


async def error_pin_matches_wipe_code(ctx: wire.Context) -> NoReturn:
    from trezor.ui.layouts import show_error

    await show_error(
        ctx,
        title="Invalid PIN",
        msg="The new PIN must be different from your\nwipe code.",
    )
    raise wire.PinInvalid
