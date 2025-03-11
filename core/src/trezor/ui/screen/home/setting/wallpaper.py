import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from storage import device, io
from trezor import utils
from trezor.ui.screen import Navigation, with_title
from trezor.ui.component import VStack

if TYPE_CHECKING:
    from typing import Generator, List
    pass

class Wallpaper(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.wallpaper, "A:/res/wallpaper-two.png")

        # right-arrow
        self.arrow = lv.label(self)
        self.arrow.set_text(lv.SYMBOL.RIGHT)
        self.arrow.set_style_text_color(colors.DS.GRAY, lv.PART.MAIN)

    def action(self):
        from trezor import workflow
        workflow.spawn(WallpaperDetail().show())

class WallpaperImage(lv.img):
    def __init__(self, parent):
        super().__init__(parent)

    def set_src(self, src : 'ImageSource'):
        super().set_src(src.thumbnail())
        self.src = src

class ImageSource:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def thumbnail(self) -> str:
        return f"A:{self.path}/thumbnail/{self.name}"

    def source(self) -> str:
        return f"A:{self.path}/{self.name}"

class WallpaperDetail(with_title(Navigation)):
    def __init__(self):
        super().__init__()
        self.set_title(i18n.Setting.wallpaper)

        self.create_content(VStack)
        self.content: VStack
        self.content.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.content.add_style(
            Style()
            .flex_main_place(lv.FLEX_ALIGN.SPACE_EVENLY)
            .width(480 - 32)
            .height(800 - 200),
            0
        )
        self.images: List[WallpaperImage] = []
        for w in self.wallpapers():

            log.debug(__name__, f"wallpaper: {w.source()}")
            log.debug(__name__, f"thumbnail wallpaper: {w.thumbnail()}")
            img = WallpaperImage(self.content)
            img.set_src(w)
            img.set_style_border_width(2, lv.PART.MAIN|lv.STATE.FOCUSED)
            img.set_style_border_color(colors.DS.PRIMARY, lv.PART.MAIN|lv.STATE.FOCUSED)
            img.add_flag(lv.obj.FLAG.CLICKABLE)
            self.images.append(img)

        self.group = lv.group_create()
        for img in self.images:
            self.group.add_obj(img)

        # find the current and set focus
        current = self.current()
        item = utils.first(self.images, lambda item: item.src.source() == current)
        lv.group_focus_obj(item)

        self.group.set_focus_cb(self.on_group_focus_changed)

    def on_deleting(self):
        super().on_deleting()
        # 如果一个对象在group，在screen删除的时候，会发送DEFOCUSED消息
        # 这会导致已经删除的对象去响应消息，出现crash问题
        # 所以在页面消失的时候，删除掉group，规避掉问题
        self.group._del()

    def on_group_focus_changed(self, group: lv._group_t):
        obj = group.get_focused()
        item = utils.first(self.images, lambda item: item == obj)
        log.debug(__name__, f"user clicked: {item.src.thumbnail()}")
        self.save_option(item.src.source())

    def current(self) -> str:
        return device.get_homescreen()

    def save_option(self, option: str):
        device.set_homescreen(option)
        from trezor.ui.screen import manager
        from trezor.ui import events
        manager.publish(events.WALLPAPER_CHANGED)

    @staticmethod
    def wallpapers() -> Generator[ImageSource]:

        SYS_WALLPAPER_PATH = "0:/res/wallpapers"
        # internal wallpapers
        for _, _, name in io.fatfs.listdir(SYS_WALLPAPER_PATH):
            source = ImageSource("0:/res/wallpapers", name)
            try :
                path = f"{SYS_WALLPAPER_PATH}/thumbnail/{name}"
                size, _, _ = io.fatfs.stat(path)
                log.debug(__name__, f"{source.thumbnail()} : {size}")
                if size :
                    yield source
            except:
                continue

        USER_WALLPAPER_PATH = "1:/res/wallpapers"
        # user wallpapers
        for _, _, name in io.fatfs.listdir(USER_WALLPAPER_PATH):
            source = ImageSource("1:/res/wallpapers", name)
            try :
                path = f"{USER_WALLPAPER_PATH}/thumbnail/{name}"
                size, _, _ = io.fatfs.stat(path)
                log.debug(__name__, f"{source.thumbnail()} : {size}")
                if size :
                    yield source
            except:
                continue
