import lvgl as lv

from trezor.ui import Style
from trezor.ui.types import *

item_style = (
    Style()
    .width(lv.pct(100))
    .bg_color(lv.color_hex(0x111126))
    .bg_opa(lv.OPA._90)
    .border_width(0)
    .height(106)
    .radius(16)
    .bg_opa()
    )
