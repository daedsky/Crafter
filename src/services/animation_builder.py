from models.gif import Gif
from PIL import Image
import os, shutil
from zipfile import ZipFile, ZIP_STORED


class Utils:
    @staticmethod
    def extract_frames(gif_path: str, extract_path: str, frames_count: int) -> int:
        with Image.open(gif_path) as image:
            for i in range(image.n_frames):
                image.seek(i)
                save_fp = rf'{extract_path}/{frames_count:05d}.png'
                image.save(save_fp)
                frames_count += 1

        return frames_count

    @staticmethod
    def zip_folder_contents(folder_path: str, zip_fp: str):
        with ZipFile(zip_fp, 'w') as archive:
            for root, folders, files in os.walk(folder_path):
                for file in files:
                    if file == 'bootanimation.zip': continue
                    filepath: str = os.path.join(root, file)
                    arcname: str = os.path.relpath(filepath, folder_path)
                    archive.write(filepath, arcname, compress_type=ZIP_STORED)


class AnimationBuilder:
    def __init__(self, gif_files: list[Gif], save_folder_path: str, width: int | str, height: int | str, fps: int | str,
                 delete_files: bool = True):
        self.gif_files = gif_files
        self.save_folder_path = save_folder_path
        self.width = width
        self.height = height
        self.fps = fps
        self.delete_files = delete_files

    def extract_all_gifs(self):
        frames_count: int = 0
        for gif in self.gif_files:
            extract_path = os.path.join(self.save_folder_path, gif.part_folder)
            os.mkdir(extract_path)
            frames_count = Utils.extract_frames(gif.filepath, extract_path, frames_count)

    def write_desc_file(self):
        desc_fp: str = os.path.join(self.save_folder_path, 'desc.txt')
        with open(desc_fp, 'w') as f:
            f.write(f'{self.width} {self.height} {self.fps}\n')
            for gif in self.gif_files:
                f.write(f'{gif.part_type} {gif.loops} {gif.pause} {gif.part_folder} {gif.bg_color}\n')

    def zip_contents(self):
        zip_fp: str = os.path.join(self.save_folder_path, 'bootanimation.zip')
        Utils.zip_folder_contents(self.save_folder_path, zip_fp)

    def delete_prezip_files(self):
        folder_items: list[str] = os.listdir(self.save_folder_path)
        for item in folder_items:
            item_path = os.path.join(self.save_folder_path, item)
            if item == 'bootanimation.zip': continue
            elif os.path.isdir(item_path): shutil.rmtree(item_path)
            else: os.remove(item_path)

    def build_animation(self):
        self.extract_all_gifs()
        self.write_desc_file()
        self.zip_contents()
        if self.delete_files: self.delete_prezip_files()


if __name__ == '__main__':
    def main():
        gif1 = Gif('dp', r'/mnt/shared_partition/PycharmProjects/BAC/storage/data/deadpool_eat_it.gif',
                   'c', 'part0', '1', '0', '#000000')
        gif2 = Gif('omnitrix', r'/mnt/shared_partition/PycharmProjects/BAC/storage/data/omnitrix.gif',
                   'p', 'part1', '1', '0', '#000000')
        save_fp = r'/mnt/shared_partition/PycharmProjects/BAC/storage/temp'
        builder = AnimationBuilder([gif1, gif2], save_fp, 690, 1690, 30, True)
        builder.build_animation()


    main()
