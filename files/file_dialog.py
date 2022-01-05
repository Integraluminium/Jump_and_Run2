import pathlib
import sys

import pygame
from typing import Union, List
from pathlib import Path

from files import input_box
from files import button
from files.constants import FONTS


class FileDialog:
    def __init__(self, x, y, width, height, file_path=None, allow_directorys=False):
        rect = pygame.Rect(x, y, width, height)
        minimum_dimensions = (260, 300)
        if rect.width < minimum_dimensions[0] or rect.height < minimum_dimensions[1]:
            raise ValueError(f"FileDialog sizes {rect.size} is smaller than minimum size {minimum_dimensions}")
        self.rect = rect
        self.rect.center = (x, y)
        self.surface = pygame.Surface(self.rect.size)

        self.allow_directorys = allow_directorys

        self.current_file_path: pathlib.Path = None #Path()
        if file_path is not None:
            pathend_file_path = Path(file_path).resolve()
            if pathend_file_path.exists():
                if pathend_file_path.is_file():
                    print("file")
                    self.current_file_path = str(pathend_file_path.resolve())
                    self.current_directory_path = str(pathend_file_path.parent.resolve())
                elif pathend_file_path.is_dir():
                    print("dir")
                    self.current_directory_path = str(pathend_file_path.resolve())
                else:
                    raise NotADirectoryError("this path in no directory or file")
            elif pathend_file_path.parent.exists():
                self.current_directory_path = str(pathend_file_path.parent.resolve())
            else:
                raise FileNotFoundError(f"file {file_path} does not exist")
            # if pathend_file_path.exists() and pathend_file_path.is_dir():
            #
            # elif pathend_file_path.exists() and pathend_file_path.is_file():
            #
            # elif
        else:
            self.current_directory_path = str(Path(".").resolve())

        self.current_file_list: Union[List[pathlib.Path]] = []
        self.current_directory_list: Union[List[pathlib.Path]] = []
        self.update_current_file_list()

        self.file_button: Union[List[button.Button]] = []
        self.define_file_buttons()

        self.directory_buttons: Union[List[button.Button]] = []
        self.define_directory_buttons()

        tlcorns = self.rect.topleft
        print(f"{tlcorns=}")
        self.ok_button = input_box.Button(self.rect.width//2, self.rect.height-20, text="laden",
                                          top_left_corner_surface=tlcorns)
        if not self._validate_file_path(self.current_file_path):
            self.ok_button.disable()
        self.create_button = input_box.Button(50, 25, 75, 25, "create", top_left_corner_surface=tlcorns)
        self.refresh_button = input_box.Button(150, 25, 75, 25, "reload", top_left_corner_surface=tlcorns)
        self.up_button = input_box.Button(250, 25, 75, 25, "up", top_left_corner_surface=tlcorns)
        print(self.ok_button.rect.center)
        print(self.ok_button.rect)
        self.path_box = input_box.InputField(10, 50, w=int(self.rect.width)-20, top_left_corner_surface=tlcorns)
        if self.current_file_path:
            self.path_box.set_text(self.current_file_path)
        else:
            self.path_box.set_text(self.current_directory_path)

        self.create_button.set_abs_pos(tlcorns)
        self.ok_button.set_abs_pos(tlcorns)
        self.refresh_button.set_abs_pos(tlcorns)
        self.path_box.set_abs_pos(tlcorns)
        self.up_button.set_abs_pos(tlcorns)

    def update_current_file_list(self):
        file_list = [file for file in Path(self.current_directory_path).iterdir() if file.is_file()]
        directory_list = [f_dir for f_dir in Path(self.current_directory_path).iterdir() if f_dir if f_dir.is_dir()]
        self.current_file_list: Union[List[pathlib.Path]] = file_list
        self.current_directory_list = directory_list

    def define_file_buttons(self):
        self.file_button = []
        for i, filename in enumerate(self.current_file_list):
            dx, dy = self.rect.topleft
            x = 50 +dx
            y = 20*i+110 + dy
            font = FONTS["my_font3"]
            self.file_button.append(button.Button2(x, y, font.render(str(filename.name), True, "black")))

    def define_directory_buttons(self):
        self.directory_buttons = []
        print(self.current_directory_list)
        for i, directory in enumerate(self.current_directory_list):
            dx, dy = self.rect.topleft
            x = 350 + dx
            y = 20*i+110 + dy
            font = FONTS["my_font3"]
            self.directory_buttons.append(button.Button2(x, y, font.render(str(directory.name), True, "green4")))

    @staticmethod
    def _validate_file_path(current_file_path: str) -> bool:
        if current_file_path is None:
            return False
        return Path(current_file_path).exists() and Path(current_file_path).is_file()

    def update(self):
        self.surface.fill(input_box.ButtonBox.COLOR_BACKGROUND)
        self.create_button.draw(self.surface)
        self.ok_button.draw(self.surface)
        self.refresh_button.draw(self.surface)
        self.path_box.draw(self.surface)
        self.up_button.draw(self.surface)

    def draw(self, screen: pygame.Surface):
        self.update()
        screen.blit(self.surface, self.rect)

        for file_button in self.file_button:
            file_button.draw(screen)

        # print(self.directory_buttons)
        for directory in self.directory_buttons:
            directory.draw(screen)

    def change_directory(self):
        self.update_current_file_list()
        self.define_file_buttons()
        self.define_directory_buttons()
        self.path_box.set_text(str(self.current_directory_path))
        self.ok_button.disable()

    def handle_events(self, eventloop_event: pygame.event.Event):
        event_log = {"create": self.create_button.handle_event(eventloop_event),
                     "ok": self.ok_button.handle_event(eventloop_event),
                     "refresh": self.refresh_button.handle_event(eventloop_event),
                     "path": self.path_box.handle_event(eventloop_event),
                     "up": self.up_button.handle_event(eventloop_event)}

        for i, file_button in enumerate(self.file_button):
            # print(button.image)
            if file_button.check_collision():
                print(self.current_file_list[i])
                print(self.current_file_path)
                if self._validate_file_path(current_file_path=str(self.current_file_list[i])):
                    self.current_file_path = self.current_file_list[i]
                    self.path_box.set_text(str(self.current_file_path))
                    self.ok_button.enable()
                else:
                    print("still not allowed")
                    self.ok_button.disable()

        for i, directory_button in enumerate(self.directory_buttons):
            if directory_button.check_collision():
                print(self.current_directory_list[i])
                self.current_directory_path = self.current_directory_list[i]
                self.change_directory()


        if event_log["path"] != "":
            folder_path: str = str(event_log["path"])
            print(folder_path)
            try:
                pathend_folder_path = Path(folder_path)
                print(pathend_folder_path)
            except None as e:
                print(e)
            else:
                if pathend_folder_path.exists():
                    if pathend_folder_path.is_dir():
                        self.current_directory_path = pathend_folder_path
                        self.change_directory()
                    elif pathend_folder_path.is_file():
                        self.current_file_path = pathend_folder_path
                        self.change_directory()

                else:
                    print("not allowed")
                    self.path_box.set_text(str(self.current_directory_path))
        if event_log["refresh"]:
            self.change_directory()
        if event_log["up"]:
            self.current_directory_path = Path(self.current_directory_path).parent
            self.change_directory()


        if not self._validate_file_path(str(self.current_file_path)):
            self.ok_button.disable()

        # print(event_log)
        return event_log

    def get_path(self, eventloop_event):
        out = self.handle_events(eventloop_event)
        if out["ok"]:
            return self.current_file_path
        return False

    def handle_box_events(self,  eventloop_event: pygame.event.Event):
        return self.get_path(eventloop_event)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 640))
    clock = pygame.time.Clock()
    screen_height, screen_width = screen.get_size()

    abs_center_x, abs_center_y = screen_height // 2, screen_width // 2

    fd = FileDialog(abs_center_x, abs_center_y, 620, 500, file_path=r"..\levels")

    while True:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            out = fd.get_path(event)
            print(out)
            if out:
                del fd
                with open(out) as f:
                    print(f.read())

                sys.exit()

            # print(text_box.handle_box_events(event))

        # pygame.draw.rect(surface_screen, "green", text_box.elements["field"].abs_rect)

        fd.draw(screen)
        pygame.display.update()

        clock.tick(60)
