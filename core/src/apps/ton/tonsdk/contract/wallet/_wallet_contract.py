from typing import TYPE_CHECKING, List, Union


from ...boc import Cell
from ...utils import Address#,sign_message
from .. import Contract
from trezor.crypto.curve import ed25519
# import base64
if TYPE_CHECKING:
    from enum import IntEnum
else:
    IntEnum = int


class SendModeEnum(IntEnum):
    carry_all_remaining_balance = 128
    carry_all_remaining_incoming_value = 64
    destroy_account_if_zero = 32
    ignore_errors = 2
    pay_gas_separately = 1

    def __str__(self) -> str:
        return super().__str__()


class WalletContract(Contract):
    def __init__(self, **kwargs):
        if "public_key" not in kwargs:
            raise Exception("WalletContract required publicKey in options")
        super().__init__(**kwargs)

    def create_data_cell(self):
        cell = Cell()
        cell.bits.write_uint(0, 32)
        cell.bits.write_bytes(self.options["public_key"])
        return cell

    def create_signing_message(self, _expiration_time, seqno=None):
        seqno = seqno or 0
        cell = Cell()
        cell.bits.write_uint(seqno, 32)
        return cell

    def create_transaction_digest(
        self,
        to_addr: str,
        amount: int,
        seqno: int,
        expire_at: int,
        payload: Union[Cell, str, bytes, None] = None,
        is_raw_data: bool = False,
        send_mode=SendModeEnum.ignore_errors | SendModeEnum.pay_gas_separately,
        state_init: bytes = None,
        ext_to: List[str] = None,
        ext_amount: List[int] = None,
        ext_payload: List[Union[Cell, str, bytes, None]] = None,
        private_key: bytes = None,
    ):
        payload_cell = Cell()
        if payload:
            if isinstance(payload, str):
                # check payload type
                # if is_raw_data:
                if payload.startswith("b5ee9c72"):
                    payload_cell = Cell.one_from_boc(payload)
                else:
                    payload_cell.bits.write_uint(0, 32)
                    payload_cell.bits.write_string(payload)
            elif isinstance(payload, Cell):
                payload_cell = payload
            else:
                payload_cell.bits.write_bytes(payload)

        order_header = Contract.create_internal_message_header(
            dest=Address(to_addr), grams=amount
        )

        state_init_cell = None
        if state_init:
            print("state_start: ", Cell.REACH_BOC_MAGIC_PREFIX)
            if state_init.startswith(Cell.REACH_BOC_MAGIC_PREFIX):
                state_init_cell = Cell.one_from_boc(state_init)
            else:
                # state_init_cell = state_init
                raise ValueError("Invalid state init")
        order = Contract.create_common_msg_info(
            order_header, state_init_cell, payload_cell
        )
        signing_message = self.create_signing_message(expire_at, seqno)
        signing_message.bits.write_uint8(send_mode)
        signing_message.refs.append(order)

        query = self.create_external_message(signing_message, seqno, private_key)
        boc = query["message"].to_boc(False)
        # boc = signing_message.to_boc(False)#bytes()#)base64.b64encode().decode('utf-8')
        return signing_message.bytes_hash(), boc
    def create_external_message(self, signing_message, seqno, private_key, dummy_signature=False):
        print("private_key: ", private_key)
        sign_messages = ed25519.sign(private_key, signing_message.bytes_hash())
        # sign_messages = sign_message(bytes(signing_message.bytes_hash()), self.options['private_key'])
        signature = bytes(64) if dummy_signature else sign_messages #
        # print("signing_message:", sign_messages)
        print("sign_messages.signature:", sign_messages)
        body = Cell()
        body.bits.write_bytes(signature)
        body.write_cell(signing_message)

        state_init = code = data = None

        if seqno == 0:
            deploy = self.create_state_init()
            state_init = deploy["state_init"]
            code = deploy["code"]
            data = deploy["data"]

        self_address = self.address
        header = Contract.create_external_message_header(self_address)
        result_message = Contract.create_common_msg_info(
            header, state_init, body)

        return {
            "address": self_address,
            "message": result_message,
            "body": body,
            "signature": signature,
            "signing_message": signing_message,
            "state_init": state_init,
            "code": code,
            "data": data,
        }

