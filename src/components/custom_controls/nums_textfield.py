import flet as ft
import re
from enum import Enum


class NumsTextFieldType(Enum):
    NonZero = 'non_zero'
    NoLeadingZeros = 'no_leading_zeros'
    NonZeroAndNoLeadingZeros = 'non_zero_and_no_leading_zeros'


class NumbersOnlyTextField(ft.TextField):
    def __init__(self, field_type: NumsTextFieldType = None,
                 empty_err_msg: str = '*required',
                 no_leading_zeros_err_msg: str = '*cannot have prefix 0',
                 non_zero_err_msg='*value cannot be 0',
                 *args, **kwargs):
        super().__init__(*args, **kwargs, input_filter=ft.NumbersOnlyInputFilter(),
                         keyboard_type=ft.KeyboardType.NUMBER,
                         filled=True, on_change=self.on_change_textfield)
        self.field_type = field_type
        self.empty_err_msg = empty_err_msg
        self.no_leading_zeros_err_msg = no_leading_zeros_err_msg
        self.non_zero_err_msg = non_zero_err_msg

    @staticmethod
    def show_visual_error(textfield: ft.TextField, err_msg: str) -> None:
        textfield.border_color = ft.Colors.ERROR
        textfield.border_width = 1.5
        textfield.label_style = ft.TextStyle(color=ft.Colors.ERROR)
        textfield.helper_text = err_msg
        textfield.update()

    @staticmethod
    def remove_visual_error(textfield: ft.TextField) -> None:
        textfield.border_color = ft.Colors.OUTLINE
        textfield.border_width = None
        textfield.label_style = ft.TextStyle(color=ft.Colors.OUTLINE)
        textfield.helper_text = None
        textfield.update()

    def on_change_textfield(self, e) -> None:
        if e.control.value == '': self.show_visual_error(e.control, self.empty_err_msg)
        elif ((self.field_type == NumsTextFieldType.NonZero or
               self.field_type == NumsTextFieldType.NonZeroAndNoLeadingZeros)
              and re.match(pattern=r'^0+$', string=e.control.value)):
            self.show_visual_error(e.control, self.non_zero_err_msg)

        elif ((self.field_type == NumsTextFieldType.NoLeadingZeros or
               self.field_type == NumsTextFieldType.NonZeroAndNoLeadingZeros)
              and re.match(pattern=r'^0+[1-9]\d*$', string=e.control.value)):
            self.show_visual_error(e.control, self.no_leading_zeros_err_msg)
        else:
            self.remove_visual_error(e.control)
