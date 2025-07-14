from controllers.gif_ui_builder import build_gif_ui
import os
import flet as ft
from components import custom_controls as cc

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.craft_layout import CraftLayout
    from views.install_layout import InstallLayout
    from views.home_view import HomeView


# type hinting <end>

def on_result_gifs_picked(craft_layout: 'CraftLayout', e):
    if e.files is None: return
    for i, file in enumerate(e.files):
        part_foldername = f'part{craft_layout.gif_files_count}'
        build_gif_ui(craft_layout, file.name, file.path, part_foldername)
        craft_layout.gif_files_count += 1
    craft_layout.container_fileslist.content = craft_layout.reorderable_gif_listview
    craft_layout.container_fileslist.update()


def on_result_dest_folder_selected(craft_layout: 'CraftLayout', e):
    if e.path is None: return
    elif os.listdir(e.path) != []:
        cc.ErrorAlertDialog(page=craft_layout.page, content='Please select an empty folder.').show()
        return
    craft_layout.dest_folder_path = e.path
    craft_layout.listile_dest_path.subtitle = ft.Text(craft_layout.dest_folder_path, weight=ft.FontWeight.BOLD,
                                                      color=ft.Colors.PRIMARY)
    craft_layout.listile_dest_path.update()


def on_gif_listview_reorder(craft_layout: 'CraftLayout', e):
    craft_layout.reorderable_gif_listview.controls.insert(
        e.new_index, craft_layout.reorderable_gif_listview.controls.pop(e.old_index)
    )
    container: cc.GifUiContainer
    for i, container in enumerate(craft_layout.reorderable_gif_listview.controls):
        container.main_controls.textfield_part_folder.value = f'part{i}'
    craft_layout.reorderable_gif_listview.update()


def on_change_navbar(home_view: 'HomeView', e):
    index = e.control.selected_index
    if index == 0:
        home_view.controls = [home_view.craft_layout]
        home_view.update()
    elif index == 1:
        home_view.controls = [home_view.install_layout]
        home_view.update()


def on_result_bootanim_zip_picked(install_layout: 'InstallLayout', e):
    if e.files is None: return
    install_layout.picked_zip_file_fp = os.path.abspath(e.files[0].path)
    install_layout.listile_picked_zip_file.subtitle = ft.Text(install_layout.picked_zip_file_fp,
                                                              weight=ft.FontWeight.BOLD,
                                                              color=ft.Colors.PRIMARY)
    install_layout.listile_picked_zip_file.update()


def on_change_install_fp_dropdown(install_layout: 'InstallLayout', e):
    if e.control.value == 'Custom':
        install_layout.textfield_install_location.disabled = False
    elif e.control.value == 'Default':
        install_layout.textfield_install_location.disabled = True
        install_layout.textfield_install_location.value = install_layout.default_bootanimation_fp
    else:
        install_layout.textfield_install_location.disabled = True
        install_layout.textfield_install_location.value = e.control.value

    install_layout.textfield_install_location.update()
