
from trezor import utils

from . import DetailBase
from .helper import parser_path


class Ton(DetailBase):
    @staticmethod
    def get_name() -> str:
        return "Ton"
    @staticmethod
    def get_icon() -> str:
        return "A:/res/chain-ton.png"
    @staticmethod
    def get_path() -> str:
        return "m/44'/607'/0'/0'/0'"

    @classmethod
    async def get_address(cls) -> str:
        import_manager = utils.unimport()
        with import_manager:
            from trezor.wire import DUMMY_CONTEXT as ctx
            from apps.base import handle_Initialize
            from trezor.messages import Initialize, TonGetAddress
            from apps.ton.get_address import get_address

            # step 1: initialize
            init = Initialize(session_id=b"\x00")
            await handle_Initialize(ctx, init)
            
            # print("address_n--"+str(parser_path(cls.get_path())))
            # step 2: get address
            req = TonGetAddress(address_n=parser_path(cls.get_path()),wallet_version=3, workchain=0, is_bounceable=False, 
                                is_testnet_only=False, wallet_id=698983191, show_display=True)
            
            resp = await get_address(ctx, req)

            return resp.address
