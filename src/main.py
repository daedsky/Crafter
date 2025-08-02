import flet as ft
from app import CrafterApp
from routes import route_change, view_pop


def set_window_size(page: ft.Page):
    if page.platform != ft.PagePlatform.ANDROID:
        page.window.height = 660
        page.window.width = 430


def main(page: ft.Page):
    set_window_size(page)
    crafter_app = CrafterApp(page=page, debug=True)
    page.overlay.append(crafter_app.file_picker)
    page.overlay.append(crafter_app.perms_handler)
    page.on_route_change = lambda route: route_change(page=page, app=crafter_app, route=route)
    page.on_view_pop = lambda view: view_pop(page=page, view=view)
    crafter_app.show_disclaimer_if_not_accepted()


ft.app(main)
