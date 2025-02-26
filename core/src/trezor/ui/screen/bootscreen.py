import lvgl as lv

from . import Screen

class BootScreen(Screen):
    def __init__(self):
        super().__init__()
        img = lv.img(self.content)
        img.set_src("A:/res/logo.png")
        img.center()

        bar = lv.bar(self.content)
        bar.set_size(lv.pct(60), 8)
        bar.align(lv.ALIGN.BOTTOM_MID, 0, -32)
        bar.set_start_value(0, lv.ANIM.OFF)

        # an anim
        anim = lv.anim_t()
        anim.init()
        anim.set_var(bar)
        anim.set_values(0, 100)
        anim.set_time(300)
        anim.set_custom_exec_cb(lambda _, v: bar.set_value(v, lv.ANIM.OFF))
        anim.set_ready_cb(lambda _: self.channel.publish(lv.EVENT.READY))
        anim.start()

    async def show(self):
        from . import manager
        await manager.switch_scene(self)

