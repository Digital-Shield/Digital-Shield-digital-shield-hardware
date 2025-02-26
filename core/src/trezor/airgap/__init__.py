"""
# Airgap service

Airgap implements `wire.Interface` interface. We can trade Airgap as a virtual wire interface.

                               ▲
                               │
                               │
                               │
                        `setup` in wire
                               │
                               │
                               │
                               │
┌──────────────────────────────┼────────────────────────────────┐
│                                                               │
│                    `wire.Interface`                           │
│                                                               │
└───────────────────────────────────────────────────────────────┘
│                              │                                │
│           read               │             write              │
│                              │                                │
└──────────────────────────────┘────────────────────────────────┘
│                                                               │
│                                                               │
│                                                               │
│              Airgap Service                                   │
│                                                               │
│  1. Use `camera` as input, scan UR format QR code as `ur`     │
│                                                               │
│  2. Use `screen` as output, draw UR format QR code            │
│                                                               │
│  3. Implement `wire.Interface` as a virtual interface         │
│                                                               │
│  4. User can setup `airgap` service to `wire`                 │
│                                                               │
│                                                               │
│  The process in `airgap` service while scanned `ur`           │
│                                                               │
│  1. switch `ur` do                                            │
│     support?                                                  │
│     yes) convert to `PB` and report to wire                   │
│     no ) show error on screen                                 │
│                                                               │
│  The process in `airgap` servce when upper write data         │
│                                                               │
│  1. Encode data in `UR` or `MUR`, single QR or animation QR   │
│                                                               │
│  2. Draw encoded on screen                                    │
│                                                               │
└────────────▲───────────────────────────────────────┬──────────┘
             │                                       │
             │                                       │
  ┌──────────┼──────────┐                 ┌──────────▼────────┐
  │                     │                 │                   │
  │        Camera       │                 │      Screen       │
  │                     │                 │                   │
  └─────────────────────┘                 └───────────────────┘
  """

import gc
import binascii
from trezor import io, log, loop, utils

from . import event
from .ur.ur_decoder import URDecoder
from .ur.ur_encoder import UREncoder
from .ur.ur import UR

def setup() -> None:
    airgap = Airgap.instance()
    loop.schedule(handle_scanning(airgap))

class Airgap():
    _instance :'Airgap' = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Airgap()
        return cls._instance

    def __init__(self) -> None:
        self.camera = loop.wait(io.CAMERA | io.POLL_READ)
        self.reading = loop.chan()
        self.writing = loop.chan()
        self.event_hub = loop.chan()

        self.decoder = URDecoder()

    async def scan(self) -> bytes|str:
        return await self.camera

    # impl wire.Interface
    async def read(self) -> bytes:
        return await self.reading.take()

    async def write(self, data: bytes) -> int:
        return await self.writing.put(data)

    def reset(self) -> None:
        """
        User can reset the airgap , discard scanning state.
        e.g. when scanning failed, or scanned invalid QR code
        """
        self.decoder = URDecoder()


async def handle_scanning(airgap: Airgap) -> None:
    while True:
        data = await airgap.scan()
        if isinstance(data, bytes):
            data = data.decode()

        log.debug(__name__, f"scanned: {data}")
        accepted = airgap.decoder.receive_part(data)
        log.debug(__name__, f"accepted: {accepted}")

        if not accepted:
            continue

        if airgap.decoder.is_complete():
            airgap.event_hub.publish(event.Done())
            log.debug(__name__, "airgap receive complete")
            result: UR = airgap.decoder.result
            log.debug(__name__, f"result type: {result.type}")
            log.debug(__name__, f"result cbor: {binascii.hexlify(result.cbor)}")
            await handle_ur_message(result)
            log.debug(__name__, "airgap process done")
            continue

        expected = airgap.decoder.expected_part_count()
        processed = airgap.decoder.processed_parts_count()
        log.debug(__name__, f"received: {processed}/{expected}")
        # publish event
        airgap.event_hub.publish(event.MultiUR(expected, processed))


async def handle_ur_message(msg: UR):
    type = msg.type
    data = msg.cbor
    unimport_manager = utils.unimport()
    with unimport_manager:
        from trezor import wire
        from trezor.wire import DUMMY_CONTEXT
        from .handler import find_handler
        from trezor.ui.layouts import show_popup, show_airgap_signature
        from trezor.ui import i18n
        handler = find_handler(type)
        if not handler:
            log.error(__name__, f"no handler for type: {type}")
            await show_popup(i18n.Text.unknown_tx_type)
            return
        try:
            ur = await handler(DUMMY_CONTEXT, data)
            # the result is `eth-signature`, is not too long, no need multi part
            qrcode = UREncoder.encode(ur)
            # make upper for compatibility
            qrcode = qrcode.upper()
            log.debug(__name__, f"qrcode: {qrcode}")
            await show_airgap_signature(qrcode)
        except wire.ActionCancelled:
            # user canceled the action, do nothing
            Airgap.instance().event_hub.publish(3)
            return
        except wire.Error as e:
            log.error(__name__, f"error: {e.message}")
            await show_popup(e.message)
            Airgap.instance().event_hub.publish(3)
        except Exception as e:
            log.error(__name__, f"error: {e}")
            await show_popup(i18n.Text.internal_error)
            Airgap.instance().event_hub.publish(3)
        finally:
            gc.collect()

