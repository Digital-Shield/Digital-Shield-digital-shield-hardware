from trezor import wire
from trezor.enums import ButtonRequestType
from .helper import raise_if_cancelled, interact

from trezor.ui.layouts.bitcoin import (
    # reuse
    confirm_output
)

from trezor.ui.layouts.ethereum import (
    # reuse
    confirm_address,
)

async def confirm_freeze(
    ctx: wire.GenericContext,
    sender: str,
    resource: str | None = None,
    balance: str | None = None,
    duration: str | None = None,
    receiver: str | None = None,
) -> None:
    from trezor.ui.screen.tron import Asset

    screen = Asset(
        sender,
        mode='freeze',
        resource=resource,
        balance=balance,
        duration=duration,
        receiver=receiver,
    )
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ProtectCall)
    )

async def confirm_unfreeze(
    ctx: wire.GenericContext,
    sender: str,
    resource: str | None = None,
    balance: str | None = None,
    duration: str | None = None,
    receiver: str | None = None,
) -> None:
    from trezor.ui.screen.tron import Asset

    screen = Asset(
        sender,
        mode='unfreeze',
        resource=resource,
        balance=balance,
        duration=duration,
        receiver=receiver,
    )
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ProtectCall)
    )

async def confirm_delegate(
    ctx: wire.GenericContext,
    sender: str,
    resource: str | None = None,
    balance: str | None = None,
    receiver: str | None = None,
    lock: str| None = None,
) -> None:
    from trezor.ui.screen.tron import Asset

    screen = Asset(
        sender,
        mode='delegate',
        resource=resource,
        balance=balance,
        receiver=receiver,
        lock=lock,
    )
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ProtectCall)
    )

async def confirm_undelegate(
    ctx: wire.GenericContext,
    sender: str,
    resource: str | None = None,
    balance: str | None = None,
    receiver: str | None = None,
    lock: str| None = None,
) -> None:
    from trezor.ui.screen.tron import Asset

    screen = Asset(
        sender,
        mode='undelegate',
        resource=resource,
        balance=balance,
        receiver=receiver,
        lock=lock,
    )
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.ProtectCall)
    )

async def confirm_total(
    ctx: wire.GenericContext,
    from_address: str | None,
    to_address: str | None,
    amount: str,
    fee_max: str,
    total_amount: str | None,
) -> None:
    from trezor.ui.screen.tron import TransactionDetail

    screen = TransactionDetail(
        amount,
        from_address,
        to_address,
        fee_max,
        total_amount=total_amount,
    )
    await raise_if_cancelled(
        interact(ctx, screen, ButtonRequestType.SignTx)
    )
