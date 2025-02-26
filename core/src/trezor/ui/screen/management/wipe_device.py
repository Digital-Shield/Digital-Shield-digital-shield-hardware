import lvgl as lv

from typing import TYPE_CHECKING

from trezor.ui import i18n, Style, colors, font
from trezor.ui.component import HStack
from trezor.ui.screen.confirm import HolderConfirm

if TYPE_CHECKING:
    from typing import List

    pass

class WipeDeviceTips(HolderConfirm):
    def __init__(self):
        super().__init__()
        self.create_content(HStack)
        self.content: HStack
        self.set_style_pad_left(16, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)

        danger = self.add(lv.img)
        danger.set_src("A:/res/danger.png")

        self.checks: List[lv.checkbox] = []

        style = (
            Style()
            .text_color(colors.DS.DANGER)
            .text_font(font.Bold.SCS30)
            .width(lv.pct(100))
        )
        style_checked = Style().text_color(colors.DS.BLACK)
        for check in i18n.Text.wipe_device_check:
            checkbox = self.add(lv.checkbox)
            checkbox.set_ext_click_area(6)
            checkbox.set_text(check)
            checkbox.add_style(style, lv.PART.MAIN)
            checkbox.add_style(style_checked, lv.PART.MAIN | lv.STATE.CHECKED)
            checkbox.add_event_cb(self.on_value_changed, lv.EVENT.VALUE_CHANGED, None)
            self.checks.append(checkbox)

        self.holder.set_size(200, 200)
        self.holder.set_text(i18n.Button.hold_to_wipe)
        self.holder.disabled = True
        self.btn_confirm.color(colors.DS.DANGER)

    def on_value_changed(self, event: lv.event_t) -> None:
        # update holder button state
        enabled = all(check.has_state(lv.STATE.CHECKED) for check in self.checks)
        if enabled:
            self.holder.disabled = False
        else:
            self.holder.disabled = True
