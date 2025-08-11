import lvgl as lv

from trezor import io, log, loop, workflow
from trezor.ui import i18n
from trezor.ui.screen import Navigation
from trezor.ui.screen.navaigate import Navigate

CAMERA = io.Camera(io.CAMERA, 360, 360)
# CAMERA.set_style_radius(16, lv.PART.MAIN)  # Removed: Camera object has no such method
#怎么设置圆角
class ScanApp(Navigate):

    def __init__(self):
        super().__init__()
        #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_title(i18n.App.scan)

        self.led = self.add(lv.img)
        self.led.set_src(self.flashlight_img_src)
        self.led.align(lv.ALIGN.BOTTOM_MID, 0, -32)
        self.led.add_flag(lv.obj.FLAG.CLICKABLE)
        self.led.add_event_cb(lambda _: self.toggle_led(), lv.EVENT.CLICKED, None)

        # #创建一个容器，将camera和label都放在这个容器中
        # self.container = self.add(lv.obj)
        # self.container.set_size(370, 370)
        # #边框为0
        # self.container.set_style_border_width(0, lv.PART.MAIN)
        # self.container.set_style_radius(16, lv.PART.MAIN)
        # self.container.align(lv.ALIGN.CENTER, 0, 0)
        # #将CAMERA显示到容器中央
        # self.container.add(CAMERA).align(lv.ALIGN.CENTER, 0, 0)
        # 在CAMERA正下方显示一行文字
        self.scan_label = self.add(lv.label)
        self.scan_label.set_text(i18n.Title.scan_ercode)
        #文字白色
        self.scan_label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
        self.scan_label.align(lv.ALIGN.BOTTOM_MID, -10, -180)  # 距离底部再近一些

        self.task = workflow.spawn(self.scanning())
        workflow.spawn(self.start_camera())

    def toggle_camera(self):
        self.state %= 4
        if self.state == 0:
            CAMERA.suspend()
        elif self.state == 1:
            CAMERA.resume()
        elif self.state == 2:
            CAMERA.hide()
        elif self.state == 3:
            CAMERA.show()
        self.state += 1

    def on_loaded(self):
        super().on_loaded()
        log.debug(__name__, f"camera state: {CAMERA.state()}")
        if CAMERA.state() == io.Camera.SUSPENDED:
            log.debug(__name__, "show camera")
            CAMERA.show()

    def on_unload_start(self):
        super().on_unload_start()
        if CAMERA.led_state() == io.Camera.LED_ON:
            CAMERA.led_off()
        CAMERA.suspend()
        CAMERA.hide()

    def on_deleting(self):
        super().on_deleting()
        CAMERA.stop()
        self.task.close()
        CAMERA.hide()
        CAMERA.deinit()

    @staticmethod
    async def start_camera():
        await loop.sleep(500)
        CAMERA.init()
        CAMERA.start()

    @staticmethod
    async def restart_camera():
        CAMERA.show()

    @property
    def flashlight_img_src(self) -> str:
        if CAMERA.led_state() == io.Camera.LED_OFF:
            return "A:/res/led_off.png"
        else:
            return "A:/res/led_on.png"

    def toggle_led(self):
        CAMERA.led_toggle()
        # update led image
        self.led.set_src(self.flashlight_img_src)

    async def scanning(self):
        from trezor.airgap import Airgap
        from trezor.airgap.event import InvalidUR
        from trezor.ui.layouts import show_warning
        from trezor.wire import DUMMY_CONTEXT as ctx

        airgap = Airgap.instance()
        airgap.reset()

        while True:
            event = await airgap.event_hub.take()
            log.debug(__name__, f"event: {event}")
            if isinstance(event, InvalidUR):
                airgap.reset()
                await show_warning(
                    ctx,
                    i18n.Text.invalid_ur,
                    i18n.Title.invalid_data,
                    i18n.Button.try_again,
                )
            elif event == 3:
                airgap.reset()
                print("airgap reset - 初始化了")
                CAMERA.init()
                workflow.spawn(self.restart_camera())
    #退出                
    def on_nav_back(self, event):
            CAMERA.hide()
            from trezor.ui.screen import manager
            manager.mark_dismissing(self)
            from trezor.ui import NavigationBack
            # should notify caller
            self.channel.publish(NavigationBack())
            # from ... import manager
            # from trezor import workflow
            # workflow.spawn(manager.pop(self))  