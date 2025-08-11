import lvgl as lv

from typing import TYPE_CHECKING

from trezor.ui import i18n, Style, colors, font
from trezor.ui.component import HStack
from trezor.ui.screen.confirm import Confirm

if TYPE_CHECKING:
    from typing import List

    pass

class WipeDeviceTips(Confirm):
    def __init__(self):
        super().__init__()
        self.create_content(HStack)
        self.content: HStack
        self.content.set_scroll_dir(lv.DIR.NONE)      # 禁止滚动
        #设置宽高
        self.set_size(436, 700)
        self.set_style_pad_left(40, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)
        self.btn_left.set_style_width(214, lv.PART.MAIN)
        self.btn_left.set_style_height(89, lv.PART.MAIN)
        self.btn_left.set_style_bg_color(lv.color_hex(0x141419), lv.PART.MAIN)  # 设置背景颜色
        # danger = self.add(lv.img)
        # danger.set_src("A:/res/danger.png")
         # 容器（重新设计布局）
        self.a_container = lv.obj(self.content)
        self.a_container.set_size(436, 210)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 10)
        self.a_container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)  # 隐藏滚动条
        self.text1 = lv.label(self.a_container)
        self.text1.set_long_mode(lv.label.LONG.WRAP)
        self.text1.set_width(lv.pct(90))
        self.text1.set_height(lv.SIZE.CONTENT)
        self.text1.set_text(i18n.Title.wipe_device)
        self.text1.set_style_pad_top(20, 0)
        #40
        self.text1.set_style_text_font(font.Bold.SCS38, 0)
        self.text1.set_style_text_color(colors.DS.WHITE, 0)

        self.text2 = lv.label(self.a_container)
        self.text2.set_long_mode(lv.label.LONG.WRAP)
        self.text2.set_width(lv.pct(90))
        self.text2.set_height(lv.SIZE.CONTENT)
        self.text2.set_text(i18n.Title.wipe_notice)
        #设置行间距10
        self.text2.set_style_text_line_space(10, 0)
        self.text2.set_style_text_font(font.Bold.SCS30, lv.PART.MAIN)
        self.text2.set_style_text_color(colors.DS.WHITE, 0)
        self.text2.align_to(self.text1,lv.TEXT_ALIGN.LEFT, 0, 60)

        self.checks: List[lv.checkbox] = []

        style = (
            Style()
            .text_color(colors.DS.WHITE)
            .text_font(font.Regular.SCS30)
            .pad_top(0)
            .pad_left(16)
            .width(lv.pct(100))
        )
        
        for check in i18n.Text.wipe_device_check:
            checkbox = self.add(lv.checkbox)
            checkbox.set_ext_click_area(6)
            checkbox.set_text("")  # 清空默认文本
            checkbox.add_style(style, lv.PART.MAIN)
             #选中后的框背景颜色为蓝色
            style_checked = Style().bg_color(lv.color_hex(0x0062CE))
            checkbox.add_style(style_checked, lv.PART.INDICATOR | lv.STATE.CHECKED)
            #选中后的颜色为白色
            checkbox.add_style(Style().text_color(lv.color_hex(0xFFFFFF)), lv.PART.INDICATOR | lv.STATE.CHECKED)

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
            label.set_long_mode(lv.label.LONG.WRAP)  # 使用换行模式
            label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)  # 滚动条自适应
            label.set_style_text_font(font.Regular.SCS26, lv.PART.MAIN)
            label.add_style(style_checked, lv.STATE.CHECKED)  # 点击时变为白色
            label.align(lv.ALIGN.OUT_RIGHT_MID, 40, 0)  # 调整label的位置
            #行间距5
            label.set_style_text_line_space(5, 0)
            
            # 同步复选框状态（修复错乱问题）
            def update_label_text(event):
                # Ensure the label text is updated based on the checkbox state
                chk = event.get_target()
                lbl = chk.get_child(0)  # Assuming the label is the first child of the checkbox
                if chk.has_state(lv.STATE.CHECKED):
                    #设置图片路径
                    print("lbl:选中了", lbl)
                    # lbl.set_src("A:/res/checked_image.png")
                    #设置图片路径
                    print("lbl:取消了", lbl)
                    # lbl.set_src("A:/res/unchecked_image.png")
                    lbl.set_style_text_color(lv.color_hex(0xFFFFFF), 0)  # 设置文本颜色为白色
                # if not chk.has_state(lv.STATE.CHECKED):
                    # lbl.set_style_text_color(colors.DS.DANGER, 0)  # 设置文本颜色为红色

            checkbox.add_event_cb(update_label_text, lv.EVENT.VALUE_CHANGED, None)

            self.checks.append(checkbox)
            # 禁用复选框的横向滚动
            checkbox.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
            # checkbox.set_flex_flow(lv.FLEX_FLOW_ROW)  # 保证内容横向排列但不滚动
            checkbox.set_scroll_dir(lv.DIR.NONE)      # 禁止滚动

        # self.holder.set_size(200, 200)
        # self.holder.set_text(i18n.Button.hold_to_wipe)
        # self.holder.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        # self.holder.disabled = True

        # disable `ok` button, user need hold sometime on to enable `ok` button
        self.btn_confirm.add_state(lv.STATE.DISABLED)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_style_pad_left(16, lv.PART.MAIN)
        self.set_style_pad_right(16, lv.PART.MAIN)
        self.create_content(HStack)
        self.content : HStack
        self.content.items_center()
        self.content.reverse()
        self.content.set_height(90)  # 设置高度为60px
        # self.content.set_style_pad_bottom(32, lv.PART.MAIN)

        # 替换为滑动滑块确认
        self.slider = self.add(lv.slider)
        self.slider.set_width(260)
        self.slider.set_height(66)
        self.slider.set_range(0, 280)
        self.slider.set_value(0, lv.ANIM.OFF)
       
        self.slider.set_pos(100, 0)  # 距离左边100px，距离上方150px（可根据实际UI调整）
        self.slider.set_style_border_width(0, lv.PART.MAIN)
        # 设置滑动条背景为灰色
        self.slider.add_style(Style().bg_color(colors.DS.GRAY).radius(60), lv.PART.MAIN)
        # 设置滑块为白色
        self.slider.add_style(Style().bg_color(colors.DS.WHITE).radius(60), lv.PART.KNOB)
        self.slider.add_style(Style().bg_img_src("A:/res/wipe_button.png"), lv.PART.KNOB)
        #滑过的轨道的颜色设置蓝色
        self.slider.add_style(Style().bg_color(lv.color_hex(0x0062CE)), lv.PART.INDICATOR)
        self.slider.add_event_cb(self.on_slider_changed, lv.EVENT.VALUE_CHANGED, None)

        # 新增：松开时如果没滑到头就回弹
        def on_slider_released(event):
            slider = event.get_target()
            value = slider.get_value()
            def update_confirm(timer):
                timer._del()
                # 滑到头，触发确认按钮的回调
                lv.event_send(self.btn_confirm, lv.EVENT.CLICKED, None)
            if value >= 260:
                if value >= 200:
                    #改变slider背景图片
                    print("改变slider背景图片")
                    self.slider.set_style_bg_img_src("A:/res/wipe_button_ok.png", lv.PART.KNOB)
                    #暂停1秒
                self._timer = lv.timer_create(update_confirm, 500, None)
            else:
                slider.set_value(0, lv.ANIM.ON)
                self.slider_label.set_style_text_opa(255, lv.PART.MAIN)
    
        self.slider.add_event_cb(on_slider_released, lv.EVENT.RELEASED, None)

        # 添加提示文本
        self.slider_label = lv.label(self.slider)
        self.slider_label.set_width(260)
        self.slider_label.set_text(i18n.Button.hold_to_wipe)
         #居中显示
        self.slider_label.set_style_pad_left(60, lv.PART.MAIN)
        #超出滑块轨道则向左滚动显示
        self.slider_label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)  # 启用循环滚动模式
        self.slider_label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)  # 滚动条自适应
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            self.slider_label.set_style_base_dir(lv.BASE_DIR.RTL, 0)  # 设置显示方向为向右
        else:
            self.slider_label.set_style_base_dir(lv.BASE_DIR.LTR, 0)  # 设置滚动方向为向左

        self.slider_label.add_style(
            Style().bg_color(colors.DS.GRAY).radius(60).text_color(lv.color_hex(0xFFFFFF)),
            lv.PART.MAIN
        )
        self.slider_label.add_style(Style().text_opa(255), lv.PART.MAIN)
        def on_slider_value_changed(event):
            slider = event.get_target()
            value = slider.get_value()
            opa = max(0, 255 - round(value / 230) * 255)  # 计算不透明度，使文本在滑动块向右滑动时淡出
            self.slider_label.set_style_text_opa(opa, lv.PART.MAIN)

        self.slider.add_event_cb(on_slider_value_changed, lv.EVENT.VALUE_CHANGED, None)
        # 滑块弹回后文字淡入
        def on_slider_anim_end(event):
            slider = event.get_target()
            if slider.get_value() == 0:
                self.slider_label.set_style_text_opa(255, lv.PART.MAIN)

        self.slider.add_event_cb(on_slider_anim_end, lv.EVENT.VALUE_CHANGED, None)
        # #上边距-50
        # self.slider.set_style_pad_top(-50, lv.PART.MAIN)
        self.slider_label.center()
        
        # 默认隐藏滑块
        self.slider.add_flag(lv.obj.FLAG.HIDDEN)
        self.slider.add_state(lv.STATE.DISABLED)

        # self.create_content(lv.obj)
        # self.content.set_flex_grow(1)

        # self.btn_confirm.add_state(lv.STATE.DISABLED)
        # self.btn_confirm.color(colors.DS.DANGER)

    def on_slider_changed(self, event):
            slider = event.get_target()
            value = slider.get_value()
            if value >= 100:
                self.btn_confirm.clear_state(lv.STATE.DISABLED)
            else:
                self.btn_confirm.add_state(lv.STATE.DISABLED)

    def on_value_changed(self, event: lv.event_t) -> None:
        # update holder button state
        enabled = all(check.has_state(lv.STATE.CHECKED) for check in self.checks)
        if enabled:
            self.slider.clear_flag(lv.obj.FLAG.HIDDEN)
            self.slider.clear_state(lv.STATE.DISABLED)
        else:
            self.slider.add_flag(lv.obj.FLAG.HIDDEN)
