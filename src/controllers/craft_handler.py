import flet as ft
from utils import extras
from components import custom_controls as cc
from models.gif import Gif
from services.animation_builder import AnimationBuilder

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.craft_layout import CraftLayout


# type hinting <end>

def __show_err_dlg_if_any_invalid(textfields: list[ft.TextField], page: ft.Page) -> bool:
    for textfield in textfields:
        if textfield.border_color == ft.Colors.ERROR:
            cc.ErrorAlertDialog(page=page, content=f'Invalid Value for field: "{textfield.label}"').show()
            return True
    return False


def __get_gif_files(listview: ft.ReorderableListView, page: ft.Page) -> list[Gif] | None:
    container: cc.GifUiContainer
    gif_files: list[Gif] = []
    for container in listview.controls:
        main_controls = container.main_controls
        filename = main_controls.text_filename.value
        filepath = main_controls.text_filepath.value
        part_type = main_controls.radio_part_type.value
        part_folder = main_controls.textfield_part_folder.value

        textfield_loops = main_controls.textfield_loops
        textfield_pause = main_controls.textfield_pause
        textfield_bg_color = main_controls.textfield_bg_color

        if __show_err_dlg_if_any_invalid(textfields=[textfield_loops, textfield_pause, textfield_bg_color],
                                         page=page):
            gif_files.clear()
            return None

        loops = textfield_loops.value
        pause = textfield_pause.value
        bg_color = f'#{textfield_bg_color.value}'

        gif_files.append(Gif(
            filename=filename,
            filepath=filepath,
            part_type=part_type,
            part_folder=part_folder,
            loops=loops,
            pause=pause,
            bg_color=bg_color
        ))
    return gif_files


def __start_crafting_functions(craft_layout: 'CraftLayout') -> bool:
    gif_files: list[Gif] = __get_gif_files(listview=craft_layout.reorderable_gif_listview, page=craft_layout.page)
    if not gif_files: return False

    process_dlg = cc.ProcessDialog(craft_layout.page)
    craft_layout.page.open(process_dlg)

    anim_builder = AnimationBuilder(gif_files=gif_files, save_folder_path=craft_layout.dest_folder_path,
                                    width=craft_layout.textfield_width.value,
                                    height=craft_layout.textfield_height.value,
                                    fps=craft_layout.textfield_fps.value, delete_files=True)

    extras.run_function(dialog=process_dlg, title='extracting', subtitle='gif files',
                        function=anim_builder.extract_all_gifs)
    extras.run_function(dialog=process_dlg, title='writing', subtitle='desc.txt',
                        function=anim_builder.write_desc_file)
    extras.run_function(dialog=process_dlg, title='zipping', subtitle='gif frames and desc.txt',
                        function=anim_builder.zip_contents)
    extras.run_function(dialog=process_dlg, title='cleaning', subtitle='unnecessary files',
                        function=anim_builder.delete_prezip_files)

    process_dlg.add_text(text=f'Process Finished', color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD)
    process_dlg.enable_done_btn()
    return True


def start_craft(craft_layout: 'CraftLayout') -> None:
    if __show_err_dlg_if_any_invalid(textfields=[craft_layout.textfield_width, craft_layout.textfield_height,
                                                 craft_layout.textfield_fps],
                                     page=craft_layout.page): return
    elif not craft_layout.reorderable_gif_listview.controls:
        cc.ErrorAlertDialog(page=craft_layout.page, content=f'No Files Selected').show()
        return
    elif craft_layout.dest_folder_path is None:
        cc.ErrorAlertDialog(page=craft_layout.page, content='No Destination Folder Selected').show()
        return

    if not __start_crafting_functions(craft_layout=craft_layout): return
    craft_layout.btn_generate.disabled = True
    craft_layout.btn_generate.update()
