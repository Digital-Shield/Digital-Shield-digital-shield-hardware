
from trezor import utils

from . import DetailBase
from .helper import parser_path


class Polkadot(DetailBase):
    @staticmethod
    def get_name() -> str:
        return "Polkadot"
    @staticmethod
    def get_icon() -> str:
        return "A:/res/chain-dot.png"
    @staticmethod
    def get_path() -> str:
        return "m/44'/354'/0'/0'/0'"

    @staticmethod
    async def get_address() -> str:
        import_manager = utils.unimport()
        with import_manager:
            from trezor.wire import DUMMY_CONTEXT as ctx
            from apps.base import handle_Initialize
            from trezor.messages import Initialize, PolkadotGetAddress
            from apps.polkadot.get_address import get_address

            # step 1: initialize
            init = Initialize(session_id=b"\x00")
            await handle_Initialize(ctx, init)

            # step 2: get address
            req = PolkadotGetAddress(address_n=parser_path(Polkadot.get_path()), prefix=0, network='polkadot')
            resp = await get_address(ctx, req)

            return resp.address
