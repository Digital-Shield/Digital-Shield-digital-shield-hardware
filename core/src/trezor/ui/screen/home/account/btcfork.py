from trezor import utils

from . import DetailBase
from .helper import parser_path
from trezor.enums import InputScriptType

BTC_COIN_NAME = "Bitcoin"
LTC_COIN_NAME = "Litecoin"
DOGE_COIN_NAME = "Dogecoin"

def BTCFork(coin_name:str):
    name_map = {
        BTC_COIN_NAME: "BTC",
        LTC_COIN_NAME: "LTC",
        DOGE_COIN_NAME: "DOGE",
    }

    icon_map = {
        BTC_COIN_NAME: "A:/res/btc-btc.png",
        LTC_COIN_NAME: "A:/res/btc-ltc.png",
        DOGE_COIN_NAME: "A:/res/btc-doge.png",
    }

    path_map = {
        BTC_COIN_NAME: "m/49'/0'/0'/0/0",
        LTC_COIN_NAME: "m/49'/2'/0'/0/0",
        DOGE_COIN_NAME: "m/44'/3'/0'/0/0",
    }

    script_map = {
        BTC_COIN_NAME: InputScriptType.SPENDP2SHWITNESS,
        LTC_COIN_NAME: InputScriptType.SPENDP2SHWITNESS,
        DOGE_COIN_NAME: InputScriptType.SPENDADDRESS,
    }


    class _BTCFork(DetailBase):
        @staticmethod
        def get_name() -> str:
            return name_map[coin_name]
        @staticmethod
        def get_icon() -> str:
            return icon_map[coin_name]
        @staticmethod
        def get_path() -> str:
            return path_map[coin_name]

        @staticmethod
        async def get_address() -> str:
            import_manager = utils.unimport()
            with import_manager:
                from trezor.wire import DUMMY_CONTEXT as ctx
                from apps.base import handle_Initialize
                from trezor.messages import Initialize, GetAddress
                from apps.bitcoin.get_address import get_address

                # step 1: initialize
                init = Initialize(session_id=b"\x00")
                await handle_Initialize(ctx, init)

                # step 2: get address
                req = GetAddress(address_n=parser_path(_BTCFork.get_path()),coin_name = coin_name,script_type = script_map[coin_name])
                resp = await get_address(ctx, req)

                return resp.address

    return _BTCFork
