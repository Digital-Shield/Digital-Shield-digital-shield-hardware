from trezor import utils

from . import DetailBase
from .helper import parser_path


class Aptos(DetailBase):
    @staticmethod
    def get_name() -> str:
        return "APTOS"
    @staticmethod
    def get_icon() -> str:
        return "A:/res/chain-apt.png"
    @staticmethod
    def get_path() -> str:
        return "m/44'/637'/0'/0'/0'"

    @classmethod
    async def get_address(cls) -> str:
        import_manager = utils.unimport()
        with import_manager:
            from trezor.wire import DUMMY_CONTEXT as ctx
            from apps.base import handle_Initialize
            from trezor.messages import Initialize, AptosGetAddress
            from apps.aptos.get_address import get_address

            # step 1: initialize
            init = Initialize(session_id=b"\x00")
            await handle_Initialize(ctx, init)

            # step 2: get address
            req = AptosGetAddress(address_n=parser_path(cls.get_path()))
            resp = await get_address(ctx, req)

            return resp.address
