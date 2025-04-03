import lvgl as lv

from trezor import io, log, loop, workflow
from trezor.ui import i18n
from trezor.ui.screen import Navigation

CAMERA = io.Camera(io.CAMERA, 400, 400)

class ScanApp(Navigation):

    def __init__(self):
        super().__init__()
        self.set_title(i18n.App.scan)

        self.led = self.add(lv.img)
        self.led.set_src(self.flashlight_img_src)
        self.led.align(lv.ALIGN.BOTTOM_MID, 0, -32)
        self.led.add_flag(lv.obj.FLAG.CLICKABLE)
        self.led.add_event_cb(lambda _: self.toggle_led(), lv.EVENT.CLICKED, None)

        self.task = workflow.spawn(self.scanning())
        workflow.spawn(self.start_camera())

        # test camera state code
        # btn = self.add(Button)
        # btn.set_text("toggle")
        # btn.align(lv.ALIGN.BOTTOM_LEFT, 32, -32)
        # btn.add_event_cb(lambda _: self.toggle_camera(), lv.EVENT.CLICKED, None)
        # self.state = 0

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
        CAMERA.hide()

    def on_deleting(self):
        super().on_deleting()
        CAMERA.stop()
        self.task.close()
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
            return "A:/res/camera-led-off.png"
        else:
            return "A:/res/camera-led-on.png"

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
                await show_warning(
                    ctx,
                    i18n.Text.invalid_ur,
                    i18n.Title.invalid_data,
                    i18n.Button.try_again,
                )
                airgap.reset()
            elif event == 3:
                airgap.reset()
                workflow.spawn(self.restart_camera())
