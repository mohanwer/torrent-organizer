from pathlib import Path
from os.path import splitext
import re, os, shutil

tv_regex = "(.*?)\.(S|s)?(\d{1,2})(E|e)?(\d{2}).*?(.avi|.mkv|.mp4|.mov)$"
tv_regex_compiled = re.compile(tv_regex)


class TvFile:

    season: str
    show_name: str
    episode: str
    is_tv_show: bool

    def __init__(self, full_path: str):
        self.full_path: str = full_path
        self.transferred = False
        self.__path__: Path = Path(full_path)
        _, self.extension = splitext(full_path)
        self.file_name = self.__path__.name
        self.setup_show_props()

    def setup_show_props(self):
        file_regex = tv_regex_compiled.match(self.__path__.name)
        if not file_regex:
            file_regex = tv_regex_compiled.match(self.__path__.parent.name)
        if not file_regex:
            self.is_tv_show = False
            return

        self.is_tv_show = True
        self.show_name = file_regex.group(1)
        self.season = file_regex.group(3)
        self.episode = file_regex.group(5)

    def get_show_name(self) -> str:
        if not self.is_tv_show:
            return

        show_name = self.show_name.upper()
        return show_name

    def get_show_and_episode(self) -> str:
        if not self.is_tv_show:
            return

        show_name = self.get_show_name()
        return show_name + "." + "S" + self.season + "E" + self.episode

    def move_show(self, dest: str) -> bool:
        if not self.is_tv_show:
            return False

        try:
            show_name = self.get_show_name()
            show_folder_path = os.path.join(dest, show_name)
            if not os.path.isdir(show_folder_path):
                os.makedirs(show_folder_path)
            show_and_episode = self.get_show_and_episode()
            show_folder_episode_path = os.path.join(show_folder_path, show_and_episode) + self.extension
            shutil.move(self.__path__, show_folder_episode_path)
            self.transferred = True
            return True
        except OSError as err:
            print(err.filename)
            print(err.strerror)
            return False
