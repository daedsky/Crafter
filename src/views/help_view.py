import flet as ft
from components import custom_controls as cc
from components import admob

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import CrafterApp


# type hinting <end>

class HelperLayout(ft.Column):
    def __init__(self, app: 'CrafterApp', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app: 'CrafterApp' = app
        self.page: ft.Page = app.page
        self.controls = self.layout()

    @staticmethod
    def container_listile(title: str, subtitle: str):
        return ft.Container(
            ft.ListTile(title=ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.SECONDARY),
                        subtitle=ft.Text(subtitle)),
            border_radius=8, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
        )

    def layout(self) -> list[ft.Control]:
        width = self.container_listile('Width', 'Resolution width for bootanimation.')
        height = self.container_listile('Height', 'Resolution height for bootanimation.')
        fps = self.container_listile('FPS', '''Frames Per Second for bootanimation.
Commonly used values: 24, 30, 60.''')
        part_folder = self.container_listile('Part Folder (part0 / partN)', '''Animation starts playing from "part0" and ends at "partN".
Each GIF can be assigned to a partN folder by rearranging their order.
Change the order of GIFs by long pressing their card.''')
        loops = self.container_listile('Loop Count',
                                       'Number of times to loop this part/GIF. (0 = loop this part/GIF until boot is complete)')
        pause = self.container_listile('Pause Count', 'Number of "FRAMES" to pause at the end of this part/GIF.')
        bg_color = self.container_listile('Background Color',
                                          'Background color around the bootanimation. (HEX COLOR CODE FORMAT)')
        part_type = self.container_listile('Part Type ("c" or "p")', '''"c" means play this part/GIF till the end even if the device has booted successfully.
"p" means stop/skip playing this part/GIF as soon device has booted successfully.''')

        dont_know = ft.Container(
            ft.ListTile(title=ft.Text("Still don't know what to do?", size=14, weight=ft.FontWeight.BOLD,
                                      color=ft.Colors.SECONDARY),
                        subtitle=ft.Text('Just leave the default parameters as they are and hit Generate.')),
            border_radius=8, bgcolor=ft.Colors.SECONDARY_CONTAINER
        )

        structure = [
            ft.Container(
                content=ft.Column(
                    controls=[ft.Text('Parameter Explanations', weight=ft.FontWeight.BOLD, size=20,
                                      color=ft.Colors.SECONDARY),
                              part_folder, part_type, loops, pause, bg_color, width, height, fps],
                    scroll=ft.ScrollMode.ALWAYS, height=400
                ),
                border_radius=8, padding=10, bgcolor=ft.Colors.SECONDARY_CONTAINER
            ),
            dont_know
        ]

        if self.page.platform == ft.PagePlatform.ANDROID:
            structure.append(admob.get_new_banner_ad())
            structure.append(admob.get_new_banner_ad())

        return structure


class HelperView(ft.View):
    def __init__(self, app: 'CrafterApp', *args, **kwargs):
        super().__init__(*args, **kwargs, scroll=ft.ScrollMode.AUTO)
        self.app: 'CrafterApp' = app
        self.page: ft.Page = app.page
        self.appbar: ft.AppBar = cc.ReturnHomeAppBar(title_text='Helper')
        self.controls: list[ft.Control] = [HelperLayout(app)]
