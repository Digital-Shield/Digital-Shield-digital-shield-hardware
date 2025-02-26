import lvgl as lv

#### Standard Colors
class STD:
    WHITE = lv.color_make(0xFF, 0xFF, 0xFF)
    SILVER = lv.color_make(0xC0, 0xC0, 0xC0)
    GRAY = lv.color_make(0x80, 0x80, 0x80)
    BLACK = lv.color_make(0x00, 0x00, 0x00)
    RED = lv.color_make(0xFF, 0x00, 0x00)
    MAROON = lv.color_make(0x80, 0x00, 0x00)
    YELLOW = lv.color_make(0xFF, 0xFF, 0x00)
    OLIVE = lv.color_make(0x80, 0x80, 0x00)
    LIME = lv.color_make(0x00, 0xFF, 0x00)
    GREEN = lv.color_make(0x00, 0x80, 0x00)
    CYAN = lv.color_make(0x00, 0xFF, 0xFF)
    AQUA = CYAN
    TEAL = lv.color_make(0x00, 0x80, 0x80)
    BLUE = lv.color_make(0x00, 0x00, 0xFF)
    NAVY = lv.color_make(0x00, 0x00, 0x80)
    MAGENTA = lv.color_make(0xFF, 0x00, 0xFF)
    PURPLE = lv.color_make(0x80, 0x00, 0x80)
    ORANGE = lv.color_make(0xFF, 0xA5, 0x00)

#### Digital Shield Colors
class DS:

    BLACK = lv.color_make(0x00, 0x00, 0x1F)
    WHITE = lv.color_make(0xFF, 0xFF, 0xFF)

    GRAY  = lv.color_make(0x57, 0x5F, 0x77)
    LIGHT_GRAY = lv.color_make(0xB3, 0xB8, 0xC5)

    RED = lv.color_make(0xCD, 0x2B, 0x31)
    GREEN = lv.color_make(0x18, 0x79, 0x4E)
    BLUE = lv.color_make(0x2F, 0x65, 0xFA)
    YELLOW = lv.color_make(0xD1, 0xE1, 0x33)

    PURPLE = lv.color_make(0x52, 0x34, 0xEA)
    ORANGE = lv.color_make(0xF7, 0xEB, 0xE3)

    SHADOW = lv.color_make(0x09, 0x2A, 0x61)
    SHADOW_OPA = lv.OPA._20

    PRIMARY = PURPLE
    SECONDARY = WHITE

    BORDER = PRIMARY

    SUCCESS = GREEN
    WARNING = YELLOW
    ERROR = RED

    PLEASURE = GREEN
    PAIN = RED

    DANGER = RED
    CRITICAL = RED

    TEXT_DEFAULT = BLACK
    TEXT_DISABLED = GRAY

    BUTTON_DEFAULT = PRIMARY # primary
    BUTTON_TEXT = WHITE

    PRESSED_FILTER_COLOR = STD.BLACK
    PRESSED_FILTER_OPA = lv.OPA._80

    CHECKED_FILTER_COLOR = BLUE
    CHECKED_FILTER_OPA = lv.OPA._30

    DISABLED_FILTER_COLOR = WHITE
    DISABLED_FILTER_OPA = lv.OPA._30

    KEYBOARD_BUTTON = WHITE
    KEYBOARD_PRESSED = PRIMARY
    KEYBOARD_PRESSED_TEXT_COLOR = WHITE

