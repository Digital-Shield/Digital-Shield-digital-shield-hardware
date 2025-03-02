from trezor import wire
from trezor.enums import ButtonRequestType
from .helper import raise_if_cancelled, interact

from trezor.ui.layouts.bitcoin import (
    # reuse
    confirm_output
)

async def confirm_sol_transfer(ctx: wire.GenericContext, from_addr: str, to_addr: str, amount: str) -> None:
    from trezor.ui.screen.solana import TransactionDetail

    screen = TransactionDetail(
        amount=amount,
        from_=from_addr,
        to=to_addr,
        total=None,
    )
    await screen.show()
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ProtectCall)
    )


async def confirm_sol_create_ata(
    ctx: wire.GenericContext,
    fee_payer: str,
    funding_account: str,
    associated_token_account: str,
    wallet_address: str,
    token_mint: str,
):
    from trezor.ui.screen.template import UnImplemented
    screen = UnImplemented()
    await screen.show()
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ProtectCall)
    )

    raise wire.UnexpectedMessage("Not implemented yet")

async def confirm_sol_token_transfer(
    ctx: wire.GenericContext,
    from_addr: str,
    to_addr: str,
    amount: str,
    source_owner: str,
    fee_payer: str,
    token_mint: str = None,
):
    from trezor.ui.screen.solana import SPLTokenTransactionDetail
    screen = SPLTokenTransactionDetail(
        from_addr=from_addr,
        to_addr=to_addr,
        amount=amount,
        source_owner=source_owner,
        fee_payer=fee_payer,
        token_mint=token_mint,
    )
    await screen.show()
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ProtectCall)
    )


async def confirm_sol_blinding_sign(
    ctx: wire.GenericContext, fee_payer: str, message_hex: str
) -> None:
    from trezor.ui.screen.template import UnImplemented
    screen = UnImplemented()
    await screen.show()
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ProtectCall)
    )

    raise wire.UnexpectedMessage("Not implemented yet")
