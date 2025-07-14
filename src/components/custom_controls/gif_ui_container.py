import flet as ft
from models.gif import ControlsForGif


class GifUiContainer(ft.Container):
    def __init__(self, *args, main_controls: ControlsForGif, **kwargs):
        self.main_controls: ControlsForGif = main_controls
        super().__init__(*args, **kwargs)
