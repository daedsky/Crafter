import flet as ft
import re


class HexOnlyTextField(ft.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, filled=True, max_length=6, prefix_text='#',
                         input_filter=ft.InputFilter(r"^[0-9a-fA-F]*$"), on_change=self.on_change_func)

    @staticmethod
    def on_change_func(e):
        if re.match(r'^[0-9A-Fa-f]{6}$|^[0-9A-Fa-f]{3}$', e.control.value):
            e.control.border_color = ft.Colors.OUTLINE
            e.control.border_width = None
            e.control.label_style = ft.TextStyle(color=ft.Colors.OUTLINE)
            e.control.helper_text = None
        else:
            e.control.border_color = ft.Colors.ERROR
            e.control.border_width = 1.5
            e.control.label_style = ft.TextStyle(color=ft.Colors.ERROR)
            e.control.helper_text = '*invalid'
        e.control.update()
