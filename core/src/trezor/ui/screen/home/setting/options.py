import lvgl as lv

from trezor import utils, log
from trezor.ui import Style, colors, i18n, theme
from trezor.ui.screen import Navigation
from trezor.ui.component import HStack, VStack

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar, Sequence, List
    T = TypeVar["T"]

class Item(VStack):
    def __init__(self, parent, text, current , option ):
        super().__init__(parent)
        # print("current",current)
        # print("num",option)
        self.num = option
        # the `option` value
        self.option :T = None

        self.add_style(
            Style()
            # .bg_opa(lv.OPA.COVER)
            .width(lv.pct(100))
            .height(72)
            .text_color(lv.color_hex(0xFFFFFF))
            .pad_right(32)
            .pad_column(160)
            .border_width(1)
            .border_side(lv.BORDER_SIDE.BOTTOM)
            .bg_color(lv.color_hex3(0x373737)),
            0,
        )
        # self.items_center()
        # option
        # self.screenleft =  self.add(lv.obj)
        # self.screenleft.set_size(170,lv.SIZE.CONTENT)
        # #边宽为0
        # self.screenleft.set_style_border_width(2, 0)
        # # self.screenleft.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # #全透明
        # self.screenleft.set_style_bg_opa(lv.OPA.TRANSP, 0)
        # #可点击
        # self.screenleft.add_flag(lv.obj.FLAG.CLICKABLE)
        # self.screenleft.add_event_cb(self.__on_event, lv.EVENT.ALL, None)
        #显示到条目左侧
        # self.screenleft.set_style_pad_right(380, 0)
        self.label = lv.label(self)
        #宽度170
        self.label.set_size(170,lv.SIZE.CONTENT)
        self.label.set_text(text)
        self.label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        

        # self.screensaver =  lv.obj(self)
        # self.screensaver.set_size(50,50)
        # self.screensaver.set_style_pad_bottom(10, 0)
        # 距离父级容器左边260
        # self.screensaver.set_style_text_align(lv.TEXT_ALIGN.LEFT, 260)  # 这行不起作用

        # 推荐使用 align 方法来设置位置
        # self.screensaver.align_to(self.screenleft,lv.TEXT_ALIGN.LEFT, 200, 0)
        # #显示在右侧
        # self.screensaver.set_style_align(lv.ALIGN.RIGHT_MID, 10)
        # self.screensaver.set_style_radius(80, 0)
        # #边宽为0
        # self.screensaver.set_style_border_width(0, lv.PART.MAIN)
        # self.screensaver.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        # self.screensaver.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        # #边框透明
        # self.screensaver.set_style_border_opa(lv.OPA.TRANSP, 0)
        # self.screensaver.set_style_bg_color(lv.color_hex(0x0062CE), lv.PART.MAIN)
        # #全透明
        # self.screensaver.set_style_bg_opa(lv.OPA.TRANSP, 0)
        #  #可点击
        # self.screensaver.add_flag(lv.obj.FLAG.CLICKABLE)
        
        # 让点击 screensaver 等同于点击整个 Item（self）
        # def forward_event(event):
        #     # 等于点击了 self.label
        #     lv.event_send(self.label, lv.EVENT.CLICKED, None)
        # self.screensaver.add_event_cb(forward_event, lv.EVENT.ALL, None)
        # self.screensaver.add_flag(lv.obj.FLAG.EVENT_BUBBLE)

        self.state = lv.label(self)
        self.state.set_text("")
        self.state.set_size(18,18)
        #s设置居中
        self.state.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.state.set_style_text_color(colors.DS.PRIMARY, 0)
        self.state.set_style_border_width(0, lv.PART.MAIN)
        self.state.set_flex_grow(1)
        self.state.center()
         #可点击
        # self.state.add_flag(lv.obj.FLAG.CLICKABLE)
        # self.state.add_event_cb(self.__on_event, lv.EVENT.ALL, None)
        #让self.state层级在self的同级

        self.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.add_event_cb(self.__on_event, lv.EVENT.ALL, None)
        # print("self",self.option)
        # if self.option == current:
        # if self.num == 120:
        #     self.screensaver.set_style_bg_opa(lv.OPA.COVER, 0)#不透明
        #     self.state.set_text(lv.SYMBOL.OK)
        #     self.state.set_style_text_color(lv.color_hex(0xFFFFFF), 0)

    def __on_event(self, event):
        code = event.code
        if code == lv.EVENT.FOCUSED:
            self.state.set_text(lv.SYMBOL.OK)
            self.state.set_style_text_color(lv.color_hex(0x0062CE), 0)
            
            # self.screensaver.set_style_bg_opa(lv.OPA.COVER, 0)#不透明
            # #其他条目的screensaver全都透明
            # parent = self.get_parent()
            # item = utils.first([parent.get_child(i) for i in range(parent.get_child_cnt())], lambda item: item == self)
            # if item is not None:
            #     print("item is not None",item)

        elif code == lv.EVENT.DEFOCUSED:
            self.state.set_text("")
            # self.screensaver.set_style_bg_opa(lv.OPA.TRANSP, 0)#全透明
            
