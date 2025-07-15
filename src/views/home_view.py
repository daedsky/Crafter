import flet as ft
from views.craft_layout import CraftLayout
from views.install_layout import InstallLayout
from controllers import event_handler as ev
from controllers import click_handler as ch

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import CrafterApp


# type hinting <end>

class HomeView(ft.View):
    def __init__(self, app: 'CrafterApp', *args, **kwargs):
        super().__init__(*args, **kwargs, scroll=ft.ScrollMode.AUTO)
        self.app: 'CrafterApp' = app
        self.page: ft.Page = app.page
        self.appbar: ft.AppBar = ft.AppBar(
            leading=ft.Icon(ft.Icons.FOLDER_OUTLINED), leading_width=50,
            title=ft.Text('Crafter'),
            actions=[ft.IconButton(ft.Icons.LIGHT_MODE, on_click=lambda x: ch.toggle_theme_mode(home_view=self, e=x)),
                     ft.PopupMenuButton(
                         items=[ft.PopupMenuItem(text='Settings', icon=ft.Icons.SETTINGS,
                                                 on_click=lambda x: ch.goto_settings_page(home_view=self, e=x)),
                                ft.PopupMenuItem(text='Help', icon=ft.Icons.HELP,
                                                 on_click=lambda x: ch.goto_help_page(home_view=self, e=x)),
                                ft.PopupMenuItem(text='About', icon=ft.Icons.INFO,
                                                 on_click=lambda x: ch.goto_about_page(home_view=self, e=x))
                                ])
                     ],
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
        )
        self.add_console_log_popup_items_to_appbar()
        self.navigation_bar: ft.NavigationBar = ft.NavigationBar(
            destinations=[ft.NavigationBarDestination(label='Home', icon=ft.Icons.HOME),
                          ft.NavigationBarDestination(label='Install', icon=ft.Icons.INSTALL_MOBILE)],
            on_change=lambda x: ev.on_change_navbar(home_view=self, e=x)
        )
        self.craft_layout: CraftLayout = self.get_new_craft_layout()
        self.install_layout: InstallLayout = self.get_new_install_layout()
        self.controls = [self.craft_layout]

    def get_new_craft_layout(self):
        return CraftLayout(app=self.app)

    def get_new_install_layout(self):
        return InstallLayout(app=self.app)

    def add_console_log_popup_items_to_appbar(self):
        if self.app.debug:
            self.appbar.actions[-1].items.extend([
                ft.PopupMenuItem(text='show console log', icon=ft.Icons.BUG_REPORT,
                                 on_click=lambda x: ch.show_console_log(home_view=self, e=x)
                                 ),
                ft.PopupMenuItem(text='clear console log', icon=ft.Icons.CLEAR_ALL,
                                 on_click=lambda x: ch.clear_console_log(home_view=self, e=x))
            ])
