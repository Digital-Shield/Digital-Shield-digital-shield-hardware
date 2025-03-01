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
