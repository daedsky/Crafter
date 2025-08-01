import flet as ft
from components import custom_controls as cc
from controllers import click_handler as ch
from components import admob
from components.perms_manager import StoragePermsManager
import flet_permission_handler as fph

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import CrafterApp


# type hinting <end>


class SettingsLayout(ft.Column):
    def __init__(self, app: 'CrafterApp', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app: 'CrafterApp' = app
        self.page: ft.Page = app.page
        self.controls = self.layout()

    def layout(self) -> list[ft.Control]:
        LABEL_APPEARANCE = cc.HeaderText('Appearance')
        listile_theme_mode = ft.ListTile(
            title=ft.Text('Theme mode'),
            subtitle=ft.Text('Choose between light, dark, or system theme'),
            trailing=ft.Dropdown(value=self.page.theme_mode.name.capitalize(),
                                 options=[ft.DropdownOption('Light'), ft.DropdownOption('Dark'),
                                          ft.DropdownOption('System')],
                                 on_change=lambda x: ch.change_theme_mode(settings_layout=self, e=x),
                                 border_color=ft.Colors.OUTLINE),
            content_padding=0
        )
        fav_icon = ft.Icons.FAVORITE_ROUNDED
        listile_theme_color = ft.ListTile(
            title=ft.Text('Theme color'),
            subtitle=ft.Text('Choose your preferred accent color'),
            trailing=ft.Row(
                controls=[ft.IconButton(fav_icon, icon_color=ft.Colors.PINK_300,
                                        on_click=lambda x: ch.change_theme_color(settings_layout=self,
                                                                                 color=ft.Colors.PINK_300, e=x)),
                          ft.IconButton(fav_icon, icon_color=ft.Colors.YELLOW_400,
                                        on_click=lambda x: ch.change_theme_color(settings_layout=self,
                                                                                 color=ft.Colors.YELLOW_400, e=x)),
                          ft.IconButton(fav_icon, icon_color=ft.Colors.PURPLE_400,
                                        on_click=lambda x: ch.change_theme_color(settings_layout=self,
                                                                                 color=ft.Colors.PURPLE_400, e=x)),
                          ft.IconButton(fav_icon, icon_color=ft.Colors.GREEN_400,
                                        on_click=lambda x: ch.change_theme_color(settings_layout=self,
                                                                                 color=ft.Colors.GREEN_400, e=x))],
                wrap=True),
            content_padding=0
        )
        LABEL_ADVANCE = cc.HeaderText('Advance Settings')
        listile_check_root = ft.ListTile(title=ft.Text('Root Status'),
                                         subtitle=ft.Text('Unknown'),
                                         trailing=cc.FilledButton('Check'),
                                         content_padding=0)
        listile_check_root.trailing.on_click = lambda x: ch.check_root_access(settings_layout=self,
                                                                              listile=listile_check_root, e=x)
        storage_manager = StoragePermsManager(app=self.app)
        storage_perm_status = storage_manager.only_check_storage_perms()
        listile_storage_perms = ft.ListTile(title=ft.Text('Grant Storage Permission'),
                                            subtitle=ft.Text(
                                                f'{storage_perm_status.value}'),
                                            trailing=cc.FilledButton('Grant'),
                                            content_padding=0)
        if storage_perm_status == fph.PermissionStatus.GRANTED:
            listile_storage_perms.subtitle.color = ft.Colors.GREEN
        else:
            listile_storage_perms.subtitle.color = ft.Colors.RED
        listile_storage_perms.trailing.on_click = lambda x: ch.goto_storage_perms_settings(
            settings_layout=self, storage_manager=storage_manager, listile_perm_status=listile_storage_perms, e=x
        )
        structure = [
            LABEL_APPEARANCE,
            listile_theme_mode,
            listile_theme_color,
            LABEL_ADVANCE,
            listile_check_root,
            listile_storage_perms
        ]

        if self.page.platform == ft.PagePlatform.ANDROID:
            structure.append(admob.get_new_banner_ad())
            structure.append(admob.get_new_banner_ad())

        return structure


class SettingsView(ft.View):
    def __init__(self, app: 'CrafterApp', *args, **kwargs):
        super().__init__(*args, **kwargs, scroll=ft.ScrollMode.AUTO)
        self.app: 'CrafterApp' = app
        self.page: ft.Page = app.page
        self.appbar: ft.AppBar = cc.ReturnHomeAppBar(title_text='Settings')
        self.controls: list[ft.Control] = [SettingsLayout(app=self.app)]
