import lvgl as lv
# 粗体
class Bold:
    SCS48 = lv.font_pljs_bold_48
    SCS38 = lv.font_scs_bold_38
    SCS30 = lv.font_scs_bold_30
    SCS26 = lv.font_scs_bold_26

# 常规
class Regular:
    SCS30 = lv.font_scs_reg_30
    SCS26 = lv.font_scs_reg_26
    SCS28 = lv.font_scs_reg_28 #这个新加的加不上
    SCS24 = lv.font_scs_reg_24

# #中粗体-新加
class Medium:
    SCS40 = lv.font_scs_med_40
    SCS32 = lv.font_scs_med_32
    SCS28 = lv.font_scs_med_28


# 等宽
class Mono:
    JB28 = lv.font_mono_reg_28

default = Regular.SCS26
large = Regular.SCS30
small = Regular.SCS24
bold = Bold.SCS30
mono = Mono.JB28
status_bar = lv.font_status_bar
