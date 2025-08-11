import lvgl as lv
from typing import TYPE_CHECKING

from . import *
from storage import device, io
from trezor import utils
from trezor.ui.screen import Navigation
from trezor.ui.component import VStack
from trezor.ui.screen.message import Success
from trezor.ui import i18n, Cancel
from trezor.ui.screen.confirm import SimpleConfirm
from trezor import workflow

if TYPE_CHECKING:
    from typing import Generator, List
    pass

class Wallpaper(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Setting.wallpaper, "A:/res/wallpaper-new.png")
        #边框为0
        self.set_style_border_width(0, 0)
        # # right-arrow
        # self.arrow = lv.label(self)
        # self.arrow.set_text(lv.SYMBOL.RIGHT)
        # self.arrow.set_style_text_color(colors.DS.WHITE, lv.PART.MAIN)
        # arrow
        self.arrow = lv.img(self)
        #设置箭头背景图
        self.arrow.set_src("A:/res/a_right_arrow.png")
        #设置显示在最右边
        self.arrow.align(lv.ALIGN.OUT_RIGHT_MID, 0,0)

    def action(self):
        from trezor import workflow
        workflow.spawn(WallpaperDetail().show())

class WallpaperImage(lv.img):
    def __init__(self, parent):
        super().__init__(parent)
        # self.set_style_pad_all(10, lv.PART.MAIN)

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
    
from trezor.ui.screen.navaigate import Navigate
class WallpaperDetail(Navigate):
    def __init__(self):
        super().__init__()
         #隐藏左右按钮
        self.btn_cancel.add_flag(lv.obj.FLAG.HIDDEN)
        self.btn_confirm.add_flag(lv.obj.FLAG.HIDDEN)
        self.set_title(i18n.Setting.wallpaper)
        self.title.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)

        self.create_content(VStack)
        self.content: VStack
        self.content.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        # self.content.set_align_items(lv.ALIGN.CENTER)
        self.content.add_style(
            Style()
            .pad_all(25)
            .pad_left(35)
            .pad_column(45)
            .pad_row(20)
            .bg_color(lv.color_hex(0x111126))
            .bg_opa(lv.OPA.COVER)
            .width(lv.pct(100))  # 占满宽度
            .height(800-175),
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
            self.reverting = False
            # 添加点击事件回调
            img.add_event_cb(self.on_image_clicked, lv.EVENT.CLICKED, img)
            self.images.append(img)

        self.group = lv.group_create()
        for img in self.images:
            img.src.source().replace("0:", "")
            # print("add image to group", img.src.source())
            self.group.add_obj(img)

        # find the current and set focus
        current = self.current()
        item = utils.first(self.images, lambda item: item.src.source().replace("0:", "") == current.replace("0:", ""))
        lv.group_focus_obj(item)
        print("current wallpaper: ", current)
        # 在item的中心显示一张图片selected_icon.png
        self.selected_icon = lv.img(item)
        self.selected_icon.set_src("A:/res/selected_icon.png")
        self.selected_icon.align(lv.ALIGN.CENTER, 0, 0)
        
        # self.group.set_focus_cb(self.on_group_focus_changed)
    def on_image_clicked(self, event):
        # 获取被点击的图片对象
        img = event.get_target()
        item = utils.first(self.images, lambda item: item == img)
        log.debug(__name__, f"user clicked: {item.src.thumbnail()}")
        self.save_option(item.src.source())

    def on_deleting(self):
        super().on_deleting()
        # 如果一个对象在group，在screen删除的时候，会发送DEFOCUSED消息
        # 这会导致已经删除的对象去响应消息，出现crash问题
        # 所以在页面消失的时候，删除掉group，规避掉问题
        self.group._del()

    def on_group_focus_changed(self, group: lv._group_t):
        obj = group.get_focused()
        # item = utils.first(self.images, lambda item: item == obj)
        # log.debug(__name__, f"user clicked: {item.src.thumbnail()}")
        # self.save_option(item.src.source())

    def current(self) -> str:
        return device.get_homescreen()

    def save_option(self, option: str):
        
        workflow.spawn(self.do_confirm_save_option(option))
        
        # # 显示成功提示框
        # success_popup = Success(i18n.Title.operate_success, i18n.Title.theme_success)
        # workflow.spawn(success_popup.show())  #异步显示弹框

    async def do_confirm_save_option(self, option: str):
        from trezor.ui.screen.preview import Preview
        # 创建确认页面，设置背景为选中的壁纸
        screen = Preview(option)
        screen.set_title(i18n.Title.preview)
        # 设置背景透明
        # screen.set_style_bg_img_opa(lv.OPA.COVER, lv.PART.MAIN)
        
        #替换option中的0:为空
        option = option.replace("0:", "")
        print(f"set wallpaper: {option}")
        # screen.set_style_bg_img_src(option, lv.PART.MAIN)
        
        
        # # 确保内容透明
        # content_style = lv.style_t()
        # content_style.init()
        # content_style.set_bg_opa(lv.OPA.TRANSP)
        # content_style.set_bg_img_src(option)
        # screen.content.add_style(content_style, lv.PART.MAIN)
        # # # 让 content 占据全屏
        # screen.content.set_style_pad_all(0, lv.PART.MAIN)
        # screen.content.set_style_pad_top(-50, lv.PART.MAIN)
        # screen.content.set_style_pad_bottom(-50, lv.PART.MAIN)
        # screen.content.set_style_pad_row(0, lv.PART.MAIN)
        # screen.content.set_style_pad_column(0, lv.PART.MAIN)
        # screen.content.set_width(lv.pct(160))
        # screen.content.set_height(lv.pct(130))
        # screen.content.set_size(lv.pct(160), lv.pct(130))
        # screen.content.add_style(theme.Styles.board, lv.PART.MAIN)
    
        # 去掉中间文本
        # screen.label.set_text("")
        
        # screen.btn_confirm.set_text(i18n.Button.confirm)
        await screen.show()
        r = await screen
        if isinstance(r, Cancel):
            self.reverting = True
            return

        # `Continue`
        device.set_homescreen(option)
        print("set wallpaper--: ", option)
        item = utils.first(self.images, lambda item: item.src.source().replace("0:", "") == option)
        #先清除其中item中心的图片
        self.selected_icon.delete()
        # 在item的中心显示一张图片selected_icon.png
        self.selected_icon = lv.img(item)
        self.selected_icon.set_src("A:/res/selected_icon.png")
        self.selected_icon.align(lv.ALIGN.CENTER, 0, 0)
        self.selected_icon.set_ext_click_area(0)
        self.selected_icon.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.selected_icon.clear_flag(lv.obj.FLAG.CLICKABLE)
        from trezor.ui.screen import manager
        from trezor.ui import events
        manager.publish(events.WALLPAPER_CHANGED)
 
    def _is_background_visible(self, obj) -> bool:
        """检查背景是否可见的辅助方法"""
        try:
            # 检查背景不透明度
            opa = obj.get_style_bg_img_opa(lv.PART.MAIN)
            if opa == lv.OPA.TRANSP or opa == 0:
                return False
            
            # 检查是否有背景源
            src = obj.get_style_bg_img_src(lv.PART.MAIN)
            return src is not None and src != ""
        except:
            return False
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
