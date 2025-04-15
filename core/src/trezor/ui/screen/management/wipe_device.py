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
        style_checked = Style().text_color(colors.DS.WHITE)
        for check in i18n.Text.wipe_device_check:
            checkbox = self.add(lv.checkbox)
            checkbox.set_ext_click_area(6)
            checkbox.set_text("")  # 清空默认文本
            checkbox.add_style(style, lv.PART.MAIN)
            checkbox.add_style(style_checked, lv.PART.MAIN | lv.STATE.CHECKED)
            checkbox.add_event_cb(self.on_value_changed, lv.EVENT.VALUE_CHANGED, None)

            checkbox.set_width(450)

            # 创建label并将其作为checkbox的子项
            label = lv.label(checkbox)
            label.set_text(check)  # 使用原始文本
            cur_language = i18n.using.code if i18n.using is not None else None
            if cur_language == "al":
                print("current language is al")
                label.set_style_base_dir(lv.BASE_DIR.RTL, lv.PART.MAIN)  # 设置文本显示方向从右到左
            label.set_width(360)  # 必须设置宽度
            label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
            label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)  # 滚动条自适应
            label.set_style_text_color(colors.DS.DANGER, 0)  # 设置文本颜色为红色
            label.add_style(style_checked, lv.STATE.CHECKED)  # 点击时变为白色
            label.align(lv.ALIGN.OUT_RIGHT_MID, 40, 0)  # 调整label的位置
            
            # 同步复选框状态（修复错乱问题）
            def update_label_text(event):
                # Ensure the label text is updated based on the checkbox state
                chk = event.get_target()
                lbl = chk.get_child(0)  # Assuming the label is the first child of the checkbox
                if chk.has_state(lv.STATE.CHECKED):
                    lbl.set_style_text_color(lv.color_hex(0xFFFFFF), 0)  # 设置文本颜色为白色
                if not chk.has_state(lv.STATE.CHECKED):
                    lbl.set_style_text_color(colors.DS.DANGER, 0)  # 设置文本颜色为红色

            checkbox.add_event_cb(update_label_text, lv.EVENT.VALUE_CHANGED, None)

            self.checks.append(checkbox)

        self.holder.set_size(200, 200)
        self.holder.set_text(i18n.Button.hold_to_wipe)
        self.holder.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        self.holder.disabled = True
        self.btn_confirm.color(colors.DS.DANGER)

    def on_value_changed(self, event: lv.event_t) -> None:
        # update holder button state
        enabled = all(check.has_state(lv.STATE.CHECKED) for check in self.checks)
        if enabled:
            self.holder.disabled = False
        else:
            self.holder.disabled = True
            self.holder.reset()
            self.btn_confirm.add_state(lv.STATE.DISABLED)
