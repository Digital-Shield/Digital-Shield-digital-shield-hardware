import lvgl as lv

from . import manager

from trezor import loop, log
from trezor.ui import Style, events, theme, colors
from trezor.ui.constants import SCREEN_WIDTH, SCREEN_HEIGHT

# for type annotations
from trezor.ui.types import *

# control use background image or not
__USE_BACKGROUND_IMAGE__ = True


class Screen(lv.obj):
    """
    Screen 是呈现在屏幕上的 UI 组件。 一页界面，就是一个 Screen
    """

    def __init__(self):
        super().__init__()

        # maybe speedup if not use background image
        if __USE_BACKGROUND_IMAGE__:
            self.set_style_bg_img_src("A:/res/background_six.png", lv.PART.MAIN)

        # an empty content view, this is the root of `all` user UI components
        # almost all
        # default content is self
        self._content: lv.obj = self

        # a channel for events
        self.channel = loop.chan()

        self.set_width(SCREEN_WIDTH)
        self.set_height(SCREEN_HEIGHT)
        self.clear_flag(lv.obj.FLAG.SCROLLABLE)

        # a channel for screen lifecycle
        self.__life_chan = loop.chan()
        self.add_event_cb(
            lambda _: self.on_load_start(), lv.EVENT.SCREEN_LOAD_START, None
        )
        self.add_event_cb(lambda _: self.on_loaded(), lv.EVENT.SCREEN_LOADED, None)
        self.add_event_cb(
            lambda _: self.on_unload_start(), lv.EVENT.SCREEN_UNLOAD_START, None
        )
        self.add_event_cb(lambda _: self.on_unloaded(), lv.EVENT.SCREEN_UNLOADED, None)
        self.add_event_cb(lambda _: self.on_deleting(), lv.EVENT.DELETE, None)

    def create_content(self, cls: Type[Widget]):
        """
        Create a `Widget` as the `content`

        The `content` is part of current `content` view
        """
        content = cls(self.content)
        content.add_style(theme.Styles.container, lv.PART.MAIN)
        self._content = content

    @property
    def content(self) -> Widget:
        return self._content

    # component manager
    def add(self, cls: Type[Widget]) -> Widget:
        """
        Add a `Widget` to the `content`
        """
        return cls(self.content)

    # screen life cycle
    def on_load_start(self):
        log.debug(__name__, f"{self.__class__.__name__} load start")
        self.__life_chan.publish(lv.EVENT.SCREEN_LOAD_START)

    def on_loaded(self):
        log.debug(__name__, f"{self.__class__.__name__} loaded")
        self.__life_chan.publish(lv.EVENT.SCREEN_LOADED)

    def on_unload_start(self):
        log.debug(__name__, f"{self.__class__.__name__} unload start")
        self.__life_chan.publish(lv.EVENT.SCREEN_UNLOAD_START)

    def on_unloaded(self):
        log.debug(__name__, f"{self.__class__.__name__} unloaded")
        self.__life_chan.publish(lv.EVENT.SCREEN_UNLOADED)

    def on_deleting(self):
        log.debug(__name__, f"{self.__class__.__name__} deleting")
        self.__life_chan.publish(lv.EVENT.DELETE)

    async def __waiting(self, event: int):
        while True:
            e = await self.__life_chan.take()
            if e == event:
                return event

    async def wait_loaded(self):
        await self.__waiting(lv.EVENT.SCREEN_LOADED)

    async def wait_unloaded(self):
        await self.__waiting(lv.EVENT.SCREEN_UNLOADED)

    async def show(self):
        """
        Show the screen.

        User decide how to show it.
        """
        log.debug(__name__, f"{self.__class__.__name__} show")
        pass

    def dismiss(self):
        """
        Dismiss the screen.

        User decide how to dismiss it.
        """
        log.debug(__name__, f"{self.__class__.__name__} dismiss")
        pass

    def close(self, value: R):
        """
        Close the screen, and return `value`
        """
        self.channel.publish(value)
        self.dismiss()

    # make `Screen` awaitable
    # see https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md#4-designing-classes-for-asyncio
    # https://peps.python.org/pep-0492/#await-expression
    def __await__(self) -> Generator[R]:
        return (yield from self.channel.take())

    __iter__ = __await__


# Two type of interactions:
# 1. Navigation
# 2. Modal
class Navigation(Screen):

    def __init__(self):
        super().__init__()
        # leave space for navigation, state bar
        self.set_style_pad_top(64, lv.PART.MAIN)

        # navigation icon container
        # global ui component, not belong to `content`
        obj = lv.obj(self)
        obj.set_size(64, 64)
        obj.add_style(Style().bg_opa(lv.OPA.TRANSP).border_width(0), lv.PART.MAIN)
        obj.add_flag(lv.obj.FLAG.CLICKABLE)
        # position is relative to the `content` area, `content` is padded top 64
        # so we need to offset by -64
        obj.set_pos(0, -64)

        nav = lv.img(obj)
        nav.set_src("A:/res/nav-back.png")
        nav.center()
        nav.add_flag(lv.obj.FLAG.CLICKABLE)
        nav.add_flag(lv.obj.FLAG.EVENT_BUBBLE)

        obj.add_event_cb(self.on_nav_back, lv.EVENT.CLICKED, None)
        self.add_event_cb(self.on_nav_back, events.NAVIGATION_BACK, None)

    def on_nav_back(self, event):
        from trezor.ui import NavigationBack

        # should notify caller
        self.channel.publish(NavigationBack())
        from . import manager
        from trezor import workflow

        workflow.spawn(manager.pop(self))

    def on_loaded(self):
        super().on_loaded()
        # a small `gesture pad` for navigation back by swipe right from left screen edge
        # create when load screen done to make it one top of all other widgets
        # there is another way: create a `navigator` on `top_layer` like `StatusBar`
        navigator = lv.obj(self)
        # it not active on all left edge
        navigator.add_style(
            Style().width(32).height(lv.pct(60)).bg_opa(lv.OPA.TRANSP).border_width(0),
            lv.PART.MAIN,
        )
        navigator.set_pos(0, 160)
        navigator.add_flag(lv.obj.FLAG.CLICKABLE)
        navigator.clear_flag(lv.obj.FLAG.SCROLLABLE)
        navigator.clear_flag(lv.obj.FLAG.GESTURE_BUBBLE)
        navigator.add_event_cb(self.__on_swipe, lv.EVENT.GESTURE, None)

    def __on_swipe(self, event):
        dir = lv.indev_get_act().get_gesture_dir()
        if dir == lv.DIR.RIGHT:
            lv.indev_get_act().wait_release()
            # send events.NAVIGATION_BACK to active screen
            lv.event_send(self, events.NAVIGATION_BACK, None)
            log.debug(__name__, "gesture navigation back")

    async def show(self):
        await super().show()
        await manager.push(self)

    # as navigation styled screen, it should provide `dismiss` function?
    # does user need close it by code?
    # def dismiss(self):
    #     from . import manager
    #     manager.pop()


