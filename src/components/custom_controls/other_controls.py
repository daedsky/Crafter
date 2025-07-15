import flet as ft


class FilledButton(ft.FilledButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(14)))


class HeaderText(ft.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, size=16, weight=ft.FontWeight.W_500, color=ft.Colors.PRIMARY)


class ListTilePickedItem(ft.ListTile):
    def __init__(self, title: str, subtitle: str, **kwargs):
        super().__init__(title=ft.Text(title, size=12),
                         subtitle=ft.Text(subtitle, size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.ERROR),
                         leading=ft.Icon(ft.Icons.FOLDER_OPEN_SHARP),
                         bgcolor=ft.Colors.SECONDARY_CONTAINER,
                         **kwargs)


class ErrorAlertDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, content: str, *args, **kwargs):
        self.pagee: ft.Page = page  # Gives Error if used "self.page" so using "self.pagee"
        super().__init__(modal=True, title=ft.Text('Error'), content=ft.Text(content),
                         actions=[ft.TextButton('OK', on_click=lambda _: page.close(self))],
                         scrollable=True, *args, **kwargs)

    def show(self):
        self.pagee.open(self)


class InfoAlertDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, content_text: str, title_text: str = 'Info', **kwargs):
        self.pagee = page
        super().__init__(modal=True, title=ft.Text(title_text), content=ft.Text(content_text),
                         actions=[ft.TextButton('OK', on_click=lambda _: page.close(self))], scrollable=True,
                         **kwargs)

    def show(self):
        self.pagee.open(self)


class CardViewContainer(ft.Container):
    def __init__(self, icon: ft.Icons = None, title_text: str = None, content_controls: list[ft.Control] = None,
                 bgcolor: ft.Colors = ft.Colors.SURFACE_CONTAINER_HIGHEST, *args, **kwargs):
        title = ft.Row(
            [ft.Icon(icon), ft.Text(title_text, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, size=16)])
        col = ft.Column(controls=[title])
        col.controls.extend(content_controls)
        super().__init__(*args, **kwargs, content=col, padding=5, bgcolor=bgcolor,
                         border_radius=8, expand=True)


class ReturnHomeAppBar(ft.AppBar):
    def __init__(self, title_text: str, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_size=25, on_click=lambda x: self.page.go('/')),
                         title=ft.Text(title_text),
                         bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST)
