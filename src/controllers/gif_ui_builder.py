import flet as ft
from components import custom_controls as cc
from models.gif import ControlsForGif

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.craft_layout import CraftLayout


# type hinting <end>

def build_gif_ui(craft_layout: 'CraftLayout', filename: str, filepath: str, part_foldername: str):
    text_filename: ft.Text = ft.Text(filename)
    text_filepath: ft.Text = ft.Text(filepath, visible=False)
    ui_filename: ft.Row = ft.Row([ft.Icon(ft.Icons.TEXT_SNIPPET), text_filename])

    textfield_part_folder: ft.TextField = ft.TextField(value=part_foldername, expand=True, filled=True, read_only=True,
                                                       border_color=ft.Colors.PRIMARY, label='part folder (read only)',
                                                       height=65, fill_color=ft.Colors.SECONDARY_CONTAINER,
                                                       text_style=ft.TextStyle(weight=ft.FontWeight.W_500,
                                                                               color=ft.Colors.PRIMARY))

    tf_kwargs: dict = dict(border_color=ft.Colors.OUTLINE, height=65, expand=True,
                           helper_style=ft.TextStyle(color=ft.Colors.ERROR, size=7.5))

    textfield_loops: cc.NumbersOnlyTextField = cc.NumbersOnlyTextField(label='loop count', value='1', width=60,
                                                                       max_length=2,
                                                                       field_type=cc.NumsTextFieldType.NoLeadingZeros,
                                                                       **tf_kwargs)

    textfield_pause: cc.NumbersOnlyTextField = cc.NumbersOnlyTextField(label='pause frames', value='0', width=60,
                                                                       max_length=3,
                                                                       field_type=cc.NumsTextFieldType.NoLeadingZeros,
                                                                       **tf_kwargs)

    textfield_bg_color: cc.HexOnlyTextField = cc.HexOnlyTextField(label='bg color hex', value='000000', width=110,
                                                                  **tf_kwargs)

    radio_part_type: ft.RadioGroup = ft.RadioGroup(
        content=ft.Column([ft.Text('  Part type'),
                           ft.Row([ft.Radio(label='c', value='c'),
                                   ft.Radio(label='p', value='p')
                                   ])
                           ]),
        value='p'
    )
    ui_part_type: ft.Container = ft.Container(
        content=radio_part_type,
        border=ft.border.only(left=ft.BorderSide(2)),
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        expand=True
    )

    structure: cc.GifUiContainer = cc.GifUiContainer(
        content=ft.ListTile(ft.Column([ui_filename,
                                       ft.Row([textfield_part_folder,
                                               ft.Row([textfield_loops, textfield_pause], expand=True)]),
                                       ft.Row([ui_part_type, textfield_bg_color])
                                       ]), content_padding=0, trailing=ft.Icon(ft.Icons.DRAG_INDICATOR)),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, padding=10, margin=5, border_radius=8,
        main_controls=ControlsForGif(text_filename=text_filename, text_filepath=text_filepath,
                                     textfield_part_folder=textfield_part_folder,
                                     textfield_loops=textfield_loops, textfield_pause=textfield_pause,
                                     textfield_bg_color=textfield_bg_color, radio_part_type=radio_part_type)
    )

    craft_layout.reorderable_gif_listview.controls.append(structure)
