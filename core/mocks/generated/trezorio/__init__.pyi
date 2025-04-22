from typing import *


# extmod/modtrezorio/modtrezorio-battery.h
class Battery:
    """
    """

    def __init__(self):
        """
        """

    def state_of_charge(self) -> int|None:
        """
        read SOC (state of charge), in percent
        Returns None if the battery is not present
        Returns int between 0 and 100
        """

    def current(self) -> int|None:
        """
        read (current), in 1mA
        Returns current in mA, positive in discharging, negative is charging
        """

    def voltage(self) -> int:
        """
        read (voltage), in 1mV
        Returns voltage in mV
        """


# extmod/modtrezorio/modtrezorio-ble.h
class BLE:
    """
    """

    def __init__(
        self,
    ) -> None:
        """
        """

    def ctrl(self, cmd: byte, value: byte) -> None:
        """
        Send command to the BLE.
        """

    def power_on() -> None:
        """
        Turn on the BLE.
        """

    def power_off() -> None:
        """
        Turn off the BLE.
        """


# extmod/modtrezorio/modtrezorio-camera.h
class Camera:
    """
    Camera configuration.
    """
    NONE: int = 0
    INIT: int = 1
    STOPPED: int = 2
    SUSPENDED: int = 3
    CAPTURING: int = 4
    def __init__(self, iface_num: int, width: int, height: int) -> None:
        ...
    def iface_num(self) -> int:
        ...
    def init(self) -> None:
        ...
    def deinit(self) -> None:
        ...
    def start(self) -> None:
        ...
    def stop(self) -> None:
        ...
    def suspend(self) -> None:
        ...
    def resume(self) -> None:
        ...
    def hide(self) -> None:
        ...
    def show(self) -> None:
        ...
    def led_on(self) -> None:
        ...
    def led_off(self) -> None:
        ...
    def led_toggle(self) -> None:
        ...
    def led_state(self) -> int:
        ...
    def buffer(self) -> bytes:
        ...
    def state(self) -> int:
        ...
    def width(self) -> int:
        ...
    def height(self) -> int:
        ...


# extmod/modtrezorio/modtrezorio-flash.h
class FlashOTP:
    """
    """

    def __init__(self) -> None:
        """
        """

    def write(self, block: int, offset: int, data: bytes) -> None:
        """
        Writes data to OTP flash
        """

    def read(self, block: int, offset: int, data: bytearray) -> None:
        """
        Reads data from OTP flash
        """

    def lock(self, block: int) -> None:
        """
        Lock OTP flash block
        """

    def is_locked(self, block: int) -> bool:
        """
        Is OTP flash block locked?
        """


# extmod/modtrezorio/modtrezorio-hid.h
class HID:
    """
    USB HID interface configuration.
    """

    def __init__(
        self,
        iface_num: int,
        ep_in: int,
        ep_out: int,
        emu_port: int,
        report_desc: bytes,
        subclass: int = 0,
        protocol: int = 0,
        polling_interval: int = 1,
        max_packet_len: int = 64,
    ) -> None:
        """
        """

    def iface_num(self) -> int:
        """
        Returns the configured number of this interface.
        """

    def write(self, msg: bytes) -> int:
        """
        Sends message using USB HID (device) or UDP (emulator).
        """

    def write_blocking(self, msg: bytes, timeout_ms: int) -> int:
        """
        Sends message using USB HID (device) or UDP (emulator).
        """


# extmod/modtrezorio/modtrezorio-moto.h
class MOTOR:
    """
    """

    def __init__(
        self,
    ) -> None:
        """
        """

    def ctrl(self, start: bool) -> None:
        """
        Control the motor start or stop
        """


# extmod/modtrezorio/modtrezorio-poll.h
def poll(ifaces: Iterable[int], list_ref: list, timeout_ms: int) -> bool:
    """
    Wait until one of `ifaces` is ready to read or write (using masks
    `list_ref`:
    `list_ref[0]` - the interface number, including the mask
    `list_ref[1]` - for touch event, tuple of:
                    (event_type, x_position, y_position)
                  - for button event (T1), tuple of:
                    (event type, button number)
                  - for USB read event, received bytes
                  - for Camera scan event, scanned bytes
    If timeout occurs, False is returned, True otherwise.
    """


# extmod/modtrezorio/modtrezorio-sbu.h
class SBU:
    """
    """

    def __init__(self) -> None:
        """
        """

    def set(self, sbu1: bool, sbu2: bool) -> None:
        """
        Sets SBU wires to sbu1 and sbu2 values respectively
        """


# extmod/modtrezorio/modtrezorio-spi.h
class SPI:
    """
    """

    def __init__(
        self,
        iface_num: int,
    ) -> None:
        """
        """

    def iface_num(self) -> int:
        """
        Returns the configured number of this interface.
        """

    def write(self, msg: bytes) -> int:
        """
        Sends message using SPI.
        """


# extmod/modtrezorio/modtrezorio-usb.h
class USB:
    """
    USB device configuration.
    """

    def __init__(
        self,
        vendor_id: int,
        product_id: int,
        release_num: int,
        device_class: int = 0,
        device_subclass: int = 0,
        device_protocol: int = 0,
        manufacturer: str = "",
        product: str = "",
        interface: str = "",
        usb21_enabled: bool = True,
        usb21_landing: bool = True,
    ) -> None:
        """
        """

    def add(self, iface: HID | VCP | WebUSB) -> None:
        """
        Registers passed interface into the USB stack.
        """

    def open(self, serial_number: str) -> None:
        """
        Initializes the USB stack.
        """

    def close(self) -> None:
        """
        Cleans up the USB stack.
        """

    def state(self) -> bool:
        """
        Get USB state.
        """


# extmod/modtrezorio/modtrezorio-vcp.h
class VCP:
    """
    USB VCP interface configuration.
    """

    def __init__(
        self,
        iface_num: int,
        data_iface_num: int,
        ep_in: int,
        ep_out: int,
        ep_cmd: int,
        emu_port: int,
    ) -> None:
        """
        """

    def iface_num(self) -> int:
        """
        Returns the configured number of this interface.
        """


# extmod/modtrezorio/modtrezorio-webusb.h
class WebUSB:
    """
    USB WebUSB interface configuration.
    """

    def __init__(
        self,
        iface_num: int,
        ep_in: int,
        ep_out: int,
        emu_port: int,
        subclass: int = 0,
        protocol: int = 0,
        polling_interval: int = 1,
        max_packet_len: int = 64,
    ) -> None:
        """
        """

    def iface_num(self) -> int:
        """
        Returns the configured number of this interface.
        """

    def write(self, msg: bytes) -> int:
        """
        Sends message using USB WebUSB (device) or UDP (emulator).
        """
from . import fatfs, sdcard
POLL_READ: int  # wait until interface is readable and return read data
POLL_WRITE: int  # wait until interface is writable
TOUCH: int  # interface id of the touch events
TOUCH_START: int  # event id of touch start event
TOUCH_MOVE: int  # event id of touch move event
TOUCH_END: int  # event id of touch end event
UART: int  # interface id of the uart events
USB_STATE: int  # interface id of the usb state events
BUTTON: int  # interface id of button events
BUTTON_PRESSED: int  # button down event
BUTTON_RELEASED: int  # button up event
BUTTON_LEFT: int  # button number of left button
BUTTON_RIGHT: int  # button number of right button
WireInterface = Union[HID, WebUSB, SPI]
USB_CHECK: int # interface id for check of USB data connection
