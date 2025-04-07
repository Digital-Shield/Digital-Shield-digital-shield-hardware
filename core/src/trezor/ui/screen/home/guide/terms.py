import lvgl as lv
from typing import TYPE_CHECKING
from trezor.ui import Style, font, colors, i18n
from . import *
from trezor.ui.screen import Navigation

if TYPE_CHECKING:
    from typing import List
    pass

class Terms(Navigation):
    def __init__(self,title):
        super().__init__()
        self.set_title(title)
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style().pad_left(16).pad_right(16),
            0
        )
        contaner = self.add(lv.obj)
        contaner.add_style(
            theme.Styles.container,
            0
        )
        contaner.set_height(lv.SIZE.CONTENT)
        contaner.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
        #一、接受條款
        label = self.add(lv.label)
        label.set_text(i18n.Guide.accept_tems)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        label.set_style_text_font(font.Bold.SCS30, 0)

        # label = self.add(lv.label)
        # label.set_text(i18n.Guide.use_range)
        # label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        # label.set_style_text_font(font.Bold.SCS26, 0)
        
        # 適用範圍
        view = self.add(Text)
        view.set_label_2(i18n.Guide.use_range)
        view.set_text(i18n.Guide.range_include)
        # view.add_style(
        #     Style()
        #     .text_color(colors.STD.WHITE)
        #     .text_line_space(8),
        #     0
        # )
        view.set_text(view.get_text() + "\n" + i18n.Guide.range_include_1)#
        # 用戶資格
        view = self.add(Text)
        view.set_label_2(i18n.Guide.user_qualification)
        view.set_text(i18n.Guide.ability_include)
        view.set_text(view.get_text() + "\n" + i18n.Guide.ability_include_1)
        # 條款更新與通知
        view = self.add(Text)
        view.set_label_2(i18n.Guide.terms_update_infor)
        view.set_text(i18n.Guide.update_infor_content)

         #二、硬體錢包購買條款
        label = self.add(lv.label)
        label.set_text(i18n.Guide.wallet_buy_iterms)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        label.set_style_text_font(font.Bold.SCS30, 0)
        #1. 訂單流程
        view = self.add(Text)
        view.set_label_2(i18n.Guide.order_process)
        view.set_text(i18n.Guide.payment_confirmation)
        view.set_text(view.get_text() + "\n" + i18n.Guide.inventory_shortage)
        view.set_text(view.get_text() + "\n" + i18n.Guide.inventory_shortage_1 + "\n" + i18n.Guide.inventory_shortage_2)
        #2. 退換政策
        view = self.add(Text)
        view.set_label_2(i18n.Guide.return_and_exchange_policy)
        view.set_text(i18n.Guide.return_and_exchange_condi)#退貨條件：
        view.set_text(view.get_text() + "\n" + i18n.Guide.return_and_exchange_condi_con)
        view.set_text(view.get_text() + "\n" + i18n.Guide.warranty_scope)#保修範圍：
        view.set_text(view.get_text() + "\n" + i18n.Guide.warranty_scope_1 + "\n" + i18n.Guide.warranty_scope_2 + "\n" + i18n.Guide.warranty_scope_3)

        #三、免責聲明
        label = self.add(lv.label)
        label.set_text(i18n.Guide.disclaimer)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        label.set_style_text_font(font.Bold.SCS30, 0)
        #1. 產品風險
        view = self.add(Text)
        view.set_label_2(i18n.Guide.product_risk)
        #物理風險：
        view.set_text(i18n.Guide.physical_risk)
        view.set_text(view.get_text() + "\n" + i18n.Guide.physical_risk_1 + "\n" + i18n.Guide.physical_risk_2)
        #供應鏈風險：
        view.set_text(view.get_text() + "\n" + i18n.Guide.supply_chain_risk)
        view.set_text(view.get_text() + "\n" + i18n.Guide.supply_chain_risk_1 + "\n" + i18n.Guide.supply_chain_risk_2)
        #2. 服務中斷
        view = self.add(Text)
        view.set_label_2(i18n.Guide.service_interruption)
        view.set_text(i18n.Guide.service_interruption_1 + "\n" + i18n.Guide.service_interruption_2)
class Text(LabeledText):
    def __init__(self, parent):
        super().__init__(parent)
        self._text = ""  # 初始化 _text 属性
        self.set_label("")  # 设置默认文本为空
        self.add_style(
            Style()
            .border_width(0)
            .pad_top(0)
            .text_color(colors.STD.WHITE)
            .text_line_space(8)
            .pad_bottom(0),  
            0
        )
        #获取当前语言,如果是阿拉伯语则右对齐,否则左对齐
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            self.set_style_base_dir(lv.BASE_DIR.RTL, lv.PART.MAIN)# 设置文本方向为从右到左
    def set_text(self, text: str):
        self._text = text  # 更新 _text 属性
        super().set_text(text)  # 调用父类的 set_text 方
    def get_text(self) -> str:
        #文本加粗
        self.set_style_text_font(font.Bold.SCS26, lv.PART.MAIN)
        return self._text  # 返回存储的文本内容
    
