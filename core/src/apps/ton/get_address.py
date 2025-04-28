from typing import TYPE_CHECKING

from trezor import wire
# from trezor.enums import TonWalletVersion, TonWorkChain
# from trezor.lvglui.scrs import lv
import lvgl as lv
from trezor.messages import TonAddress, TonGetAddress
from trezor.ui.layouts import show_address

from apps.common.ton import paths, seed
from apps.common.ton.keychain import Keychain, auto_keychain

from . import ICON, PRIMARY_COLOR
from .tonsdk.contract.wallet import Wallets, WalletVersionEnum

if TYPE_CHECKING:
    from trezor.wire import Context

V4R2 = 3
BASECHAIN = 0
MASTERCHAIN = 1

@auto_keychain(__name__)
async def get_address(
    ctx: Context, msg: TonGetAddress, keychain: Keychain
) -> TonAddress:
    #打印Keychain
    # print("keychain--"+str(keychain))
    # print("address_n--in--"+str(msg.address_n))
    # await paths.validate_path(ctx, keychain, msg.address_n)

    node = keychain.derive(msg.address_n)
    public_key = seed.remove_ed25519_prefix(node.public_key())
    workchain = (
        -1 if msg.workchain == MASTERCHAIN else BASECHAIN
    )

    if msg.wallet_version == V4R2:
        wallet_version = WalletVersionEnum.v4r2
    else:
        raise wire.DataError("Invalid wallet version.")
    #打印public_key=public_key, wallet_id=msg.wallet_id, wc=workchain这些内容
    # print("public_key=",public_key)
    # print("wallet_id=",msg.wallet_id)
    # print("wc=",workchain)
    wallet = Wallets.ALL[wallet_version](
        public_key=public_key, wallet_id=msg.wallet_id, wc=workchain
    )
    address = wallet.address.to_string(
        is_user_friendly=True,
        is_url_safe=True,
        is_bounceable=msg.is_bounceable,
        is_test_only=msg.is_testnet_only,
    )
    print("address=",address)
    # address =  "tryrtytryuuroweiureweoir"
    if msg.show_display:
        path = paths.address_n_to_str(msg.address_n)
        ctx.primary_color, ctx.icon_path = lv.color_hex(PRIMARY_COLOR), ICON
        await show_address(
            ctx,
            address=address,
            path=path,
            network="TON",
        )

    return TonAddress(address=address)
