from . import *

class WipeDevice(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Security.wipe_device, "A:/res/wipe-device.png")

    def action(self):
        super().action()
        from trezor import workflow
        from apps.management.wipe_device import wipe_device
        from trezor.messages import WipeDevice
        from trezor.wire import DUMMY_CONTEXT

        workflow.spawn(wipe_device(DUMMY_CONTEXT, WipeDevice()))
