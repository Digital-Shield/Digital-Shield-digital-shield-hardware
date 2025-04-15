import lvgl as lv

from trezor.ui.screen import Modal
from trezor import log, workflow

_RECEIVE_TIMEOUT = 60 * 1000

class LoadingResource(Modal):
    def __init__(self, res: str, total: int):
        super().__init__()

        log.debug(__name__, f"total: {total}")
        label = self.add(lv.label)
        label.center()
        label.set_text(res)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.total = total
        self.size = 0
        self.bar = self.add(lv.bar)
        self.bar.set_size(lv.pct(60), 12)
        self.bar.set_value(0, lv.ANIM.OFF)
        self.bar.set_style_bg_color(lv.color_hex(0x31343B), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bar.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bar.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.bar.set_style_bg_opa(lv.OPA.COVER, lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.bar.align(lv.ALIGN.BOTTOM_MID, 0, -32)

    def update(self, size: int):
        workflow.idle_timer.set(_RECEIVE_TIMEOUT, self.cancel_transmit)

        self.size += size
        log.debug(__name__, f"{self.size}/{self.total}")
        value = (self.size * 100) // self.total
        if value > 100:
            value = 100
        log.debug(__name__, f"uploading: {value}")
        self.bar.set_value(value, lv.ANIM.OFF)

    def close(self, value):
        workflow.idle_timer.remove(self.cancel_transmit)
        super().close(value)

    def cancel_transmit(self):
        # not get message while wait a long time
        # may bee the app die, or bluetooth disconnect?
        from trezor import wire
        wire.signal_ack()
