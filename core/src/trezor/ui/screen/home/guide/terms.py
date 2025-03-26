import lvgl as lv
from typing import TYPE_CHECKING
from trezor.ui import Style, font, colors, i18n
from . import *
from trezor.ui.screen import Navigation, with_title

if TYPE_CHECKING:
    from typing import List
    pass

class Terms(with_title(Navigation)):
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
        
        view = self.add(Text)
        view.set_label(i18n.Guide.terms_title_terms_us)
        view.set_text(i18n.Guide.terms_describe_terms_us)
        
        view = self.add(Text)
        view.set_label(i18n.Guide.terms_title_product_services)
        view.set_text(i18n.Guide.terms_describe_product_services)
        
        view = self.add(Text)
        view.set_label(i18n.Guide.terms_title_risks)
        view.set_text(i18n.Guide.terms_describe_risks)

        view = self.add(Text)
        view.set_label(i18n.Guide.terms_title_disclaimers)
        view.set_text(i18n.Guide.terms_describe_disclaimers)

        view = self.add(Text)
        view.set_label(i18n.Guide.terms_title_contact_us)
        view.set_text(i18n.Guide.terms_describe_contact_us)

class Text(LabeledText):
    def __init__(self, parent):
        super().__init__(parent)
        #获取当前语言,如果是阿拉伯语则右对齐,否则左对齐
        cur_language = i18n.using.code if i18n.using is not None else None
        if cur_language == "al":
            self.add_style(
                Style()
                .border_width(0)
                .pad_top(0)
                .text_color(colors.STD.WHITE)
                .text_line_space(8)
                .pad_bottom(0)
                .text_align(lv.TEXT_ALIGN.RIGHT),  # 添加右对齐样式
                0
            )
        else:
            self.add_style(
                Style()
                .border_width(0)
                .pad_top(0)
                .text_color(colors.STD.WHITE)
                .text_line_space(8)
                .pad_bottom(0),  # 添加右对齐样式
                0
            )