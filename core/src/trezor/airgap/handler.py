from typing import TYPE_CHECKING
from trezor import log
from trezor.airgap.ur.ur import UR
from trezor.wire import errors

if TYPE_CHECKING:
    from trezor.airgap.bc_types.keypath import KeyPath, PathComponent
    from typing import (
        Any,
        Callable,
        Coroutine,
        List,
    )
    from trezor.wire import GenericContext

    HandlerTask = Coroutine[Any, Any, UR]
    Handler = Callable[["GenericContext", bytes], HandlerTask]

handlers: dict[str, Handler] = {}

def register_handler(name: str, handler: Handler) -> None:
    handlers[name] = handler

def find_handler(type: str) -> Handler:
    log.debug(__name__, f"finding handler: {type}")
    return handlers.get(type)


# === handlers ===
from trezor.airgap.bc_types.eth_sign_request import (
    EthSignRequest,
    ETH_TRANSACTION_DATA,
    ETH_TYPED_DATA,
    ETH_RAW_BYTES,
    ETH_TYPED_TRANSACTION,
)

def _keypath_to_address_n(keypath: KeyPath) -> List[int]:
    components = keypath.components
    if any(c.wildcard for c in components):
        raise errors.DataError("Wildcard is not supported")
    def convert(c: PathComponent) -> int:
        index, hardened = c.index, c.hardened
        return 0x80000000 + index if hardened else index

    return [convert(c) for c in components]

async def handle_eth_sign_request(ctx: 'GenericContext', cbor: bytes) -> 'UR':
    req = EthSignRequest.from_cbor(cbor)

    try:
        # initialize session
        from apps.base import handle_Initialize
        from trezor.messages import Initialize
        init = Initialize(session_id=b'\x00')
        await handle_Initialize(ctx, init)

        # get public key
        # verify keypath, keypath.source_fingerprint is matching
        from trezor.messages import EthereumGetPublicKey
        from apps.ethereum.get_public_key import get_public_key
        address_n = _keypath_to_address_n(req.derivation_path)
        # get master key fingerprint
        msg = EthereumGetPublicKey(address_n=address_n[:1])
        pubkey = await get_public_key(ctx, msg)
        log.debug(__name__, f"master key fingerprint in device: {pubkey.node.fingerprint}")
        log.debug(__name__, f"master key fingerprint in request: {req.derivation_path.source_fingerprint}")
        if pubkey.node.fingerprint != req.derivation_path.source_fingerprint:
            raise errors.DataError("Invalid sign-request. Keypath source fingerprint does not match")

        # verify address
        if req.address:
            from trezor.messages import EthereumGetAddress
            from apps.ethereum.get_address import get_address
            from apps.ethereum.helpers import bytes_from_address
            msg = EthereumGetAddress(address_n=address_n)
            resp = await get_address(ctx, msg)
            addres_bytes = bytes_from_address(resp.address)
            if addres_bytes != req.address:
                raise errors.DataError("Invalid sign-request. Address does not match")

        if req.data_type == ETH_TRANSACTION_DATA:
            # legacy transaction
            resp = await eth_sign_tx(ctx, req)
            signature = resp.signature_r + resp.signature_s + bytes([resp.signature_v])
        elif req.data_type == ETH_TYPED_DATA:
            # eip-712 message
            resp = await eth_sign_typed_data(ctx, req)
            signature = resp.signature
        elif req.data_type == ETH_RAW_BYTES:
            # raw bytes
            resp = await eth_sign_message(ctx, req)
            signature = resp.signature
        elif req.data_type == ETH_TYPED_TRANSACTION:
            # typed transaction
            resp = await eth_sign_tx_eip1559(ctx, req)
            signature = resp.signature_r + resp.signature_s + bytes([resp.signature_v])
        else:
            raise errors.DataError(f"Unknown data type: {req.data_type}")

        from trezor.airgap.bc_types.eth_signature import EthSignature
        sig =  EthSignature(
            signature=signature,
            request_id=req.request_id,
            origin="DigitShield"
        )
        return UR(sig.type(), sig.cbor())
    finally:
        from trezor.messages import EndSession
        from apps.base import handle_EndSession
        await handle_EndSession(ctx, EndSession())

