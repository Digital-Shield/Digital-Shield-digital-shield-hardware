import lvgl as lv
from storage import device
from . import manager
from trezor.ui import Style, font, i18n
from trezor import loop, log
from trezor.ui import Style, events, theme, colors
from trezor.ui.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from trezor.ui.component import Title, Button, HStack, VStack

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
        self.set_style_bg_img_src("A:/res/wallpapers/4.png", 0)  # 使用默认背景
        # wallpaper = device.get_homescreen()
        # if wallpaper:  # 判断 `wallpaper` 是否存在
        #     self.set_style_bg_img_src(wallpaper, 0)
        # else:
        #     self.set_style_bg_img_src("A:/res/background_six.png", 0)  # 使用默认背景
        # maybe speedup if not use background image
        # if __USE_BACKGROUND_IMAGE__:
        #     self.set_style_bg_img_src("A:/res/background_six.png", lv.PART.MAIN)

        # an empty content view, this is the root of `all` user UI components
        # almost all
        # default content is self
        self._content: lv.obj = self

        # lazy initialize components
        self._title: Title|None = None
        self._btn_container: VStack|None = None
        self._btn_right: Button|None = None
        self._btn_left: Button|None = None

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

    @property
    def title(self) -> Title:
        if not self._title:
            # use HStack as content ot manager title and remaining content
            self.create_content(HStack)
            self.content: HStack

            # add title
            self._title = self.add(Title)
            # self.title.set_style_text_font(font.Bold.SCS26, 0)
            # `content` is remained, for draw all other ui components
            self.create_content(lv.obj)
            self.content.set_flex_grow(1)

        return self._title

    @property
    def btn_right(self) -> Button:
        if not self._btn_container:
            self._create_btn_container()

        if not self._btn_right:
            if not self._btn_left:
                # only `right` button
                # add `right` first
                self._btn_container.reverse()
                self._btn_container.set_style_flex_main_place(lv.FLEX_ALIGN.END, lv.PART.MAIN)
            else:
                self._btn_container.set_style_flex_main_place(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.PART.MAIN)
            self._btn_right = self._btn_container.add(Button)

            # Remove the white shadow by setting the shadow width to 0
            self._btn_right.set_style_shadow_width(0, lv.PART.MAIN)
            self._btn_right.set_style_shadow_opa(lv.OPA.TRANSP, lv.PART.MAIN)
            #判断是否阿拉伯语
            cur_language = i18n.using.code if i18n.using is not None else None
            if cur_language == "al":
                #增大self._btn_right的宽度
                # print("阿拉伯语,宽度是--"+str(self._btn_right.get_style_width(lv.PART.MAIN)))
                self._btn_right.set_style_width(180, lv.PART.MAIN)

        return self._btn_right

    @property
    def btn_left(self) -> Button:
        if not self._btn_container:
            self._create_btn_container()

        if not self._btn_left:
            if not self._btn_right:
                # only `left` button
                # add `left` first
                self._btn_container.set_style_flex_main_place(lv.FLEX_ALIGN.START, lv.PART.MAIN)
            else:
                self._btn_container.set_style_flex_main_place(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.PART.MAIN)
            self._btn_left = self._btn_container.add(Button)

            # Remove the white shadow by setting the shadow width to 0
            self._btn_left.set_style_shadow_width(0, lv.PART.MAIN)
            self._btn_left.set_style_shadow_opa(lv.OPA.TRANSP, lv.PART.MAIN)
            
        return self._btn_left

    def _create_btn_container(self):
        self.create_content(HStack)
        self.content: HStack

        # make buttons at bottom
        self.content.reverse()
        self.content.set_style_pad_bottom(32, lv.PART.MAIN)

        # a container for buttons
        self._btn_container = self.add(VStack)

        # `content` is remained, for draw all other ui components
        self.create_content(lv.obj)
        self.content.set_flex_grow(1)

        self._btn_container.set_size(lv.pct(100), lv.SIZE.CONTENT)
        self._btn_container.set_style_pad_all(0, lv.PART.MAIN)
        self._btn_container.set_style_pad_left(32, lv.PART.MAIN)
        self._btn_container.set_style_pad_right(32, lv.PART.MAIN)


    # component manager
    def add(self, cls: Type[Widget]) -> Widget:
        """
        Add a `Widget` to the `content`
        """
        return cls(self.content)

    def set_title(self, title:str, icon:str|None = None):
        self.title.set(title, icon)

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
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色
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
        nav.set_zoom(350)  # 设置缩放比例，256表示原始大小，512表示放大2倍
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
