import flet as ft
from components import custom_controls as cc
from controllers import click_handler as ch
from controllers import event_handler as ev
from components import admob

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import CrafterApp


# type hinting <end>

class CraftLayout(ft.Column):
    def __init__(self, app: 'CrafterApp', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app: 'CrafterApp' = app
        self.page: ft.Page = app.page
        self.gif_files_count: int = 0
        self.dest_folder_path: str | None = None

        # ui elements block <start>
        self.reorderable_gif_listview: ft.ReorderableListView = ft.ReorderableListView(
            on_reorder=lambda x: ev.on_gif_listview_reorder(craft_layout=self, e=x), expand=True)
        self.listile_dest_path: ft.ListTile = cc.ListTilePickedItem(title='DESTINATION FOLDER',
                                                                    subtitle='*No Folder Selected*')

        tf_kwargs: dict = dict(expand=True, border_color=ft.Colors.ERROR, height=65,
                               label_style=ft.TextStyle(color=ft.Colors.ERROR),
                               field_type=cc.NumsTextFieldType.NonZeroAndNoLeadingZeros, helper_text='*required',
                               helper_style=ft.TextStyle(color=ft.Colors.ERROR, size=7.5))
        self.textfield_width: ft.TextField = cc.NumbersOnlyTextField(label='Width', hint_text="eg: 500", max_length=4,
                                                                     **tf_kwargs)
        self.textfield_height: ft.TextField = cc.NumbersOnlyTextField(label='Height', hint_text="eg: 500", max_length=4,
                                                                      **tf_kwargs)
        self.textfield_fps: ft.TextField = cc.NumbersOnlyTextField(label='FPS', hint_text="eg: 30", max_length=2,
                                                                   **tf_kwargs)

        self.container_fileslist: ft.Container = ft.Container()
        self.btn_generate = cc.FilledButton('Craft', icon=ft.Icons.AUTO_AWESOME_OUTLINED,
                                            expand=True,
                                            on_click=lambda x: ch.craft_bootanimation(
                                                craft_layout=self,
                                                e=x))
        # ui elements block <end>

        self.controls = self.get_layout()

    def get_layout(self) -> list[ft.Control]:
        LABEL_FILE_SELECTION = cc.HeaderText('File Selection', expand=True)
        btn_clear_all = ft.FilledTonalButton('Clear All', color=ft.Colors.PRIMARY,
                                             on_click=lambda x: ch.reload_homeview_control_layout(
                                                 home_view=self.app.home_view, nav_index=0, e=x))

        btn_pick_files = cc.FilledButton('PICK FILES', ft.Icons.FILE_UPLOAD,
                                         on_click=lambda x: ch.pick_gif_files(craft_layout=self, e=x))

        btn_select_folder = cc.FilledButton('SELECT DESTINATION FOLDER', icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                                            on_click=lambda x: ch.select_dest_folder(craft_layout=self, e=x))

        label_settings = cc.HeaderText('Settings')

        label_selected_files = cc.HeaderText('Selected Files')

        self.container_fileslist.content = ft.Text('*No Files Selected*', color=ft.Colors.ERROR,
                                                   weight=ft.FontWeight.BOLD, italic=True)

        structure = [ft.Row([LABEL_FILE_SELECTION, btn_clear_all]),
                     btn_pick_files,
                     btn_select_folder,
                     ft.Container(content=self.listile_dest_path, border=ft.border.only(left=ft.BorderSide(3)),
                                  border_radius=5),
                     label_settings,
                     ft.Row([self.textfield_width, self.textfield_height, self.textfield_fps]),
                     label_selected_files,
                     self.container_fileslist,
                     ft.Row([self.btn_generate])]

        if self.page.platform == ft.PagePlatform.ANDROID:
            structure.insert(4, admob.get_new_banner_ad())
            structure.append(admob.get_new_banner_ad())

        return structure
