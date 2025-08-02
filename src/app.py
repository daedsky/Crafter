import flet as ft
from views.home_view import HomeView
from models.app_info import AppInfo
import flet_permission_handler as fph
from components.custom_controls import InfoAlertDialog
import sys
from components.perms_manager import StoragePermsManager
from components import admob


class CrafterApp:
    def __init__(self, page: ft.Page, debug: bool = False):
        self.debug: bool = debug
        self.page: ft.Page = page
        self.file_picker: ft.FilePicker = ft.FilePicker()
        self.perms_handler: fph.PermissionHandler = fph.PermissionHandler()
        self.home_view: HomeView = HomeView(app=self, route='/')
        self.load_preferences()
        self.interstitial_ad = None
        self.last_int_ad_show_time = None
        self.setup_ads()

    def load_preferences(self) -> None:
        client_storage = self.page.client_storage
        if client_storage.contains_key(AppInfo.THEME_MODE_KEY):
            mode: str = client_storage.get(AppInfo.THEME_MODE_KEY)
            self.page.theme_mode = ft.ThemeMode(mode)
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT

        if client_storage.contains_key(AppInfo.THEME_COLOR_KEY):
            color = client_storage.get(AppInfo.THEME_COLOR_KEY)
            self.page.theme = ft.Theme(color_scheme_seed=color)
            self.page.dark_theme = ft.Theme(color_scheme_seed=color)
        else:
            self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.PURPLE_400)
            self.page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.PURPLE_400)

        self.page.update()

    def show_disclaimer_if_not_accepted(self):
        if self.page.client_storage.get(AppInfo.LICENSE_AGREED_KEY) is True:
            self.page.go('/')
            return

        disclaimer_text = ft.Text(
            spans=[
                ft.TextSpan('''This app is provided "as-is" without any warranties or guarantees. 
The developer is not responsible for any damage to your device or data that may occur from using this app. 
By continuing to use this app, you acknowledge and accept this disclaimer.
This app is open-source and licensed under the MIT License. 
You can view the source code and license details at '''),
                ft.TextSpan('git repo', style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                            url=AppInfo.GIT_REPO_URL)
            ])

        dialog = InfoAlertDialog(self.page, content_text='', title_text='Disclaimer')

        def continue_app():
            self.page.close(dialog)
            self.page.client_storage.set(AppInfo.LICENSE_AGREED_KEY, True)
            StoragePermsManager(app=self).check_ask_and_req_storage_perms()
            self.page.go('/')

        def close_app():
            if self.page.platform != ft.PagePlatform.ANDROID:
                self.page.window.close()
                return
            sys.exit(0)

        dialog.content = disclaimer_text
        dialog.actions = [
            ft.OutlinedButton('Exit', on_click=lambda _: close_app()),
            ft.OutlinedButton('Continue', on_click=lambda _: continue_app()),
        ]

        dialog.show()

    def setup_ads(self) -> None:
        if self.page.platform != ft.PagePlatform.ANDROID: return
        self.interstitial_ad = admob.get_new_interstitial_ad(app=self)
        self.page.overlay.append(self.interstitial_ad)
