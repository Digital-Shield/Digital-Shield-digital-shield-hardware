import lvgl as lv
import math
import ujson as json
from storage import device
from trezor.ui import i18n, Style, theme, colors
from trezor.ui.component import HStack, VStack, LabeledText
from trezor.ui.screen import Navigation, with_title
from trezor import io, loop, uart, utils, workflow, log

class NftApp(with_title(Navigation)):
    def __init__(self):
        super().__init__()
        # self.set_title(i18n.App.nft)
        self.set_style_bg_img_src(None, lv.PART.MAIN)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)  # 让背景可见
        self.set_style_bg_color(lv.color_hex(0x0D0D17), lv.PART.MAIN)# 设置背景颜色

        title_label = lv.label(self)
        title_label.set_text(i18n.App.nft)
        title_label.align(lv.ALIGN.TOP_MID, 0, 10)  # 让标题居中
        title_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)

        # use HStack as content
        self.create_content(HStack)
        self.content: HStack
        self.content.set_style_pad_left(16, lv.PART.MAIN)
        self.content.set_style_pad_right(16, lv.PART.MAIN)
        self.content.set_style_pad_top(15, lv.PART.MAIN)  # 设置顶部填充
        # self.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        nft_counts = 0
        file_name_list = []
        for size, _, name in io.fatfs.listdir("1:/res/nfts/zooms"):
            print(f"Name: {name}, Size: {size} bytes")
            if size > 0:
                nft_counts += 1
                file_name_list.append(name)

        if not utils.EMULATOR:
            file_name_list.sort(
                key=lambda name: int(
                    name[5:].split("-")[-1][: -(len(name.split(".")[1]) + 1)]
                )
            )
        rows_num = math.ceil(nft_counts / 2)
        row_dsc = [224] * rows_num
        row_dsc.append(lv.GRID_TEMPLATE.LAST)
        # 2 columns
        col_dsc = [
            224,
            224,
            lv.GRID_TEMPLATE.LAST,
        ]
        grid = lv.obj(self)
        grid.align_to(self.content, lv.ALIGN.TOP_LEFT, 0, 0)
        grid.set_size(448, 700)
        grid.set_layout(lv.LAYOUT_GRID.value)
        grid.add_style(
            Style()
            .radius(0)
            .bg_color(lv.color_hex(0x0D0D17))  # 深色背景
            # .pad_right(16)
            # .pad_left(16)
            .border_width(0)
            .grid_column_dsc_array(col_dsc)
            .grid_row_dsc_array(row_dsc),
            0,
        )
        grid.set_grid_align(lv.GRID_ALIGN.SPACE_AROUND, lv.GRID_ALIGN.START)

        for i, file_name in enumerate(file_name_list):
            path_dir = "A:1:/res/nfts/zooms/"
            ImgGridItem(grid,file_name,path_dir,(i) % 2,(i) // 2)

class ImgGridItem(lv.img):
    """Img Grid Item"""
    def __init__(
        self,
        parent,
        file_name: str,
        path_dir: str,
        col_num,
        row_num
        # img_path_other: str = "A:/res/checked-solid.png",
        # is_internal: bool = False,
    ):
        super().__init__(parent)
        self.set_grid_cell(
            lv.GRID_ALIGN.CENTER, col_num, 1, lv.GRID_ALIGN.CENTER, row_num, 1
        )
        self.file_name = file_name
        self.zoom_path = path_dir + file_name
        self.set_src(self.zoom_path)
        self.set_size(224, 224)
        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(lambda _: self.action(), lv.EVENT.CLICKED, None)
    def action(self):
        log.debug(__name__, self.file_name)
        if utils.lcd_resume():
            return
        file_name_without_ext = self.file_name.split(".")[0][5:]
        print(file_name_without_ext)
        desc_file_path = f"1:/res/nfts/desc/{file_name_without_ext}.json"
        metadata = {
            "header": "",
            "subheader": "",
            "network": "",
            "owner": "",
        }
        with io.fatfs.open(desc_file_path, "r") as f:
            description = bytearray(2048)
            n = f.read(description)
            if 0 < n < 2048:
                try:
                    metadata_load = json.loads(
                        (description[:n]).decode("utf-8")
                    )
                except BaseException as e:
                    if __debug__:
                        print(f"Invalid json {e}")
                else:
                    if all(
                        key in metadata_load.keys()
                        for key in metadata.keys()
                    ):
                        metadata = metadata_load
        print(metadata)
        workflow.spawn(ImgDetail(self.file_name,"A:1:/res/nfts/zooms/",metadata).show())

class ImgDetail(with_title(Navigation)):
    """Img Item"""
    def __init__(
        self,
        file_name: str,
        path_dir: str,
        nft_metadata
    ):
        super().__init__()
        self.set_title(nft_metadata["header"])
        self.create_content(HStack)
        self.content: HStack
        self.content.add_style(
            Style().pad_left(16).pad_right(16),
            0
        )
        contaner = self.add(lv.obj)
        contaner.add_style(
            theme.Styles.container,
            0
        )
        contaner.set_height(lv.SIZE.CONTENT)
        contaner.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)

        self.img = lv.img(contaner)
        self.img.set_src(path_dir+file_name)
        self.img.set_zoom(256)
        self.img.center()

        view = self.add(Text)
        view.set_label(nft_metadata["header"])
        view.set_text(nft_metadata["subheader"])

class Text(LabeledText):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_style(
            Style()
            .border_width(0)
            .pad_top(0)
            .pad_bottom(0),
            0
        )
