import lvgl as lv

from trezor import utils

# 粗体
class Bold:
    if utils.EMULATOR:
        SCS48 = lv.font_load("A:/res/PlusJakartaSans-Bold-48.bin")
        SCS38 = lv.font_load("A:/res/lv_font_source_han_bold_38.bin")
        SCS30 = lv.font_load("A:/res/lv_font_source_han_bold_30.bin")
        SCS26 = lv.font_load("A:/res/lv_font_source_han_bold_26.bin")
    else:
        SCS48 = lv.font_pljs_bold_48
        SCS38 = lv.font_scs_bold_38
        SCS30 = lv.font_scs_bold_30
        SCS26 = lv.font_scs_bold_26

# 常规
class Regular:
    if utils.EMULATOR:
        SCS30 = lv.font_load("A:/res/lv_font_source_han_reg_30.bin")
        SCS26 = lv.font_load("A:/res/lv_font_source_han_reg_26.bin")
        SCS24 = lv.font_load("A:/res/lv_font_source_han_reg_24.bin")
    else:
        SCS30 = lv.font_scs_reg_30
        SCS26 = lv.font_scs_reg_26
        SCS24 = lv.font_scs_reg_24

# 等宽
class Mono:
    # JetBrainsMono
    if utils.EMULATOR:
        JB28 = lv.font_load("A:/res/JetBrainsMono-Medium-28.bin")
    else:
        JB28 = lv.font_mono_reg_28



default = Regular.SCS26
large = Regular.SCS30
small = Regular.SCS24
bold = Bold.SCS30
mono = Mono.JB28
if utils.EMULATOR:
    status_bar = lv.font_load("A:/res/PlusJakartaSans-Regular-24.bin")
else:
    status_bar = lv.font_status_bar
