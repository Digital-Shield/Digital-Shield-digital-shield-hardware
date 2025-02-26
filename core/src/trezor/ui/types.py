from typing import TYPE_CHECKING

"""
Collect types for type annotations, checking
"""
if TYPE_CHECKING:
    from typing import TypeVar, Type, Callable, Union, Optional, Generic, Generator
    from typing import Sequence, List, Dict, Tuple
    from trezor.ui.screen import Screen

    # generic type
    T = TypeVar("T")

    # generic return type
    R = TypeVar("R")

    S = TypeVar("S", bound=Screen)

    # widget for ui
    from typing import Protocol
    # widget is a lvgl object, which need a parent for initialization
    class WidgetProtocol(Protocol):
        def __init__(self, parent) -> None: ...

    Widget = TypeVar("Widget", bound=WidgetProtocol)
