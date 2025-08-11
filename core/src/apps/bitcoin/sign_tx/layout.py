from micropython import const
from typing import TYPE_CHECKING
from ubinascii import hexlify

from trezor import utils, wire
from trezor.enums import AmountUnit, ButtonRequestType, OutputScriptType
from trezor.ui import i18n
from trezor.strings import format_amount, format_timestamp
from trezor.ui import layouts

from .. import addresses
from ..common import format_fee_rate
from . import omni

if not utils.BITCOIN_ONLY:
    from trezor.ui.layouts import altcoin
from ...ethereum.layout import (
    require_confirm_fee_ton,
)


if TYPE_CHECKING:
    from typing import Any

    from trezor.messages import TxAckPaymentRequest, TxOutput

    from apps.common.coininfo import CoinInfo

_LOCKTIME_TIMESTAMP_MIN_VALUE = const(500_000_000)


def format_coin_amount(amount: int, coin: CoinInfo, amount_unit: AmountUnit) -> str:
    decimals, shortcut = coin.decimals, coin.coin_shortcut
    if amount_unit == AmountUnit.SATOSHI:
        decimals = 0
        shortcut = "sat"
        if coin.coin_shortcut != "BTC":
            shortcut += " " + coin.coin_shortcut
    elif amount_unit == AmountUnit.MICROBITCOIN and decimals >= 6:
        decimals -= 6
        shortcut = "u" + shortcut
    elif amount_unit == AmountUnit.MILLIBITCOIN and decimals >= 3:
        decimals -= 3
        shortcut = "m" + shortcut
    # we don't need to do anything for AmountUnit.BITCOIN
    return f"{format_amount(amount, decimals)} {shortcut}"


async def confirm_output(
    ctx: wire.Context, output: TxOutput, coin: CoinInfo, amount_unit: AmountUnit
) -> None:
    if output.script_type == OutputScriptType.PAYTOOPRETURN:
        data = output.op_return_data
        # print("这是her1--")
        assert data is not None
        if omni.is_valid(data):
            # OMNI transaction
            layout = layouts.confirm_data(
                ctx,
                "OMNI transaction",
                description="Omni",
                data=omni.parse(data),
                br_code=ButtonRequestType.ConfirmOutput,
            )
        else:
            # generic OP_RETURN
            # print("这是her2--")
            layout = layouts.confirm_data(
                ctx,
                "OP_RETURN",
                description="OP_RETURN",
                blob=data,
                br_code=ButtonRequestType.ConfirmOutput,
            )
    else:
        assert output.address is not None
        print("这是输出地址--",output.address)
        address_short = addresses.address_short(coin, output.address)
        print("这是地址--",address_short)
        print("金额--",format_coin_amount(output.amount, coin, amount_unit))
        print("network--",coin.coin_name)
        chain_id = 20
        if coin.coin_name == "Litecoin":
            chain_id = 2
        elif coin.coin_name == "Dogecoin":
            chain_id = 2000

        decimals = coin.decimals
        if amount_unit == AmountUnit.SATOSHI:
            decimals = 0
        elif amount_unit == AmountUnit.MICROBITCOIN and decimals >= 6:
            decimals -= 6
        elif amount_unit == AmountUnit.MILLIBITCOIN and decimals >= 3:
            decimals -= 3
        print("decimals--",decimals)
        # layout = layouts.bitcoin.confirm_output(
        #     ctx,
        #     address_short,
        #     format_coin_amount(output.amount, coin, amount_unit),
        # )
        await require_confirm_fee_ton(
            ctx,
            output.amount,
            0,
            1,
            chain_id,
            None,
            from_address="",
            to_address=address_short,
            contract_addr=None,
            token_id=None,
            evm_chain_id=None,
            raw_data=None,
            decimals=decimals,
        )
        from trezor.ui.layouts import confirm_final
        await confirm_final(ctx, coin.coin_name)

#  # await layout
# def format_coin_amount(amount: int, coin: CoinInfo, amount_unit: AmountUnit) -> str:
   
#     # we don't need to do anything for AmountUnit.BITCOIN
#     return decimals

async def confirm_decred_sstx_submission(
    ctx: wire.Context, output: TxOutput, coin: CoinInfo, amount_unit: AmountUnit
) -> None:
    assert output.address is not None
    address_short = addresses.address_short(coin, output.address)

    await altcoin.confirm_decred_sstx_submission(
        ctx, address_short, format_coin_amount(output.amount, coin, amount_unit)
    )


