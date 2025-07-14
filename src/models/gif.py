from dataclasses import dataclass
from flet import Text, TextField, RadioGroup


@dataclass
class Gif:
    filename: str
    filepath: str
    part_type: str
    part_folder: str
    loops: str
    pause: str
    bg_color: str


@dataclass
class ControlsForGif:
    text_filename: Text
    text_filepath: Text
    textfield_part_folder: TextField
    textfield_loops: TextField
    textfield_pause: TextField
    textfield_bg_color: TextField
    radio_part_type: RadioGroup
