import flet as ft
from views.home_view import HomeView
from models.app_info import AppInfo
from components import admob


class CrafterApp:
    def __init__(self, page: ft.Page):
        self.APP_VERSION = "0.0.1-dev"
        self.page: ft.Page = page
        self.file_picker: ft.FilePicker = ft.FilePicker()
        self.home_view: HomeView = HomeView(app=self, route='/')
        self.load_preferences()
        self.interstitial_ad = None
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

    def setup_ads(self) -> None:
        if self.page.platform != ft.PagePlatform.ANDROID: return
        self.interstitial_ad = admob.get_new_interstitial_ad(app=self)
        self.page.overlay.append(self.interstitial_ad)
