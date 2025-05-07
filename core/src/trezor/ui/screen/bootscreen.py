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

        # gif = lv.gif(self.content)
        # gif.set_src("A:/res/wallpapers/988.gif")
        # 1. 动画实现：将GIF拆解为frame_0.png, frame_1.png...
        # 2. 代码实现
        self.img = lv.img(self.content)
        self.timer = lv.timer_create(lambda _: self.next_frame(), 10, None)  # 减小间隔时间到16ms/帧
        self.current_frame = 1
        self.max_frames = 48  # 总帧数

        bar = lv.bar(self.content) 
        bar.set_size(lv.pct(60), 12)
        bar.align(lv.ALIGN.BOTTOM_MID, 0, -32)
        bar.set_start_value(0, lv.ANIM.OFF)
        bar.set_style_bg_color(lv.color_hex(0x31343B), lv.PART.MAIN | lv.STATE.DEFAULT)  # 背景色为灰色
        bar.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT)
        # 设置进度条指示器的颜色（进度部分的颜色）
        bar.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.INDICATOR | lv.STATE.DEFAULT) 
        bar.set_style_bg_opa(lv.OPA.COVER, lv.PART.INDICATOR | lv.STATE.DEFAULT)


        # 动画
        anim = lv.anim_t() 
        anim.init() 
        # anim.set_var(bar) 
        # anim.set_values(0, 100)  # 进度从 0 到 100
        anim.set_time(11000)  # 11秒完成
        # anim.set_custom_exec_cb(lambda _, v: self.update_animation(bar, v))  # 动态更新
        anim.set_ready_cb(lambda _: self.channel.publish(lv.EVENT.READY))
        anim.start()

    def next_frame(self):
        if self.current_frame <= self.max_frames:
            try:
                self.img.set_src(f"A:/res/bootGifs/qingmiao_{self.current_frame}.png")
            except Exception as e:
                self.timer._del()  # Stop the timer if an error occurs
            self.current_frame += 1
        else:
            print("动画播放完毕")
            self.timer._del()  # 删除定时器

    def update_animation(self, bar, v):
        bar.set_value(v, lv.ANIM.OFF)

    async def show(self):
        from . import manager
        await manager.switch_scene(self)
