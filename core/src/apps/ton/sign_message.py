from typing import TYPE_CHECKING

from trezor import wire
from trezor.crypto.curve import ed25519
from trezor.crypto.hashlib import sha256
from trezor.enums import TonWalletVersion, TonWorkChain
import lvgl as lv
from trezor.messages import TonSignedMessage, TonSignMessage, TonTxAck

from apps.common.ton import paths, seed
from apps.common.ton.keychain import Keychain, auto_keychain

from . import ICON, PRIMARY_COLOR, tokens
from .layout import require_confirm_fee, require_show_overview
from .tonsdk.boc._cell import validate_cell_repr
from .tonsdk.contract.token.ft import JettonWallet
from .tonsdk.contract.wallet import Wallets, WalletVersionEnum
from .tonsdk.utils._address import Address
from ..ethereum.layout import (
    require_confirm_fee_ton,
    require_show_overview_ton,
)
# from tonsdk.contract.wallet import  _wallet_contract
# from trezor.crypto import base64
# import requests
if TYPE_CHECKING:
    from trezor.wire import Context


@auto_keychain(__name__)
async def sign_message(
    ctx: Context, msg: TonSignMessage, keychain: Keychain
) -> TonSignedMessage:
    if __debug__:
        from trezor.utils import dump_protobuf_lines
        print("\n".join(dump_protobuf_lines(msg)))
        print("这是接收的参数: ", msg)

    # await paths.validate_path(ctx, keychain, msg.address_n)

    node = keychain.derive(msg.address_n)
    public_key = seed.remove_ed25519_prefix(node.public_key())
    workchain = (
        -1 if msg.workchain == TonWorkChain.MASTERCHAIN else TonWorkChain.BASECHAIN
    )

    if msg.wallet_version == TonWalletVersion.V4R2:
        wallet_version = WalletVersionEnum.v4r2
    else:
        raise wire.DataError("Invalid wallet version.")

    init_data = bytes()

    if msg.init_data_initial_chunk is not None:
        init_data += msg.init_data_initial_chunk

    data_total = msg.init_data_length if msg.init_data_length is not None else 0
    data_left = max(0, data_total - len(init_data))

    while data_left > 0:
        resp = await send_request_chunk(ctx, data_left)
        init_data_chunk = resp.init_data_chunk
        data_left -= len(init_data_chunk)
        init_data += init_data_chunk

    # jetton_amount = check_jetton_transfer(msg)
    print("public_key: ", public_key)
    print("private_key: ", node.private_key())
    wallet = Wallets.ALL[wallet_version](
        public_key=public_key, private_key = node.private_key() + public_key, wallet_id=698983191, wc=workchain
    )
    address = wallet.address.to_string(
        is_user_friendly=True,
        is_url_safe=True,
        is_bounceable=msg.is_bounceable,
        is_test_only=msg.is_testnet_only,
    )
    #从这个地方前边都是获取当前钱包的地址
    # display
    ctx.primary_color, ctx.icon_path = lv.color_hex(PRIMARY_COLOR), ICON
    from trezor.ui.layouts import confirm_final #, confirm_unknown_token_transfer

    token = None
    recipient = Address(msg.destination).to_string(True, True)


    amount = msg.ton_amount #jetton_amount if jetton_amount else
    if amount is None:
        raise ValueError("Amount cannot be None")

    # if jetton_amount:
    #     body = JettonWallet().create_transfer_body(
    #         Address(msg.address),
    #         jetton_amount,
    #         msg.fwd_fee,
    #         msg.comment,
    #         wallet.address,
    #     )
    #     payload = body
    # else:
    payload = ""

     # 如果 seqno = 0，说明钱包还未激活，需要带上 state_init 激活信息
    if msg.seqno == 0:
        # 构建初始化状态数据（激活用）
        state_init = bytes(wallet.create_state_init()['state_init'].to_boc())
        # print("state_init0: ", state_init)
    else:
        # 已激活钱包则无需携带
        state_init = bytes()
    print("msg.address_n: ", msg.address_n)
    print("msg.address: ", msg.destination)
    print("msg.seqno: ", msg.seqno)
    print("msg.valid_until: ", msg.expire_at)
    print("msg.amount: ", msg.ton_amount)
    try:
        digest, boc = wallet.create_transaction_digest(
            to_addr=msg.destination,
            amount=msg.ton_amount,
            seqno=msg.seqno,
            expire_at=msg.expire_at,
            payload=payload,
            is_raw_data=False,
            send_mode=msg.mode,
            state_init=state_init,
            private_key=node.private_key(),
        )
    except Exception as e:
        print(e)
        if msg.signing_message_repr is not None:
            validate_cell_repr(msg.signing_message_repr)
            boc = msg.signing_message_repr
            from trezor.ui.layouts import confirm_blind_sign_common

            await confirm_blind_sign_common(ctx, address, msg.signing_message_repr)
            await confirm_final(ctx, "TON")
            digest = sha256(msg.signing_message_repr).digest()
            signature = ed25519.sign(node.private_key(), digest)
            return TonSignedMessage(signature=bytes(boc), signning_message=None)
        else:
            raise wire.DataError("Parse boc failed.")
    # print(f"Recipient: {recipient}, Amount: {amount}, Token: {token}")

    print("msg.amount--",msg.ton_amount)

    show_details = await require_show_overview_ton(
        ctx,
        "TON",
        msg.destination,
        msg.ton_amount,
        0,
        token,
        False,
    )
    await require_confirm_fee_ton(
        ctx,
        msg.ton_amount,
        0,
        1,
        -11,
        token,
        from_address=address,
        to_address=msg.destination,
        contract_addr=None,
        token_id=None,
        evm_chain_id=None,
        raw_data=None,
    )
    await confirm_final(ctx, "TON")
    # if show_details:
    #     has_raw_data = False
    #     # await require_confirm_data(ctx, msg.data_initial_chunk, data_total)
    #     node = keychain.derive(msg.address_n)
    #     await require_confirm_fee_ton(
    #         ctx,
    #         msg.amount,
    #         0,
    #         1,
    #         0,
    #         token,
    #         from_address=address,
    #         to_address=msg.address,
    #         contract_addr="0x",
    #         token_id=1,
    #         evm_chain_id=None,
    #         raw_data=None,
    #     )


    # await confirm_final(ctx, "TON")
    signature = ed25519.sign(node.private_key(), digest)
    print("signature------: ", signature)
    # print("boc------: ", boc)
    from binascii import a2b_base64, b2a_base64, unhexlify
    boc_b64 = b2a_base64(boc).decode("utf-8")
    # print("signature------: ", b2a_base64(signature).decode("utf-8"))
    print("boc_b64------: ", boc_b64)
    #广播
    # res = requests.post(
    #     "https://toncenter.com/api/v2/sendBoc",
    #     headers={"X-API-Key": "319e1b21f3d6367aef8194daa7883bc002500799d705703be609488b6fb27a49"},
    #     json={"boc": boc_b64}
    # )

    # print(res.json())
    return TonSignedMessage(signature=bytes(boc), signning_message=signature)

def string_to_bytes(string, size=1):  # ?
    if size == 1:
        buf = bytearray(len(string))
    elif size == 2:
        buf = bytearray(len(string) * 2)
    elif size == 4:
        buf = bytearray(len(string) * 4)
    else:
        raise Exception("Invalid size")

    for i, c in enumerate(string):
        # buf[i] = ord(c)
        buf[i] = c  # ?

    return bytes(buf)

def check_jetton_transfer(msg: TonSignMessage) -> int:
    if msg.jetton_amount is None and msg.jetton_amount_bytes is None:
        return 0
    # fmt: off
    elif msg.jetton_amount_bytes is not None and msg.jetton_master_address is not None:
        return int.from_bytes(msg.jetton_amount_bytes, "big")
    # fmt: on
    elif msg.jetton_amount is not None and msg.jetton_master_address is not None:
        return msg.jetton_amount
    else:
        raise wire.DataError("Invalid jetton transfer message.")


async def send_request_chunk(ctx: wire.Context, data_left: int) -> TonTxAck:
    req = TonSignedMessage()
    if data_left <= 1024:
        req.init_data_length = data_left
    else:
        req.init_data_length = 1024

    return await ctx.call(req, TonTxAck)
