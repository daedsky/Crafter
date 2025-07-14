import flet as ft
import os
import subprocess
from components import custom_controls as cc
import time
from typing import Callable


def get_installation_filepath(page_platform: ft.PagePlatform) -> tuple[bool, str]:
    if page_platform != ft.PagePlatform.ANDROID: return True, r'/dummy/location/bootanimation.zip'

    possible_file_paths: list[str] = [r'/system/media/bootanimation.zip', r'/product/media/bootanimation.zip',
                                      r'/oem/media/bootanimation.zip', r'/vendor/etc/bootanimation.zip',
                                      r'/data/local/bootanimation.zip']

    file_exists: bool = False
    for file in possible_file_paths:
        if os.path.isfile(file):
            file_exists = True
            return file_exists, file

    for file in possible_file_paths:
        if os.path.isdir(os.path.dirname(file)):
            return file_exists, file

    return file_exists, ''


def run_command(dialog: cc.ProcessDialog, title: str, subtitle: str, command: str) -> None:
    dialog.add_process_tile(title, subtitle)
    try:
        process = subprocess.run(command.split(), capture_output=True, text=True)
    except FileNotFoundError:
        process = subprocess.CompletedProcess(command.split(), 127,
                                              stderr=f'127:command: "{command.split()[0]}" not found')
    time.sleep(1.5)
    dialog.prev_process_completed(code=process.returncode, stderr=process.stderr)


def run_function(dialog: cc.ProcessDialog, title: str, subtitle: str, function: Callable) -> None:
    dialog.add_process_tile(title, subtitle)
    function()
    time.sleep(1.5)
    dialog.prev_process_completed()