class Modal(Screen):
    """
    Model Screen

    User should call `dismiss` when done something
    """

    def __init__(self):
        super().__init__()
        self._auto_close_timeout = None
        self._auto_close_task = None
        # leave space for state bar
        self.set_style_pad_top(64, lv.PART.MAIN)

    @property
    def auto_close_timeout(self):
        """
        Auto close timeout in milliseconds.
        """
        return self._auto_close_timeout

    @auto_close_timeout.setter
    def auto_close_timeout(self, value):
        self._auto_close_timeout = value
        from trezor import workflow
        if self._auto_close_task:
            # user update `auto_close_timeout`, need to close old task
            log.debug(__name__, "user update auto close timeout, close old auto close task")
            self._auto_close_task.close()
        self._auto_close_task = workflow.spawn(self._auto_close())

    async def _auto_close(self):
        from trezor import loop
        from trezor.ui import AutoClose

        await loop.sleep(self.auto_close_timeout)
        self.close(AutoClose())

    async def show(self):
        await super().show()
        await manager.push(self)

    def dismiss(self):
        super().dismiss()
        from trezor import workflow

        workflow.spawn(manager.pop(self))

# 可能使用组合的方式给`Screen`添加 `Title` 和 `Button` 是一个更好的方式

if TYPE_CHECKING:
    from trezor.ui.component import HStack, Title, Button
    S = TypeVar("S", bound=Screen)
    # for type annotation
    class TitledScreen(Screen):
        def __init__(self):
            self.title: Title
            ...

        def set_title(self, title: str, icon: str|None = None):
            ...

    class ButtonsScreen(Screen):
        def __init__(self):
            self.btn_right: Button
            self.btn_left: Button|None

    class ButtonsTitledScreen(ButtonsScreen, TitledScreen, Screen):
        ...

def with_title(cls: Type[S]) -> Type[TitledScreen]:
    """
    Add title to screen.

    class MyScreen(with_title(Screen)):
        pass

    # a titled modal
    class MyModal(with_title(Modal)):
        pass
    """

    from trezor.ui.component import HStack, Title
    class Titled(cls):
        def __init__(self):
            super().__init__()

            # use HStack as content ot manager title and remaining content
            self.create_content(HStack)
            self.content: HStack

            # add title
            self.title = self.add(Title)

            # `content` is remained, for draw all other ui components
            self.create_content(lv.obj)
            self.content.set_flex_grow(1)

            self.content: lv.obj

        def set_title(self, title: str, icon: str|None = None):
            # can get title width, title can very long? do need wrap?
            # from trezor.ui import font
            # size = lv.point_t()
            # lv.txt_get_size(size, title, font.Bold.SCS38, 0, 0, lv.COORD.MAX, lv.TEXT_FLAG.EXPAND)
            # log.debug(__name__, f"width of title string is: {size.x})")
            self.title.set_text(title)
            if icon:
                self.title.set_icon(icon)

    return Titled

def with_buttons(cls: Type[S], right: str, left: str|None = None) -> Type[ButtonsScreen]:

    from trezor.ui.component import HStack, VStack, Button
    class ButtonsScreen(cls):
        def __init__(self):
            super().__init__()
            self.btn_right = None
            self.btn_left = None

            self.create_content(HStack)
            self.content: HStack

            # make buttons at bottom
            self.content.reverse()
            self.content.set_style_pad_bottom(32, lv.PART.MAIN)

            # a container for buttons
            container = self.add(VStack)
            container.reverse()
            container.set_size(lv.pct(100), lv.SIZE.CONTENT)
            if not left:
                container.set_style_flex_main_place(lv.FLEX_ALIGN.END, lv.PART.MAIN)
            else:
                container.set_style_flex_main_place(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.PART.MAIN)

            container.set_style_pad_all(0, lv.PART.MAIN)
            container.set_style_pad_left(32, lv.PART.MAIN)
            container.set_style_pad_right(32, lv.PART.MAIN)

            self.btn_right = container.add(Button)
            self.btn_right.set_text(right)

            if left:
                self.btn_left = container.add(Button)
                self.btn_left.set_text(left)

            # `content` is remained, for draw all other ui components
            self.create_content(lv.obj)
            self.content.set_flex_grow(1)

    return ButtonsScreen

def with_title_and_buttons(cls: Type[S], right: str, left: str|None = None) -> Type[ButtonsTitledScreen]:
    return with_title(with_buttons(cls, right, left))
