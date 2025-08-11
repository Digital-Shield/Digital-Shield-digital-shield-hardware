from trezor import utils
from .helper import parser_path

# a `CoinProtocol` class
class Solana:
    def get_name(self) -> str:
        return "Solana"
    def get_icon(self) -> str:
        return "A:/res/chain-sol.png"
    def get_path(self) -> str:
        return "m/44'/501'/0'/0'"

    async def get_address(self) -> str:
        import_manager = utils.unimport()
        with import_manager:
            from trezor.wire import DUMMY_CONTEXT as ctx
            from apps.base import handle_Initialize
            from trezor.messages import Initialize, SolanaGetAddress
            from apps.solana.get_address import get_address

            # step 1: initialize
            init = Initialize(session_id=b"\x00")
            await handle_Initialize(ctx, init)

            # step 2: get address
            req = SolanaGetAddress(address_n=parser_path(self.get_path()))
            resp = await get_address(ctx, req)

            return resp.address
