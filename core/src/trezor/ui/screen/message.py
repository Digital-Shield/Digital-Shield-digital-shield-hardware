import lvgl as lv

from trezor.ui import i18n, Done, colors,theme
from trezor.ui.screen import Modal
from trezor.ui.component.container import HStack

class Message(Modal):
    """
    Message screen use for display message for user

    It have a button. User only need click the button, means "Yes, I have know"
    """
    def __init__(self, title, message, icon=None):
        super().__init__()
        if title:
            self.title.set_text(title)

        self.btn_right.set_text(i18n.Button.ok)

        self.content.set_style_pad_all(16, lv.PART.MAIN)

        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(theme.Styles.board, lv.PART.MAIN)

        self.content.items_center()
        self.content.center()

        if icon:
            self.add(lv.img).set_src(icon)

        if message:
            self.text = self.add(lv.label)
            self.text.set_long_mode(lv.label.LONG.WRAP)
            self.text.set_width(lv.pct(90))
            self.text.set_height(lv.SIZE.CONTENT)
            # `max_width` not work in this version lvgl
            # self.msg.set_style_max_width(320, 0)
            self.text.set_text(message)
            self.text.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            self.text.set_style_text_line_space(8, 0)
            self.text.set_style_text_color(colors.DS.WHITE, 0)
            self.text.set_style_pad_top(15, 0)

        self.btn = self.btn_right

        self.btn.add_event_cb(lambda _: self.on_click_ok(), lv.EVENT.CLICKED, None)

    def button_text(self, text):
        label :lv.label= self.btn.get_child(0)
        label.set_text(text)

    def text_color(self, color):
        self.text.set_style_text_color(color, 0)

    def on_click_ok(self):
        self.close(Done())

class Info(Message):
    def __init__(self, title, message):
        super().__init__(title, message, "A:/res/info-two.png")

class Success(Message):
    def __init__(self, title, message):
        super().__init__(title, message, "A:/res/success.png")
        self.text_color(colors.DS.PLEASURE)

class Warning(Message):
    def __init__(self, title, message):
        super().__init__(title, message, "A:/res/warning.png")
        self.text_color(colors.DS.PLEASURE)

class Error(Message):
    def __init__(self, title, message):
        super().__init__(title, message, "A:/res/error.png")
        self.text_color(colors.DS.DANGER)