async def confirm_payment_request(
    ctx: wire.Context,
    msg: TxAckPaymentRequest,
    coin: CoinInfo,
    amount_unit: AmountUnit,
) -> Any:
    memo_texts = []
    for m in msg.memos:
        if m.text_memo is not None:
            memo_texts.append(m.text_memo.text + " ")
        elif m.refund_memo is not None:
            pass
        elif m.coin_purchase_memo is not None:
            memo_texts.append(f" Buying {m.coin_purchase_memo.amount}.")
        else:
            raise wire.DataError("Unrecognized memo type in payment request memo.")

    assert msg.amount is not None

    return await layouts.bitcoin.confirm_payment_request(
        ctx,
        msg.recipient_name,
        format_coin_amount(msg.amount, coin, amount_unit),
        memo_texts,
        coin=coin.coin_name,
    )


async def confirm_replacement(ctx: wire.Context, description: str, txid: bytes) -> None:
    await layouts.bitcoin.confirm_replacement(
        ctx,
        description,
        hexlify(txid).decode(),
    )


async def confirm_modify_output(
    ctx: wire.Context,
    txo: TxOutput,
    orig_txo: TxOutput,
    coin: CoinInfo,
    amount_unit: AmountUnit,
) -> None:
    assert txo.address is not None
    address_short = addresses.address_short(coin, txo.address)
    amount_change = txo.amount - orig_txo.amount
    await layouts.bitcoin.confirm_modify_output(
        ctx,
        address_short,
        amount_change,
        format_coin_amount(abs(amount_change), coin, amount_unit),
        format_coin_amount(txo.amount, coin, amount_unit),
    )


async def confirm_modify_fee(
    ctx: wire.Context,
    user_fee_change: int,
    total_fee_new: int,
    fee_rate: float,
    coin: CoinInfo,
    amount_unit: AmountUnit,
) -> None:
    await layouts.bitcoin.confirm_modify_fee(
        ctx,
        format_coin_amount(total_fee_new, coin, amount_unit),
        user_fee_change,
        format_coin_amount(abs(user_fee_change), coin, amount_unit),
    )


async def confirm_joint_total(
    ctx: wire.Context,
    spending: int,
    total: int,
    coin: CoinInfo,
    amount_unit: AmountUnit,
) -> None:
    await layouts.bitcoin.confirm_joint_total(
        ctx,
        spending_amount=format_coin_amount(spending, coin, amount_unit),
        total_amount=format_coin_amount(total, coin, amount_unit),
        coin=coin.coin_name,
    )


async def confirm_total(
    ctx: wire.Context,
    spending: int,
    fee: int,
    fee_rate: float,
    coin: CoinInfo,
    amount_unit: AmountUnit,
) -> None:
    await layouts.bitcoin.confirm_total(
        ctx,
        total_amount=format_coin_amount(spending, coin, amount_unit),
        fee_amount=format_coin_amount(fee, coin, amount_unit),
        amount=format_coin_amount(spending - fee, coin, amount_unit),
        coin=coin.coin_name,
    )


async def confirm_feeoverthreshold(
    ctx: wire.Context, fee: int, coin: CoinInfo, amount_unit: AmountUnit
) -> None:
    fee_amount = format_coin_amount(fee, coin, amount_unit)
    await layouts.confirm_metadata(
        ctx,
        i18n.Title.high_fee,
        i18n.Text.fee_is_unexpectedly_high,
        fee_amount,
        description=i18n.Text.fee,
        br_code=ButtonRequestType.FeeOverThreshold,
    )


async def confirm_change_count_over_threshold(
    ctx: wire.Context, change_count: int
) -> None:
    await layouts.confirm_metadata(
        ctx,
        i18n.Title.warning,
        i18n.Text.too_many_change_outputs,
        br_code=ButtonRequestType.SignTx,
        description= i18n.Text.change_count,
        data = str(change_count),
    )


async def confirm_unverified_external_input(ctx: wire.Context) -> None:
    await layouts.confirm_metadata(
        ctx,
        "unverified_external_input",
        "Warning",
        "The transaction contains unverified external inputs.",
        br_code=ButtonRequestType.SignTx,
    )


async def confirm_nondefault_locktime(
    ctx: wire.Context, lock_time: int, lock_time_disabled: bool
) -> None:
    if lock_time_disabled:
        title = i18n.Title.warning
        text = i18n.Text.locktime_will_have_no_effect
        param: str | None = None
        description = None
    else:
        title = i18n.Title.confirm_locktime
        text = i18n.Text.confirm_locktime_for_this_transaction
        if lock_time < _LOCKTIME_TIMESTAMP_MIN_VALUE:
            param = str(lock_time)
            description = i18n.Text.block_height
        else:
            param = format_timestamp(lock_time)
            description = i18n.Text.time

    await layouts.confirm_metadata(
        ctx,
        "nondefault_locktime",
        title,
        text,
        param,
        br_code=ButtonRequestType.SignTx,
        description=description,
    )