# === eth sign request ===
async def eth_sign_tx(ctx: 'GenericContext', req: EthSignRequest):
    from trezor.messages import EthereumSignTx
    from trezor.crypto import rlp
    from apps.ethereum.sign_tx import sign_tx
    from apps.ethereum.helpers import address_from_bytes
    # legacy
    # rlp([nonce, gasPrice, gasLimit, to, value, data, v, r, s])
    data = req.sign_data
    items = rlp.decode(data)
    if len(items) != 6:
        raise errors.DataError("Invalid sign data")
    address_n = _keypath_to_address_n(req.derivation_path)
    chain_id = req.chain_id
    nonce = items[0]
    gas_price = items[1]
    gas_limit = items[2]
    to = items[3]
    to = address_from_bytes(to)
    value = items[4]
    data = items[5]
    # _ = items[6]
    # _ = items[7]
    # _ = items[8]

    msg = EthereumSignTx(
        address_n=address_n,
        chain_id=chain_id,
        gas_price=gas_price,
        gas_limit=gas_limit,
        nonce=nonce,
        to=to,
        value=value,
        data_initial_chunk=data,
        data_length=len(data),
    )

    return await sign_tx(ctx, msg)

async def eth_sign_typed_data(ctx: 'GenericContext', req: EthSignRequest):
    from trezor.messages import EthereumSignTypedData
    from apps.ethereum.sign_typed_data import sign_typed_data
    address_n = _keypath_to_address_n(req.derivation_path)
    primary_type = req.sign_data[0]
    data = req.sign_data[1:]

    msg = EthereumSignTypedData(
        address_n=address_n,
        primary_type=primary_type,
        data=data
    )

    return await sign_typed_data(ctx, msg)
    # eip-712
    pass
async def eth_sign_message(ctx: 'GenericContext', req: EthSignRequest):
    from trezor.messages import EthereumSignMessage
    from apps.ethereum.sign_message import sign_message
    address_n = _keypath_to_address_n(req.derivation_path)
    data = req.sign_data

    msg = EthereumSignMessage(
        address_n=address_n,
        data=data
    )
    return await sign_message(ctx, msg)
    # eip-191
    pass
async def eth_sign_tx_eip1559(ctx: 'GenericContext', req: EthSignRequest):
    from trezor.messages import EthereumSignTxEIP1559
    from trezor.crypto import rlp
    from apps.ethereum.sign_tx_eip1559 import sign_tx_eip1559
    from apps.ethereum.helpers import address_from_bytes
    # eip-2930
    # 0x01 || rlp([chainId, nonce, gasPrice, gasLimit, to, value, data, accessList, signatureYParity, signatureR, signatureS])

    # eip-1559
    #0x02 || rlp([chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list, signature_y_parity, signature_r, signature_s])
    data = req.sign_data
    if data[0] != 0x02:
        raise errors.DataError("Invalid sign data, unexpected data type")

    items = rlp.decode(data, 1)
    if len(items) != 9:
        raise errors.DataError("Invalid sign data")

    address_n = _keypath_to_address_n(req.derivation_path)
    chain_id = req.chain_id
    nonce = items[1]
    max_priority_fee_per_gas = items[2]
    max_fee_per_gas = items[3]
    gas_limit = items[4]
    to = items[5]
    to = address_from_bytes(to)
    value = items[6]
    data = items[7]
    access_list = items[8]
    # _ = items[9]
    # _ = items[10]
    # _ = items[11]

    msg = EthereumSignTxEIP1559(
        address_n=address_n,
        chain_id=chain_id,
        nonce=nonce,
        max_priority_fee=max_priority_fee_per_gas,
        max_gas_fee= max_fee_per_gas,
        gas_limit=gas_limit,
        data_length=len(data),
        data_initial_chunk=data,
        to=to,
        value=value,
        access_list=access_list,
    )
    return await sign_tx_eip1559(ctx, msg)

# only one handler at this moment
register_handler("eth-sign-request", handle_eth_sign_request)
