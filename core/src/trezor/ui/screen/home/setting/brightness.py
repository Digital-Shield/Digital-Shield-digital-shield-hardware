import lvgl as lv

from . import *

from trezor import utils
from trezor.ui import colors

class Brightness(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.brightness, "A:/res/brightness-new.png")
        # arrow
        self.arrow = lv.img(self)
        #设置箭头背景图
        self.arrow.set_src("A:/res/a_right_arrow.png")
        #设置显示在最右边
        self.arrow.align(lv.ALIGN.OUT_RIGHT_MID, 0,0)
        # # right-arrow
        # self.arrow = lv.label(self)
        # self.arrow.set_text(lv.SYMBOL.RIGHT)
        # self.arrow.set_style_text_color(colors.DS.WHITE, lv.PART.MAIN)

    def action(self):
        log.debug(__name__, "power off")
        from trezor import workflow
        from trezor.ui.screen.brightness import Brightness
        screen = Brightness()
        workflow.spawn(screen.show())


