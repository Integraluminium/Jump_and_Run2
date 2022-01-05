import random
from typing import Tuple, List, Dict
import json
import shutil
import sys
import jump_and_run2

import pygame

from files import SpriteSheet
from files import button
import multiprocessing as mp

from files.level_editor_config import INDEX_LIST, TILE_SIZE, ROWS, MAX_COLS, HUD_SIZE, pattern_dict, get_file_explorer
from files import level_editor_config, file_dialog
from files.constants import FONTS


def draw_text(text: str, color: (Tuple[int, int, int], List[int]), pos: (Tuple[int, int], List[int]),
              font: pygame.font.Font, surface: pygame.Surface):
    img = font.render(text, True, color)
    surface.blit(img, pos)


def _handle_game_instance(file):
    print(file)
    game = jump_and_run2.JumpAndRun()
    game.create_level(file)
    game.run()


def load_new_game_process(level_number):
    level = f"level{level_number}.json"
    print(f"load level {level}")
    try:
        mp.set_start_method('spawn')
        q = mp.Queue()
    except RuntimeError as e:
        print(e)
    p = mp.Process(target=_handle_game_instance, args=(level,))
    p.start()


def load_images(
        tile_size: (Tuple[int, int]),
        index_list: List[str],
        patterns: (List[str], Tuple[str])) -> Dict[str, pygame.Surface]:
    pictures = {}
    sp_sheet = SpriteSheet.SpriteSheet("./graphics/sprites/Spritesheet_most.png")
    t_size = tile_size
    with open("files/index.json", "r") as f:
        data = json.load(f)
    for index in index_list:
        num_pat = index[:2]
        file = data[index]["image"]
        if num_pat in patterns:
            pictures[index] = pygame.transform.scale(sp_sheet.parse_sprite(file), t_size)
    return pictures


def load_background():
    sky_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/sky_cloud.png").convert_alpha())
    mountain_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/mountain2.png").convert_alpha())
    pine1_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/pine1.png").convert_alpha())
    pine2_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/pine2.png").convert_alpha())
    return [sky_img, mountain_img, pine1_img, pine2_img]


