from .helper import interact, raise_if_cancelled

from trezor.enums import ButtonRequestType
from trezor import wire
from trezor.ui import i18n
from trezor.ui.screen.bitcoin import (
    PublicKey,
    XPub,
    PaymentRequest,
    OutputChange,
    FeeChange,
)


async def show_multisig_address():
    raise NotImplementedError()


async def show_pubkey(
    ctx: wire.GenericContext,
    pubkey: str,
    path: str,
    network: str,
):
    screen = PublicKey(pubkey, path, network)
    await screen.show()
    await interact(ctx, screen, ButtonRequestType.Address)


async def show_xpub(
    ctx: wire.GenericContext,
    xpub: str,
    path: str,
    network: str,
):
    screen = XPub(xpub, path, network)
    await screen.show()
    await interact(ctx, screen, ButtonRequestType.Address)


async def confirm_output(
    ctx: wire.GenericContext,
    address: str,
    amount: str,
):
    from trezor.ui.screen.bitcoin import Output

    screen = Output(to=address, amount=amount)
    await screen.show()
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.SignTx))


async def confirm_payment_request(
    ctx: wire.GenericContext,
    recipient_name: str,
    amount: str,
    memos: list[str],
    coin: str,
):
    message = " ".join(memos)
    screen = PaymentRequest(
        i18n.Title.x_confirm_payment.format(coin),
        amount,
        recipient_name,
        message=message,
    )
    return await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ConfirmOutput)
    )


async def confirm_replacement(
    ctx: wire.GenericContext,
    description: str,
    txid: str,
):
    from . import confirm_text

    return await confirm_text(
        ctx, i18n.Title.confirm_replacement, description=description, txid=txid
    )


async def confirm_modify_output(
    ctx: wire.GenericContext,
    address: str,
    sign: int,
    amount_change: str,
    amount_new: str,
) -> None:
    if sign < 0:
        description = i18n.Text.amount_increased
    else:
        description = i18n.Text.amount_decreased

    screen = OutputChange(amount_new, address, amount_change, description)
    await raise_if_cancelled(
        interact(
            ctx,
            screen,
            ButtonRequestType.ConfirmOutput,
        )
    )

async def confirm_modify_fee(
    ctx: wire.GenericContext,
    fee_new: str,
    sign: int,
    fee_change: str,
) -> None:
    if sign < 0:
        description = i18n.Text.fee_decreased
    elif sign == 0:
        description = i18n.Text.fee_unchanged
    else:
        description = i18n.Text.fee_increased

    screen = FeeChange(fee_new, fee_change, description)
    return await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.SignTx)
    )

async def confirm_total(
    ctx: wire.GenericContext,
    total_amount: str,
    fee_amount: str,
    amount: str | None = None,
    coin: str = "BTC",
) -> None:
    from trezor.ui.screen.bitcoin import Total
    screen = Total(amount, fee_amount, total_amount, coin)
    return await raise_if_cancelled(interact(ctx, screen, ButtonRequestType.SignTx))

async def confirm_joint_total(
    ctx: wire.GenericContext,
    spending_amount: str,
    total_amount: str,
    coin: str = "BTC",
) :
    from trezor.ui.screen.bitcoin import JointAmount
    screen = JointAmount(spending_amount, total_amount, coin)

    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.SignTx)
    )

async def confirm_coinjoin(
    ctx: wire.GenericContext, coin_name: str, max_rounds: int, max_fee_per_vbyte: str
) -> None:
    raise NotImplementedError()
