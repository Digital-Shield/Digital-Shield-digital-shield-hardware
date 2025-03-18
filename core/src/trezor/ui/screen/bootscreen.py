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
        bar.set_size(lv.pct(60), 8)
        bar.align(lv.ALIGN.BOTTOM_MID, 0, -32)
        bar.set_start_value(0, lv.ANIM.OFF)
        # 创建一个新的样式
        style = lv.style_t()
        style.init()
        style.set_bg_opa(lv.OPA.COVER)  # 设置背景透明度为透明
        style.set_bg_color(lv.color_hex(0xC0C0C0)) # 设置背景色为灰色
        # style.set_fg_color(lv.color_hex(0xFFFFFF), lv.PART.INDICATOR)  # 设置进度颜色为白色
        
        style.set_bg_grad_color(lv.color_hex(0xFFFFFF))  # 设置渐变色为白色
        style.set_bg_grad_dir(lv.GRAD_DIR.HOR)  # 设置渐变方向为水平
        
        # 将样式应用到进度条上
        bar.add_style(style, 0)

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
        # opa = int(v * 255 / 100)  # 计算透明度（0~255）
        # self.set_style_bg_opa(opa, lv.PART.MAIN)  # 设置透明度

    async def show(self):
        from . import manager
        await manager.switch_scene(self)
