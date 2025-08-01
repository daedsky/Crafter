import flet as ft
from components import custom_controls as cc
from controllers import click_handler as ch
from utils import extras
import subprocess
from controllers import event_handler as ev
from components import admob

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import CrafterApp


# type hinting <end>

class InstallLayout(ft.Column):
    def __init__(self, app: 'CrafterApp', *args, **kwargs):
        super().__init__(*args, **kwargs, scroll=ft.ScrollMode.AUTO)
        self.app: 'CrafterApp' = app
        self.page: ft.Page = app.page
        self.picked_zip_file_fp: str | None = None
        self.default_bootanim_zip_exists, self.default_bootanimation_fp = extras.get_installation_filepath(
            self.page.platform)
        self.get_set_props()

        # ui <start>
        self.listile_picked_zip_file = cc.ListTilePickedItem(title='PICKED FILE', subtitle='*No File Selected*')
        self.textfield_install_location = ft.TextField(value=self.default_bootanimation_fp, disabled=True, filled=True,
                                                       label='Install Location', border_color=ft.Colors.OUTLINE)
        self.btn_install = cc.FilledButton('Install', icon=ft.Icons.INSTALL_MOBILE_OUTLINED, expand=True,
                                           on_click=lambda x: ch.install_bootanimation(install_layout=self, e=x))
        # ui <end>

        self.controls: list[ft.Control] = self.layout()

    def get_set_props(self):
        if self.page.platform == ft.PagePlatform.ANDROID:
            from jnius import autoclass
            Version = autoclass('android.os.Build$VERSION')

            self.android_version = Version.RELEASE
            self.android_sdk_version = Version.SDK_INT
            su_path = subprocess.run('which su'.split(), capture_output=True, text=True).stdout
            self.su_status = f'Detected' if su_path else 'Not Detected!'
        else:
            self.android_version = 'version'
            self.android_sdk_version = 'manufacturer'
            self.su_status = 'root status'

    @staticmethod
    def info_field(title, subtitle) -> ft.Column:
        return ft.Column(controls=[ft.Text(value=title, size=14, weight=ft.FontWeight.W_400),
                                   ft.Text(value=subtitle, size=16, weight=ft.FontWeight.W_500)],
                         expand=True, tight=True, spacing=0)

    def layout(self):
        label_file_selection = cc.HeaderText('File Selection', expand=True)
        btn_clear_all = ft.FilledTonalButton('Clear All', color=ft.Colors.PRIMARY,
                                             on_click=lambda x: ch.reload_homeview_control_layout(
                                                 home_view=self.app.home_view, nav_index=1, e=x))

        btn_select_file = cc.FilledButton('Select File', ft.Icons.FILE_UPLOAD,
                                          on_click=lambda x: ch.pick_bootanimation_zip_file(install_layout=self, e=x))

        label_settings = cc.HeaderText('Settings')

        dropdown_options = [ft.DropdownOption('Default'),
                            ft.DropdownOption(r'/system/media/bootanimation.zip'),
                            ft.DropdownOption(r'/product/media/bootanimation.zip'),
                            ft.DropdownOption(r'/oem/media/bootanimation.zip'),
                            ft.DropdownOption(r'/vendor/etc/bootanimation.zip'),
                            ft.DropdownOption(r'/data/local/bootanimation.zip'),
                            ft.DropdownOption('Custom')]

        dropdown = ft.Dropdown('Default', options=dropdown_options, border_color=ft.Colors.OUTLINE, filled=True,
                               label='Install Location', expand=True,
                               on_change=lambda x: ev.on_change_install_fp_dropdown(install_layout=self, e=x))

        label_device_info = cc.HeaderText('Device Info')

        col_platform_name = self.info_field(title='Platform', subtitle=self.page.platform.name)
        col_android_version = self.info_field(title='Android Version', subtitle=self.android_version)
        col_sdk_version = self.info_field(title='SDK Version', subtitle=self.android_sdk_version)
        col_su_path = self.info_field(title='Root', subtitle=self.su_status)

        device_info_container = ft.Container(
            content=ft.Column(controls=[ft.Row([col_platform_name, col_android_version]),
                                        ft.Row([col_sdk_version, col_su_path]),
                                        ],
                              spacing=10
                              ),
            padding=5, margin=0, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=8
        )

        structure = [ft.Row([label_file_selection, btn_clear_all]),
                     btn_select_file,
                     ft.Container(self.listile_picked_zip_file, border=ft.border.only(left=ft.BorderSide(3)),
                                  border_radius=5),
                     label_settings,
                     dropdown,
                     self.textfield_install_location,
                     label_device_info,
                     device_info_container,
                     ft.Row([self.btn_install])]
        if self.page.platform == ft.PagePlatform.ANDROID:
            structure.insert(3, admob.get_new_banner_ad())
            structure.append(admob.get_new_banner_ad())

        return structure
