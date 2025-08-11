from . import *

class ChangePin(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Security.change_pin, "A:/res/pin-new.png")
        

    def action(self):
        super().action()
        from trezor import workflow
        from apps.management.change_pin import change_pin
        from trezor.messages import ChangePin
        from trezor.wire import DUMMY_CONTEXT

        workflow.spawn(change_pin(DUMMY_CONTEXT, ChangePin(remove=False)))
