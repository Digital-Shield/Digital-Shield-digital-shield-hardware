import lvgl as lv

from . import *

from trezor.ui import i18n, Style, colors,font
from trezor.ui.screen import Navigation
from trezor.ui.theme import Styles
from trezor.ui.component.container import HStack

counts = [12, 18, 24]

class WordcountScreen(Navigation):
    def __init__(self):
        super().__init__()
        # self.set_title(i18n.Title.select_word_count, "A:/res/app_security.png")
        self.set_title(i18n.Title.select_word_count)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style()
            .pad_top(25),
            0
        )
        self.counts = [self.create_count_item(count) for count in counts]

    def create_count_item(self, count):
        # a container
        obj = lv.obj(self.content)
        obj.add_style(item_style, 0)
        obj.add_event_cb(lambda e: self.channel.publish(count), lv.EVENT.CLICKED, None)

        label = lv.label(obj)
        label.set_recolor(True)
        label.add_style(Styles.title_text, 0)
        label.set_text(i18n.Text.str_words.format(count))
        label.center()

        return obj