def get_buttons(screen_width: int, side_margin: int, img_dict: Dict[str, pygame.Surface], tile_size: int = 50) \
        -> Dict[str, button.Button]:
    # scr_width = screen_width
    # col = 0
    # row = 0
    # button_dict = {}
    # for name, image in img_dict.items():
    #     button_dict[name] = button.Button(scr_width + (60 * col) + 40, (60 * row) + 40, image)
    #     col += 1
    #     if col > 10:
    #         col = 0
    #         row += 1
    # tile_size = 50
    button_dict = {}
    max_columns = (side_margin-41)//tile_size + 1
    for i, value in enumerate(img_dict.items()):
        _, __ = (i // max_columns), (i % max_columns)
        top_col, top_row = screen_width + (tile_size * (i % max_columns)) + 40, (tile_size * (i // max_columns)) + 40
        button_dict[value[0]] = button.Button(top_col, top_row, value[1])
    return button_dict


def get_multidimensional_array(rows: int, cols: int) -> Dict[str, List[List[str]]]:
    # rows = self.ROWS
    # cols = self.MAX_COLS
    layers = {}
    for layer in ("layer4", "layer3", "layer2", "layer1"):
        world_data = []
        for row in range(rows):
            world_data.append(["0000"]*cols)     # Creates nested lists filled with 0

        # create ground
        if layer == "layer4":
            for tile in range(cols):
                world_data[0][tile] = random.choice(("1716", "1716", "1716", "1717", "1718"))
        if layer == "layer3":
            for tile in range(cols):
                world_data[rows-1][tile] = "1016"
        if layer == "layer2":
            for tile in range(cols):
                world_data[rows-1][tile] = "2001"
        layers.update({layer: world_data})
    return layers


class LevelEditor:
    # SCREEN_WIDTH = 800
    # SCREEN_HEIGHT = 640
    SCREEN_HEIGHT = 630
    SCREEN_WIDTH = 780

    LOWER_MARGIN = 100
    SIDE_MARGIN = 575

    ROWS = ROWS
    MAX_COLS = MAX_COLS
    TILE_SIZE = TILE_SIZE

    HUD_SIZE = HUD_SIZE

    INDEX_LIST = INDEX_LIST
    pattern_dict = pattern_dict

    def __init__(self):
        # init
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH + self.SIDE_MARGIN, self.SCREEN_HEIGHT + self.LOWER_MARGIN))
        pygame.display.set_caption("Level Editor")
        self.clock = pygame.time.Clock()

        # creates empty world
        self.world_data = get_multidimensional_array(self.ROWS, self.MAX_COLS)
        print(self.world_data)

        # var game_design
        self.bool_draw_grid = True
        self.exit_editor = False
        self.open_dialogs = []

        self.level = 0
        self.selected_layer = 1
        self.scroll_left = False
        self.scroll_right = False
        self.scroll_speed = 1
        self.scroll = 0
        self.visible_layers = {"layer1": True, "layer2": True, "layer3": True, "layer4": True}

        self.author = "NONE"
        self.level_name = "NONE"
        self.next_level = "NONE"

        self.pos = (-1, -1)
        self.current_tile = None

        # load pictures
        self.pictures = load_images(tile_size=(self.TILE_SIZE, self.TILE_SIZE), index_list=self.INDEX_LIST,
                                    patterns=["00", "14", "10", "18", "19", "20", "17"])  # loads pictures with specific patterns
        # self.pictures = self.load_images(self.pattern_dict.values())
        self.backgrounds = load_background()
        self._HUD_pictures = SpriteSheet.SpriteSheet("graphics/HUD/HUD_spritesheet.png").get_sprites(
            "import.png", "save.png", "trashcan.png", "information.png", "exit.png", "gamepad.png", "menuList.png")

        # Creates HUD
        self.hud_button_list = []
        pos = (self.SCREEN_WIDTH // 5.7) - self.HUD_SIZE[0] // 2  # distance between the icons
        hud_height = self.SCREEN_HEIGHT + self.LOWER_MARGIN // 2
        for i, img in enumerate(self._HUD_pictures, 1):
            x_pos = pos * (i+1)
            self.hud_button_list.append(button.Button(x_pos, hud_height, pygame.transform.scale(img, self.HUD_SIZE)))
        self.hud_click_list = [0] * len(self.hud_button_list)

        self.buttons = get_buttons(self.SCREEN_WIDTH, self.SIDE_MARGIN, self.pictures)

        # dialogs
        screen_x, screen_y = self.screen.get_size()
        x = screen_x // 2
        y = screen_y // 2
        w = 520
        h = 150
        self.exit_box = level_editor_config.get_boxes(x, y, w, h, "exit_box")
        self.dialog_boxes = {
            "delete_box": level_editor_config.get_boxes(x, y, w, h, "delete_box"),
            "info_box": level_editor_config.get_boxes(x, y, w, h, "info_box", font=FONTS["my_font3"]),
            "layer_box": level_editor_config.get_boxes(x, y, w, h, "layer_box"),
        }

    def save(self):

        # with open("levels/levels.json", "r") as f:
        #     data = json.load(f)
        # data[f"level{self.level}"] = self.world_data

        name = f"level{self.level}"
        author = self.author
        next_level = self.next_level
        print("save", name, author, next_level)
        data = {
            "name": name,
            "author": author,
            "next_level": next_level,
            "level_data": self.world_data,
        }

        # Backup der alten Daten
        try:
            shutil.copyfile(f"levels/{name}.json", f"levels/levelbackup/backup_data-{name}.json")
        except FileNotFoundError:
            print("created file")

        with open(f"levels/{name}.json", "w") as f:
            data = json.dumps(data)
            data = "[\n [".join(data.split("[["))
            data = "], \n".join(data.split("],"))
            data = "]\n ]}".join(data.split("]]}"))
            f.write(data)

    def load(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            self.world_data = data["level_data"]
            self.author = data["author"]
            self.level_name = data["name"]
            self.next_level = data["next_level"]
            self.update_world_info()
        except FileNotFoundError as e:
            print(e)

    def update_world_info(self):
        box = self.dialog_boxes["info_box"].elements
        box["author"].text = self.author
        box["current_level"].text = self.level_name
        box["next_level"].text = self.next_level

    def draw_bg(self):
        self.screen.fill("grey50")
        width = self.backgrounds[0].get_width()
        sky_img, mountain_img, pine1_img, pine2_img, *_ = self.backgrounds
        sr_height = self.SCREEN_HEIGHT
        scroll = self.scroll
        for x in range(2):
            self.screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
            self.screen.blit(mountain_img, ((x * width) - scroll * 0.6, sr_height - mountain_img.get_height() - 300))
            self.screen.blit(pine1_img, ((x * width) - scroll * 0.7, sr_height - pine1_img.get_height() - 150))
            self.screen.blit(pine2_img, ((x * width) - scroll * 0.8, sr_height - pine2_img.get_height()))

    def draw_grid(self):
        tile_size = self.TILE_SIZE
        scr_height, scr_width = self.SCREEN_HEIGHT, self.SCREEN_WIDTH
        cols, rows = self.MAX_COLS, self.ROWS
        scroll = self.scroll
        screen = self.screen
        # vertical lines
        for c in range(cols + 1):
            pygame.draw.line(screen, "white", (c*tile_size - scroll, 0), (c*tile_size - scroll, scr_height))
        # vertical
        for c in range(rows + 1):
            pygame.draw.line(screen, "white", (0, c*tile_size), (scr_width, c*tile_size))

    def draw_tile_panel(self):
        screen = self.screen
        btn_dict = self.buttons
        scr_height, scr_width, margin = self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.SIDE_MARGIN
        pygame.draw.rect(screen, "grey50", (scr_width, 0, margin, scr_height+10))
        for index, btn in btn_dict.items():     # Select the Tile
            # pygame.draw.rect(self.screen, "grey", btn.rect, 1, 0)     # Border Tiles
            if btn.draw(self.screen):
                self.current_tile = index
        # highlight the selected tile
        if self.current_tile is not None:
            pygame.draw.rect(self.screen, "red", btn_dict[self.current_tile].rect, 2, 5)

    def draw_load_section(self):
        screen = self.screen
        hud_button_list = self.hud_click_list
        b = [0] * len(hud_button_list)
        for i, btn in enumerate(self.hud_button_list):
            if btn.draw(screen):
                if hud_button_list[i] == 0:
                    b[i] = 1
                hud_button_list[i] = 1
            else:
                hud_button_list[i] = 0

        if b[0] == 1:
            print("select")
            # self.load()
            self.open_dialogs.append(("file_explorer", get_file_explorer(self.screen.get_size())))

        if b[1] == 1:
            print("save")
            self.save()

        if b[2] == 1:
            print("trash")
            # self.world_data = self.get_multidimensional_array()
            self.open_dialogs.append(("delete_box", self.dialog_boxes["delete_box"]))
        if b[3] == 1:
            print("information")
            self.update_world_info()
            self.open_dialogs.append(("info_box", self.dialog_boxes["info_box"]))

        if b[4] == 1:
            print("exit")
            self.exit_editor = True

        if b[5] == 1:
            print("game")
            # load_new_game_process(self.selected)
            print("out of order")

        if b[6] == 1:
            print("layer")
            self.open_dialogs.append(("layer_box", self.dialog_boxes["layer_box"]))

        draw_text(f"Level: {self.level}", "black", (20, self.SCREEN_HEIGHT + 20), FONTS["my_font1"], self.screen)
        draw_text("Press up or down", "black", (20, self.SCREEN_HEIGHT + 45), FONTS["my_font2"], self.screen)
        draw_text("to change layer", "black", (20, self.SCREEN_HEIGHT + 60), FONTS["my_font2"], self.screen)
        draw_text(f"layer: {self.selected_layer}", "black", (20, self.SCREEN_HEIGHT + 80), FONTS["my_font2"], self.screen)

    def draw_world(self):
        pictures = self.pictures
        layers = self.world_data
        screen = self.screen
        tile_size = self.TILE_SIZE
        scroll = self.scroll
        for layer in layers.keys():
            if self.visible_layers[layer]:
                world = layers[layer]
                for y, row in enumerate(world):
                    for x, tile in enumerate(row):
                        if tile not in ("0000", "0"):
                            screen.blit(pictures[tile], (x * tile_size - scroll, y * tile_size))

    def change_world(self):
        pos = pygame.mouse.get_pos()
        layer = f"layer{self.selected_layer}"  # TODO DEBUG layer is missing
        # check mouse not in working Area
        if not(pos[0] < self.SCREEN_WIDTH and pos[1] < self.SCREEN_HEIGHT):
            # print("outside Working Area")
            return
        if self.current_tile is None:
            return

        x = (pos[0] + self.scroll) // self.TILE_SIZE
        y = (pos[1]) // self.TILE_SIZE

        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_RCTRL] or pressed_key[pygame.K_LCTRL]:
            save_mode = True
        else:
            save_mode = False

        if pygame.mouse.get_pressed(3)[0] == 1:
            # rem double
            if (x, y) != self.pos:
                self.pos = (x, y)
                print(f"i {x, y}")
            if not save_mode:
                if self.world_data[layer][y][x] != self.current_tile:
                    self.world_data[layer][y][x] = self.current_tile
            else:
                if self.world_data[layer][y][x] == "0000":
                    self.world_data[layer][y][x] = self.current_tile

        if pygame.mouse.get_pressed(3)[2] == 1:
            if (x, y) != self.pos:
                self.pos = (x, y)
                print(f"r {x, y}")
            if not save_mode:
                if self.world_data[layer][y][x] != "0000":
                    self.world_data[layer][y][x] = "0000"
            else:
                if self.world_data[layer][y][x] == self.current_tile:
                    self.world_data[layer][y][x] = "0000"

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_editor = True

            if self.exit_editor:
                events = self.exit_box.handle_box_events(event)
                if events["exit"] is True:
                    pygame.quit()
                    sys.exit(43)
                elif events["cancel"] is True:
                    self.exit_editor = False

            if len(self.open_dialogs) > 0:
                name, dialog = self.open_dialogs[0]
                if name == "file_explorer":
                    out = dialog.handle_box_events(event)
                    if out:
                        print(out)
                        self.load(out)
                        self.open_dialogs.pop(0)
                    continue
                results = dialog.handle_box_events(event)
                for _name, result in results.items():   # global scope for multiple boxes
                    if _name == "cancel" and result is True:
                        self.open_dialogs.pop(0)

                if name == "delete_box":    # individual handler for each box
                    if results["delete_world"] is True:
                        self.world_data = get_multidimensional_array(self.ROWS, self.MAX_COLS)
                        self.open_dialogs.pop(0)
                elif name == "info_box":
                    if results["author"] is not None:
                        self.author = results["author"]
                        self.level_name = results["current_level"]
                        self.next_level = results["next_level"]
                        self.open_dialogs.pop(0)
                        self.save()

                    elif results["ok"] is True:
                        self.author = self.dialog_boxes["info_box"].elements["author"].text
                        self.level_name = self.dialog_boxes["info_box"].elements["current_level"].text
                        self.next_level = self.dialog_boxes["info_box"].elements["next_level"].text
                        self.open_dialogs.pop(0)
                        self.save()
                elif name == "layer_box":
                    self.visible_layers["layer1"] = results["layer1"]
                    self.visible_layers["layer2"] = results["layer2"]
                    self.visible_layers["layer3"] = results["layer3"]
                    self.visible_layers["layer4"] = results["layer4"]
                    print(self.visible_layers)

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = True
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = True
                    if event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
                        self.scroll_speed = 5
                    if event.key == pygame.K_UP and self.selected_layer+1 in (1, 2, 3, 4):
                        self.selected_layer += 1
                    if event.key == pygame.K_DOWN and self.selected_layer-1 in (1, 2, 3, 4):
                        self.selected_layer -= 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = False
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = False
                    if event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
                        self.scroll_speed = 1

        # Scroll the map
        if self.scroll_right and self.scroll < (
                self.MAX_COLS * self.TILE_SIZE) - self.SCREEN_WIDTH - self.TILE_SIZE // 2:
            self.scroll += 5 * self.scroll_speed
        if self.scroll_left and self.scroll > 0:
            self.scroll -= 5 * self.scroll_speed
        if self.scroll < 0:
            self.scroll = 0

    def run(self):
        while True:
            self.event_loop()

            self.draw_bg()
            self.draw_world()
            if self.bool_draw_grid:
                self.draw_grid()
            self.draw_tile_panel()
            self.draw_load_section()

            if len(self.open_dialogs) > 0:
                self.open_dialogs[0][1].draw(self.screen)
                # pygame.draw.rect(self.surface_screen, "green", self.exit_box.elements["exit"].abs_rect)
            else:
                self.change_world()

            if self.exit_editor:
                self.exit_box.draw(self.screen)
                # pygame.draw.rect(self.surface_screen, "green", self.exit_box.elements["exit"].abs_rect)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    editor = LevelEditor()
    # editor.get_exit_box()
    editor.run()
