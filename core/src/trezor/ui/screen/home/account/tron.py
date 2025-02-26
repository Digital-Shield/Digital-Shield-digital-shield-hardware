from trezor import utils

from . import DetailBase
from .helper import parser_path


class Tron(DetailBase):
    @staticmethod
    def get_name() -> str:
        return "TRON"
    @staticmethod
    def get_icon() -> str:
        return "A:/res/chain-tron.png"
    @staticmethod
    def get_path() -> str:
        return "m/44'/195'/0'/0/0"

    @staticmethod
    async def get_address() -> str:
        import_manager = utils.unimport()
        with import_manager:
            from trezor.wire import DUMMY_CONTEXT as ctx
            from apps.base import handle_Initialize
            from trezor.messages import Initialize, TronGetAddress
            from apps.tron.get_address import get_address

            # step 1: initialize
            init = Initialize(session_id=b"\x00")
            await handle_Initialize(ctx, init)

            # step 2: get address
            req = TronGetAddress(address_n=parser_path(Tron.get_path()))
            resp = await get_address(ctx, req)

            return resp.address
