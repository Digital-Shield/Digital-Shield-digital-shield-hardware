import lvgl as lv

from . import Screen

class BootScreen(Screen):
    def __init__(self):
        super().__init__()
        # self.set_style_bg_img_opa(0, lv.PART.MAIN)
        # self.bg_color = lv.color_hex(0x0D0D17)  # 固定背景颜色
        # self.set_style_bg_color(self.bg_color, lv.PART.MAIN)  # 设置背景色
        # self.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)  # 初始全透明

        img = lv.img(self.content)
        img.set_src("A:/res/logo_two.png")
        img.center()

        bar = lv.bar(self.content) 
        bar.set_size(lv.pct(60), 12)
        bar.align(lv.ALIGN.BOTTOM_MID, 0, -32)
        bar.set_start_value(0, lv.ANIM.OFF)
        bar.set_style_bg_color(lv.color_hex(0x31343B), lv.PART.MAIN | lv.STATE.DEFAULT)  # 背景色为灰色
        bar.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN | lv.STATE.DEFAULT)
        # 设置进度条指示器的颜色（进度部分的颜色）
        bar.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.INDICATOR | lv.STATE.DEFAULT) 
        bar.set_style_bg_opa(lv.OPA.COVER, lv.PART.INDICATOR | lv.STATE.DEFAULT)


        # 动画
        anim = lv.anim_t() 
        anim.init() 
        anim.set_var(bar) 
        anim.set_values(0, 100)  # 进度从 0 到 100
        anim.set_time(3000)  # 3 秒完成
        anim.set_custom_exec_cb(lambda _, v: self.update_animation(bar, v))  # 动态更新
        anim.set_ready_cb(lambda _: self.channel.publish(lv.EVENT.READY))
        anim.start()

    def update_animation(self, bar, v):
        bar.set_value(v, lv.ANIM.OFF)

    async def show(self):
        from . import manager
        await manager.switch_scene(self)
