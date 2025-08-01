import os
from utils import extras
from datetime import datetime
from components import custom_controls as cc
import flet as ft
from pathlib import PurePath

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.install_layout import InstallLayout


# type hinting <end>

def __is_file(path: PurePath) -> bool:
    if path.suffix == '':
        return False
    return True


def __get_installation_location_fp_if_exists(install_layout: 'InstallLayout') -> str | None:
    path = PurePath(os.path.abspath(install_layout.textfield_install_location.value))
    if __is_file(path):  # check if the path have suffix i.e. file extension then it is a file else dir
        if os.path.basename(path) == 'bootanimation.zip':
            if os.path.exists(path):  # check if the whole file exists
                return str(path)
            elif os.path.exists(os.path.dirname(path)):  # check if directory exists but file doesn't
                return str(path)
            cc.ErrorAlertDialog(page=install_layout.page,
                                content=f'Installation location file or directory {path} not found.').show()
            return None
        cc.ErrorAlertDialog(page=install_layout.page, content=f'Filename must be "bootanimation.zip"').show()
        return None

    if os.path.exists(path): return os.path.join(path, 'bootanimation.zip')
    cc.ErrorAlertDialog(page=install_layout.page, content=f'Installation location {path} not found.').show()
    return None


def __su_binary_exists(page: ft.Page) -> bool:
    if page.platform != ft.PagePlatform.ANDROID: return True
    try:
        import subprocess
        proc = subprocess.run('su -c echo hello'.split(), capture_output=True, text=True)
        if proc.returncode != 0:
            cc.ErrorAlertDialog(page=page, content=f'{proc.stderr}').show()
        return proc.returncode == 0
    except FileNotFoundError:
        cc.ErrorAlertDialog(page=page, content='su binary not found. Aborting...').show()
        return False


def __start_installing(install_layout: 'InstallLayout', install_location_fp: str) -> None:
    after_root_dir = PurePath(install_location_fp).parents[-2]  # "/system", "/product", "/data", etc
    bootanim_zip_exists: bool = os.path.exists(install_location_fp)
    CURRENT_DATETIME: str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    BACKUP_FP: str = rf'/sdcard/Download/bootanimation_backup_{CURRENT_DATETIME}.zip'

    REMOUNT_CMD = rf'su -c mount -o rw,remount {after_root_dir}'
    BACKUP_CMD = rf'su -c cp {install_location_fp} {BACKUP_FP}'
    INSTALL_CMD = rf'su -c cp {install_layout.picked_zip_file_fp} {install_location_fp}'
    CHOWN_CMD = rf'su -c chown root:root {install_location_fp}'
    CHMOD_CMD = rf'su -c chmod 644 {install_location_fp}'

    if install_layout.page.platform.name != 'ANDROID':
        REMOUNT_CMD = rf'echo {REMOUNT_CMD}'
        BACKUP_CMD = rf'echo {BACKUP_CMD} '
        INSTALL_CMD = rf'pecho {INSTALL_CMD}'
        CHOWN_CMD = rf'echo {CHOWN_CMD}'
        CHMOD_CMD = rf'hecho {CHMOD_CMD}'

    process_dlg = cc.ProcessDialog(install_layout.page)
    install_layout.page.open(process_dlg)
    process_dlg.add_text('Process Started', color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD)

    extras.run_command(dialog=process_dlg, title='Remounting', subtitle=str(after_root_dir),
                       command=REMOUNT_CMD)

    if bootanim_zip_exists:
        extras.run_command(dialog=process_dlg, title='Creating Backup',
                           subtitle=f'{install_location_fp} to {BACKUP_FP}',
                           command=BACKUP_CMD)

    extras.run_command(dialog=process_dlg, title='Installing',
                       subtitle=f'{install_layout.picked_zip_file_fp} to {install_location_fp}',
                       command=INSTALL_CMD)

    extras.run_command(dialog=process_dlg, title='Changing Owner & Group',
                       subtitle=f'{install_location_fp} to root',
                       command=CHOWN_CMD)

    extras.run_command(dialog=process_dlg, title=f'Changing Permissions', subtitle=f'{install_location_fp} to 644',
                       command=CHMOD_CMD)

    process_dlg.add_text('Process Finished', color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD)
    process_dlg.enable_done_btn()


def install(install_layout: 'InstallLayout') -> None:
    if not __su_binary_exists(page=install_layout.page): return

    elif install_layout.picked_zip_file_fp is None:
        cc.ErrorAlertDialog(page=install_layout.page, content='Please select a bootanimation.zip file').show()
        return

    install_location_fp: str | None = __get_installation_location_fp_if_exists(install_layout)
    if not install_location_fp: return

    __start_installing(install_layout=install_layout, install_location_fp=install_location_fp)

    install_layout.btn_install.disabled = True
    install_layout.btn_install.update()
