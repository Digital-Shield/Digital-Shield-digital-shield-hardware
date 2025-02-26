import lvgl as lv
from micropython import const

from . import *
from trezor import motor, io
from storage import device

BLE_CMD_CTRL = const(0x81)

BLE_CMD_CTRL_OP_OPEN = const(1)
BLE_CMD_CTRL_OP_CLOSE = const(2)
BLE_CMD_CTRL_OP_DISCONNECT = const(3)

class Bluetooth(ToggleItem):

    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.bluetooth, "A:/res/ble-connected.png")
        self.checked = device.ble_enabled()

    def toggle(self):
        motor.vibrate()
        enabled = self.checked
        log.debug(__name__, f"bluetooth {'enabled' if enabled else 'disabled'}")
        device.set_ble_status(enabled)
        ble = io.BLE()
        if enabled:
            ble.ctrl(BLE_CMD_CTRL, BLE_CMD_CTRL_OP_OPEN)
            # ble.power_on()
            # StatusBar.instance().show_ble(StatusBar.BLE_STATE_ENABLED)
        else:
            ble.ctrl(BLE_CMD_CTRL, BLE_CMD_CTRL_OP_DISCONNECT)
            ble.ctrl(BLE_CMD_CTRL, BLE_CMD_CTRL_OP_CLOSE)
            # power off reduce battery use
            # ble.power_off()
            # StatusBar.instance().show_ble(StatusBar.BLE_STATE_DISABLED)