from trezor.ui.screen.navaigate import Navigate
class OptionDetails(Navigate):
    def __init__(self, title, options: Sequence):
        self.subscriber: lv.obj = None

        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_title(title)
        self.title.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            # .radius(16)
            # .pad_all(16)
            .height(lv.SIZE.CONTENT)
            .width(lv.pct(100))
            .bg_opa(lv.OPA.TRANSP),  # 设置完全透明
            # .bg_color(lv.color_hex(0x0D0D17)),  # 深色背景
            lv.PART.MAIN
        )
        # 容器（重新设计布局）
        self.a_container = lv.obj(self.content)
        self.a_container.set_size(440, lv.SIZE.CONTENT)
        self.a_container.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        #设置背景色
        self.a_container.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.a_container.set_style_pad_left(20, lv.PART.MAIN)
        self.a_container.set_style_border_width(0, lv.PART.MAIN)
        self.a_container.set_style_shadow_width(0, lv.PART.MAIN)  # 去除阴影
        self.a_container.set_style_outline_width(0, lv.PART.MAIN) # 去除外轮廓
        self.a_container.align(lv.ALIGN.TOP_LEFT, 0, 20)

         # 选项
        self.options_container = HStack(self.a_container)
        self.options_container.set_size(440, lv.SIZE.CONTENT)
        self.options_container.set_style_bg_color(lv.color_hex(0x0D0E17), lv.PART.MAIN)
        self.options_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.options_container.set_style_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.options_container.set_style_radius(20, lv.PART.MAIN)#圆角20
        self.options_container.set_width(lv.pct(100))
        self.options_container.align(lv.ALIGN.TOP_LEFT, -8, 0)
        self.options_container.set_style_border_width(0, lv.PART.MAIN)
        self.options_container.set_style_pad_left(10, lv.PART.MAIN)#设置左上角显示
        #设置喊行间距0
        self.options_container.set_style_pad_row(0, lv.PART.MAIN)
        self.options = [Item(self.options_container, self.option_format(o), self.current(),o) for o in options]

        for item, o in zip(self.options, options):
            # add time to item as a property
            item.option = o
            item.add_style(
                Style()
                .bg_color(lv.color_hex(0x0D0E17))
                .bg_opa(lv.OPA._90)
                .radius(16)
                .height(72)
                .width(400)
                .pad_all(8),
                lv.PART.MAIN | lv.STATE.DEFAULT
            )
            # 添加底边灰色边框
            item.set_style_border_side(lv.BORDER_SIDE.BOTTOM, lv.PART.MAIN)
            item.set_style_border_width(2, lv.PART.MAIN)
            item.set_style_border_color(lv.color_hex(0x333344), lv.PART.MAIN)
            item.set_style_border_opa(lv.OPA._50, lv.PART.MAIN)
            # if item is not None:
            #     if item.option == self.current():
            #         #item被点击一下
            #         lv.event_send(item, lv.EVENT.CLICKED, None)
        self.group = lv.group_create()
        for item in self.options:
            self.group.add_obj(item)

        # find the current and set focus
        current = self.current()

        item = utils.first(self.options, lambda item: item.option == current)
        # if item is not None:
        #     item.screensaver.set_style_bg_opa(lv.OPA.COVER, 0) # 不透明
        #     item.state.set_text(lv.SYMBOL.OK)
        #     item.state.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        lv.group_focus_obj(item)

        self.group.set_focus_cb(self.on_group_focus_changed)


    @classmethod
    def option_format(cls, v: T) -> str:
        """ format options """
        raise NotImplementedError

    @classmethod
    def current(cls) -> T:
        """the default one"""
        raise NotImplementedError

    def save_option(self, option: T):
        raise NotImplementedError

    def on_deleting(self):
        super().on_deleting()
        self.group._del()

    def on_group_focus_changed(self, group: lv._group_t):
        obj = group.get_focused()
        item = utils.first(self.options, lambda item: obj == item)
        log.debug(__name__, f"user clicked: {self.option_format(item.option)}")
        self.save_option(item.option)

        from . import __OPTION_VALUE_CHANGED
        if self.subscriber:
            lv.event_send(self.subscriber, __OPTION_VALUE_CHANGED, None)

def _time_format(t: int) -> str:
    #当前语言
    cur_language = i18n.using.code if i18n.using is not None else None
    if t < 0:
        return i18n.Text.never
    elif t < 60:
        if cur_language == "al":  # 阿拉伯语 (Arabic)
            return f"{i18n.Text.seconds} {t}"
        else:
            return f"{t} {i18n.Text.seconds}"
    elif t == 60:
        if cur_language == "al":  # 阿拉伯语 (Arabic)
            return f"{i18n.Text.minute} {t // 60}"
        else:
            return f"{t // 60} {i18n.Text.minute}"
    else:
        if cur_language == "al":  # 阿拉伯语 (Arabic)
            return f"{i18n.Text.minutes} {t // 60}"
        else:
            return f"{t // 60} {i18n.Text.minutes}"

class TimeOptionDetails(OptionDetails):
    def __init__(self, title, times: List[int]):
        super().__init__(title, times)

    @classmethod
    def option_format(cls, v: int):
        return _time_format(v)
