import flet as ft
from controllers.event_handler import (on_result_gifs_picked, on_result_dest_folder_selected,
                                       on_result_bootanim_zip_picked)

from controllers import craft_handler
from controllers import install_handler
import subprocess
from models.app_info import AppInfo
import os
from components.custom_controls import InfoAlertDialog, ErrorAlertDialog
from components.perms_manager import StoragePermsManager
import flet_permission_handler as fph
from components import admob

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.craft_layout import CraftLayout
    from views.install_layout import InstallLayout
    from views.home_view import HomeView
    from views.settings_view import SettingsLayout


# type hinting <end>

def pick_gif_files(*, craft_layout: 'CraftLayout', e):
    craft_layout.app.file_picker.on_result = lambda x: on_result_gifs_picked(craft_layout, x)
    craft_layout.app.file_picker.pick_files(dialog_title='Pick GIF Files',
                                            allowed_extensions=['gif'],
                                            allow_multiple=True)


def select_dest_folder(*, craft_layout: 'CraftLayout', e):
    def func():
        craft_layout.app.file_picker.on_result = lambda x: on_result_dest_folder_selected(craft_layout, x)
        craft_layout.app.file_picker.get_directory_path(dialog_title='Select Destination Folder')

    StoragePermsManager(app=craft_layout.app).check_ask_and_req_storage_perms(after_dialog_close_func=func)


def pick_bootanimation_zip_file(*, install_layout: 'InstallLayout', e):
    install_layout.app.file_picker.on_result = lambda x: on_result_bootanim_zip_picked(install_layout, e=x)
    install_layout.app.file_picker.pick_files(dialog_title='Pick bootanimation file',
                                              allowed_extensions=['zip'],
                                              allow_multiple=False)


@admob.show_interstitial_ad
def reload_homeview_control_layout(*, home_view: 'HomeView', nav_index: int, e):
    if nav_index == 0:
        home_view.craft_layout = home_view.get_new_craft_layout()
        home_view.controls = [home_view.craft_layout]
    elif nav_index == 1:
        home_view.install_layout = home_view.get_new_install_layout()
        home_view.controls = [home_view.install_layout]
    home_view.update()


@admob.show_interstitial_ad
def craft_bootanimation(*, craft_layout: 'CraftLayout', e):
    craft_handler.start_craft(craft_layout=craft_layout)


@admob.show_interstitial_ad
def install_bootanimation(*, install_layout: 'InstallLayout', e):
    install_handler.install(install_layout=install_layout)


def toggle_theme_mode(*, home_view: 'HomeView', e):
    if home_view.page.theme_mode == ft.ThemeMode.LIGHT:
        home_view.page.theme_mode = ft.ThemeMode.DARK

    elif home_view.page.theme_mode == ft.ThemeMode.DARK:
        home_view.page.theme_mode = ft.ThemeMode.LIGHT

    elif home_view.page.theme_mode == ft.ThemeMode.SYSTEM:
        if home_view.page.platform_brightness == ft.Brightness.LIGHT:
            home_view.page.theme_mode = ft.ThemeMode.DARK
        elif home_view.page.platform_brightness == ft.Brightness.DARK:
            home_view.page.theme_mode = ft.ThemeMode.LIGHT

    home_view.page.update()
    home_view.page.client_storage.set(key=AppInfo.THEME_MODE_KEY, value=home_view.page.theme_mode.value)


@admob.show_interstitial_ad
def goto_about_page(*, home_view: 'HomeView', e):
    home_view.page.go('/about')


@admob.show_interstitial_ad
def goto_settings_page(*, home_view: 'HomeView', e):
    home_view.page.go('/settings')


@admob.show_interstitial_ad
def goto_help_page(*, home_view: 'HomeView', e):
    home_view.page.go('/help')


def change_theme_mode(*, settings_layout: 'SettingsLayout', e):
    if e.control.value == 'Light':
        settings_layout.page.theme_mode = ft.ThemeMode.LIGHT
    elif e.control.value == 'Dark':
        settings_layout.page.theme_mode = ft.ThemeMode.DARK
    elif e.control.value == 'System':
        settings_layout.page.theme_mode = ft.ThemeMode.SYSTEM
    settings_layout.page.update()
    settings_layout.page.client_storage.set(key=AppInfo.THEME_MODE_KEY, value=settings_layout.page.theme_mode.value)


def change_theme_color(*, settings_layout: 'SettingsLayout', color: ft.Colors, e):
    settings_layout.page.theme = ft.Theme(color_scheme_seed=color)
    settings_layout.page.dark_theme = ft.Theme(color_scheme_seed=color)
    settings_layout.page.update()
    settings_layout.page.client_storage.set(key=AppInfo.THEME_COLOR_KEY, value=color)


def check_root_access(*, settings_layout: 'SettingsLayout', listile: ft.ListTile, e):
    if settings_layout.page.platform == ft.PagePlatform.ANDROID:
        process = subprocess.run('su -c echo hello'.split(), capture_output=True, text=True)
    else:
        process = subprocess.run('pkexec echo hello'.split(), capture_output=True, text=True)

    if process.returncode == 0:
        listile.subtitle.value = 'Rooted'
        listile.subtitle.color = ft.Colors.GREEN
    else:
        listile.subtitle.value = f'{process.stderr}'
        listile.subtitle.color = ft.Colors.RED
    listile.update()


def show_console_log(*, home_view: 'HomeView', e):
    fp = os.getenv('FLET_APP_CONSOLE')
    if fp is None: ErrorAlertDialog(page=home_view.page, content='File "console.log" not found').show(); return
    with open(fp, 'r') as f:
        log = f.read()
    InfoAlertDialog(page=home_view.app.page, content_text=log, title_text='console log').show()


def clear_console_log(*, home_view: 'HomeView', e):
    fp = os.getenv('FLET_APP_CONSOLE')
    if fp is None: ErrorAlertDialog(page=home_view.page, content='File "console.log" not found').show(); return

    confirm_dlg = InfoAlertDialog(home_view.app.page, content_text='Are you sure you want to clear console.log file?',
                                  title_text='clear console log')

    def clear_file_and_close():
        with open(fp, 'w') as f:
            f.write('')
        home_view.page.close(confirm_dlg)

    confirm_dlg.actions = [
        ft.TextButton(text='Cancel', on_click=lambda _: home_view.page.close(confirm_dlg)),
        ft.TextButton(text='Confirm', on_click=lambda _: clear_file_and_close()),
    ]
    confirm_dlg.show()


def goto_storage_perms_settings(*, settings_layout: 'SettingsLayout', storage_manager: 'StoragePermsManager',
                                listile_perm_status: ft.ListTile, e):
    if settings_layout.page.platform != ft.PagePlatform.ANDROID: return
    status = storage_manager.request_storage_perms()
    listile_perm_status.subtitle.value = status.value
    if status == fph.PermissionStatus.GRANTED:
        listile_perm_status.subtitle.color = ft.Colors.GREEN
    else:
        listile_perm_status.subtitle.color = ft.Colors.RED
    listile_perm_status.update()
