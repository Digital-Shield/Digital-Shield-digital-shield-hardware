import lvgl as lv

from . import *

from trezor.ui import i18n, Style, colors, font
from trezor.ui import Done
from trezor.ui.screen import Modal
from trezor.ui.theme import Styles
from trezor.ui.component.container import HStack, VStack
from trezor.ui.screen.confirm import Confirm
# from trezor.ui.component.checkbox import Checkbox  # 假设存在 Checkbox 组件

from trezor.ui.types import *

if TYPE_CHECKING:

    class SecurityMessage(Protocol):
        header: str | None = None
        tips: List[str] | None = None


class XSecurity(Confirm):
    def __init__(self, title, message: SecurityMessage, show_type: str):
        super().__init__()
        # self.set_title(title)
        #设置标题字体
        # self.set_style_text_font(font.Bold.SCS38, 0)
        #靠左对齐
        # self.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)

        if show_type == "pinSecurity":
            self.btn_right.set_text(i18n.Title.create_wallet)
        else:
            self.btn_right.set_text(i18n.Button.continue_)
        self.btn_right.set_style_width(440, lv.PART.MAIN)
        self.btn_right.set_style_height(89, lv.PART.MAIN)
        self.btn_right.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)  # 设置背景颜色
        self.btn_right.add_event_cb(lambda _: self.close(Done()), lv.EVENT.CLICKED, None)
        # 初始化一个列表来保存复选框状态
        self.checkbox_states: List[lv.checkbox] = []

        self.create_content(HStack)
        self.content: HStack
        # #设置高度800
        # self.content.set_height(800)
        self.set_style_pad_left(16, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)

        self.text1 = lv.label(self.content)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(title)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)
        self.text1.set_style_text_font(font.Bold.SCS38, lv.PART.MAIN)
        self.text1.set_style_pad_all(16, 0)
        self.text1.align(lv.ALIGN.TOP_LEFT, 40, -20)

        header = lv.label(self.content)
        header.set_long_mode(lv.label.LONG.WRAP)
        header.add_style(
            Style()
           .width(lv.pct(100))
           .text_color(colors.DS.WHITE)
           .radius(16)
           .pad_all(16)
           .text_line_space(10)
           .text_font(font.Bold.SCS26),
            lv.PART.MAIN,
        )
        header.set_text(message.header)
        # 获取当前语言，判断阿拉伯语
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            header.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置标题文本方向为从右到左
            header.set_style_text_font(lv.font_scs_reg_26, 0)  # 使用支持阿拉伯语的字体

        # header.set_text(message.header)
        # danger = self.add(lv.img)
        # danger.set_src("A:/res/danger.png")

        self.checks: List[lv.checkbox] = []

        style = (
            Style()
            # .text_color(colors.DS.DANGER)
            # .text_font(font.Bold.SCS30)
            #圆角
            .radius(32)
            .pad_left(16)
            .width(lv.pct(100))
        )

        for idx, msg in enumerate(message.tips):
            # checkbox = lv.obj(self.content)
            # checkbox.set_size(36, 80)
            checkbox = self.add(lv.checkbox)
            checkbox.set_ext_click_area(20)
            checkbox.set_text("")  # 清空默认文本
            checkbox.add_style(style, lv.PART.MAIN)
            # checkbox.set_style_text_font(font.Regular.SCS26, 0)  # 设置文本字体
            #啊设置宽度40,，高度40
            # checkbox.set_style_width(40, 0)
            # checkbox.set_style_height(40,0)
            #设置复选框颜色为蓝色
            # checkbox.set_style_bg_color(colors.DS.BLUE, 0)
            checkbox.set_style_radius(lv.RADIUS.CIRCLE, 0)  # 设置圆角半径为checkbox的一半形（等价于 size/2）
            #选中后的框背景颜色为蓝色
            style_checked = Style().bg_color(lv.color_hex(0x0062CE))
            checkbox.add_style(style_checked, lv.PART.INDICATOR | lv.STATE.CHECKED)
            #选中后的颜色为白色
            checkbox.add_style(Style().text_color(lv.color_hex(0xFFFFFF)), lv.PART.INDICATOR | lv.STATE.CHECKED)
            checkbox.set_style_bg_color(lv.color_hex(0x000000), lv.STATE.DEFAULT) # 设置背景颜色为黑色
            
            checkbox.set_style_border_color(lv.color_hex(0x000000), lv.STATE.DEFAULT)
            #设置内边框
            # 设置复选框完全透明
            # checkbox.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)


            # Create separate images for each checkbox
            # unchecked_img = lv.img(checkbox)
            # unchecked_img.set_src("A:/res/unchecked_image.png")  # Replace with actual path
            #  #啊设置宽度40,，高度40
            # unchecked_img.set_style_width(50, 0)
            # unchecked_img.set_style_height(50,0)
            # unchecked_img.align_to(checkbox, lv.ALIGN.TOP_LEFT, -3, -5)
            checkbox.add_event_cb(self.on_value_changed, lv.EVENT.VALUE_CHANGED, None)

            checkbox.set_width(450)

            # 创建label并将其作为checkbox的子项
            label = lv.label(checkbox)
            label.set_text(msg)  # 使用原始文本
            label.set_width(360)  # 必须设置宽度
            label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)  # 滚动条自适应
            label.set_style_text_color(colors.DS.WHITE, 0)  # 设置文本颜色为白
            label.set_style_text_font(font.Regular.SCS26, 0)  # 设置文本字体
            #行间距10
            label.set_style_text_line_space(10, 0)  # 设置行间距为10px
            # label.add_style(style_checked, lv.STATE.CHECKED)  # 点击时变为白色
            label.align(lv.ALIGN.OUT_RIGHT_MID, 40, 0)  # 调整label的位置
            
            # 同步复选框状态（修复错乱问题）
            def update_label_text(event):
                # Ensure the label text is updated based on the checkbox state
                chk = event.get_target()
                lbl = chk.get_child(0)  # Assuming the label is the first child of the checkbox
                # print("lbl:", lbl)
                if chk.has_state(lv.STATE.CHECKED):
                    #设置图片路径
                    print("lbl:选中了", lbl)
                    # lbl.set_src("A:/res/checked_image.png")
                else:
                    #设置图片路径
                    print("lbl:取消了", lbl)
                    # lbl.set_src("A:/res/unchecked_image.png")
                    # checked_img.set_src("A:/res/checked_image.png")

            checkbox.add_event_cb(update_label_text, lv.EVENT.VALUE_CHANGED, None)

            self.checks.append(checkbox)

        # self.holder.set_size(200, 200)
        # self.holder.set_text(i18n.Button.hold_to_wipe)
        # self.holder.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        # self.holder.disabled = True

        # disable `ok` button, user need hold sometime on to enable `ok` button
        self.btn_confirm.add_state(lv.STATE.DISABLED)
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_style_pad_left(16, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content : HStack
        self.content.items_center()
        self.content.reverse()
        self.content.set_height(260)  # 设置高度为60px
        # self.content.set_style_pad_bottom(32, lv.PART.MAIN)

       

    def on_value_changed(self, event: lv.event_t) -> None:
        # update holder button state
        enabled = all(check.has_state(lv.STATE.CHECKED) for check in self.checks)
        if enabled:
            self.btn_confirm.clear_state(lv.STATE.DISABLED)
        else:
            self.btn_confirm.add_state(lv.STATE.DISABLED)

class MyObject:
    def __init__(self, data):
        self.data = data

class PinSecurity(XSecurity):

    def __init__(self):
        title = i18n.Title.pin_security
        message = i18n.PinSecurity
        super().__init__(title=title, message=message, show_type="pinSecurity")


class MnemonicSecurity(XSecurity):
    def __init__(self):
        title = i18n.Title.prepare_backup
        message = i18n.MnemonicSecurity
        super().__init__(title=title, message=message, show_type= "mnemonicSecurity")
