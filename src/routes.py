import flet as ft
from views.settings_view import SettingsView
from views.help_view import HelperView
from views.about_view import AboutView

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import CrafterApp


# type hinting <end>

def route_change(page: ft.Page, app: 'CrafterApp', route):
    page.views.clear()
    if page.route == '/':
        page.views.append(app.home_view)
    if page.route == '/settings':
        page.views.append(SettingsView(app=app, route='/settings'))
    if page.route == '/help':
        page.views.append(HelperView(app=app, route='/help'))
    if page.route == '/about':
        page.views.append(AboutView(app=app, route='/about'))

    page.update()
