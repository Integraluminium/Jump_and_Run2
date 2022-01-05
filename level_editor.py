from typing import Tuple, List
import json
import shutil
import sys
import jump_and_run2

# import jsbeautifier as jsbeautifier
import pygame

from files import SpriteSheet
from files import button
from files import get_valid_list
from files import input_box
import multiprocessing as mp

image_dict = get_valid_list.get_path_dict()


def draw_text(text: str, color: (Tuple[int, int, int], List[int]), pos: (Tuple[int, int], List[int]),
              font: pygame.font.Font, surface: pygame.Surface):
    img = font.render(text, True, color)
    surface.blit(img, pos)


def _handle_game_instance(file):
        print(file)
        game = jump_and_run2.JumpAndRun()
        print("asdfafga")
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

    # def _handle_game_instance():
    #     game = jump_and_run2.JumpAndRun()
    #     print("asdfafga")
    #     game.create_level("level0.json")
    #     game.run()

    p = mp.Process(target=_handle_game_instance, args=(level,))
    p.start()



class LevelEditor:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 640

    LOWER_MARGIN = 100
    SIDE_MARGIN = 675

    ROWS = 16
    MAX_COLS = 150
    TILE_SIZE = SCREEN_HEIGHT // ROWS

    HUD_SIZE = (90, 90)

    INDEX_LIST = ['0001', '0005',
                  '1000', '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010', '1011',
                  '1012', '1013', '1014', '1015', '1016', '1017', '1100', '1101', '1102', '1103', '1104', '1105',
                  '1106', '1107', '1108', '1109', '1110', '1111', '1112', '1113', '1114', '1115', '1116', '1200',
                  '1201', '1202', '1203', '1204', '1205', '1206', '1207', '1208', '1300', '1301', '1302', '1303',
                  '1304', '1305', '1306', '1307', '1308', '1309', '1310', '1311', '1312', '1313', '1314', '1315',
                  '1316', '1317', '1318', '1319', '1320', '1321', '1322', '1323', '1324', '1325', '1326', '1327',
                  '1328', '1400', '1401', '1402', '1403', '1404', '1405', '1406', '1407', '1408', '1409', '1410',
                  '1411', '1412', '1413', '1414', '1415', '1416', '1417', '1500', '1501', '1502', '1503', '1504',
                  '1505', '1506', '1507', '1508', '1509', '1510', '1511', '1512', '1513', '1514', '1515', '1516',
                  '1517', '1600', '1601', '1602', '1603', '1604', '1605', '1606', '1607', '1608', '1609', '1610',
                  '1611', '1612', '1613', '1614', '1615', '1616', '1617', '1700', '1701', '1702', '1703', '1704',
                  '1705', '1706', '1707', '1710', '1711', '1712', '1713', '1714', '1715', '1716',
                  '1717', '1718', '1719', '1720', '1721', '1722', '1800', '1802', '1803', '1804', '1805', "1810", "1811",
                  '1900', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909', '1910', '1911',
                  '1912', '1913', '1914', '1915', '1916', '1917', '1918', '1919', '2000', '2001', '2002', '2003',
                  '2004', '2005', "2006", '2008', "2009",  '2010', '2013', '2014', '2015',
                  '2016', '2017', '2018', '2019', '2020', '2022', '2023', '2024', '2025', '2026', '2027',
                  '2028', '2029', '2030']
    pattern_dict = {
        "gras": "10",
        "dirt": "11",
        "dirt_en": "12",
        "stone": "13",
        "sand": "14",
        "snow": "15",
        "castle": "16",
        "metal": "17",
        "liquids": "18",
        "sp_tiles": "19",
        "items": "20"
    }

    def __init__(self):
        # init
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH + self.SIDE_MARGIN, self.SCREEN_HEIGHT + self.LOWER_MARGIN))
        pygame.display.set_caption("Level Editor")
        self.clock = pygame.time.Clock()

        # creates empty world
        self.world_data = self.get_array()

        # var game_design
        self.bool_draw_grid = True
        self.exit_editor = False
        self.open_dialogs = []

        self.level = 0
        self.selected = 0
        self.scroll_left = False
        self.scroll_right = False
        self.scroll_speed = 1
        self.scroll = 0
        self.layer = 4

        self.author = "NONE"
        self.level_name = "NONE"
        self.next_level = "NONE"

        self.pos = (-1, -1)
        self.current_tile = None

        # FONT
        self.my_font = pygame.font.SysFont("futura", 30)
        self.my_font2 = pygame.font.SysFont("futura", 20)
        my_font3 = pygame.font.SysFont("futura", 28)

        # load pictures
        self.pictures = self.load_images(["00", "14", "10", "18", "19", "20", "17"])  # loads pictures with specific patterns
        # self.pictures = self.load_images(self.pattern_dict.values())
        self.backgrounds = self.load_background()
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

        self.buttons = self.get_buttons(self.pictures)

        # dialogs
        screen_x, screen_y = self.screen.get_size()
        x = screen_x // 2
        y = screen_y // 2
        w = 520
        h = 150
        self.exit_box = input_box.ButtonBox(x, y, w, h, {
            "cancel": input_box.Button(round(w * 1 / 3), 100, 150, 34, text="cancel"),
            "exit": input_box.Button(round(w * 2 / 3), 100, 150, 34, text="exit")},
                                            text="Do you really want to exit?")
        self.dialog_boxes = {
            "delete_box": input_box.ButtonBox(x, y, w, h, {
                "cancel": input_box.Button(round(w * 1 / 3), 100, 150, 34, text="cancel"),
                "delete_world": input_box.Button(round(w * 2 / 3), 100, 150, 34, text="delete")},
                                              text="Do you really want to delete this World?"),
            "info_box": input_box.ButtonBox(x, y, w, h*2, {     # +64
                "text1": input_box.TextField(10, 60 + 7, 70, 32, "author:", font=my_font3),
                "author": input_box.InputField(95, 60, 355, 32, self.author),
                "text2": input_box.TextField(10, 124-3, 70, 32, "current", font=my_font3),
                "text3": input_box.TextField(10, 124 + 14+3, 70, 32, "level", font=my_font3),
                "current_level": input_box.InputField(95, 124, 355, 32, self.level_name, disabled=True),
                "text4": input_box.TextField(10, 188-3, 70, 32, "next", font=my_font3),
                "text5": input_box.TextField(10, 188 + 14+3, 70, 32, "level", font=my_font3),
                "next_level": input_box.InputField(95, 188, 355, 32, self.next_level, disabled=True),
                "ok": input_box.Button(round(w*1/2), 252, 150, 34, text="ok")},
                                            text="World data:"),
            "layer_box": input_box.ButtonBox(x, y, w, h*2, {
                "text1": input_box.TextField(10, 60-3, 150, 32, "Background-tiles"),
                "layer1": input_box.Button(round(w * 2 / 3), 60, text="layer1"),
                "text2": input_box.TextField(10, 124 - 3, 150, 32, "Layer1 and collision"),
                "layer2": input_box.Button(round(w * 2 / 3), 124, text="layer2"),
                "text3": input_box.TextField(10, 188 - 3, 150, 32, "Background"),
                "layer3": input_box.Button(round(w * 2 / 3), 188, text="layer3"),
                # "text4": input_box.TextField(10, 252 - 3, 150, 32, "Background"),
                # "layer4": input_box.Button(round(w * 2 / 3), 252, text="layer4"),
                "cancel": input_box.Button(round(w * 1 / 2), 252, 150, 34, text="cancel")
                        }, text="Z-Index"),
        }

    # def get_exit_box(self):
    #     screen_x, screen_y = self.screen.get_size()
    #     x = screen_x // 2
    #     y = screen_y // 2
    #     w = 520
    #     h = 150
    #     choice_box = input_box.ButtonBox(x, y, w, h, {
    #         "cancel": input_box.Button(round(w*1/3), 100, 150, 34, text="cancel"),
    #         "exit": input_box.Button(round(w*2/3), 100, 150, 34, text="exit")},
    #                                      text="Do you really want to exit?")
    #     return choice_box

    def load_images(self, patterns: (List[str], Tuple[str])):
        pictures = {}
        sp_sheet = SpriteSheet.SpriteSheet("./graphics/sprites/Spritesheet_most.png")
        t_size = (self.TILE_SIZE, self.TILE_SIZE)
        with open("files/index.json", "r") as f:
            data = json.load(f)
        for index in self.INDEX_LIST:
            num_pat = index[:2]
            file = data[index]["image"]
            if num_pat in patterns:
                pictures[index] = pygame.transform.scale(sp_sheet.parse_sprite(file), t_size)
        return pictures

    @staticmethod
    def load_background():
        sky_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/sky_cloud.png").convert_alpha())
        mountain_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/mountain2.png").convert_alpha())
        pine1_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/pine1.png").convert_alpha())
        pine2_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/pine2.png").convert_alpha())
        return [sky_img, mountain_img, pine1_img, pine2_img]

    def get_buttons(self, img_dict: dict) -> dict:
        scr_width = self.SCREEN_WIDTH
        col = 0
        row = 0
        button_dict = {}
        for name, image in img_dict.items():
            button_dict[name] = button.Button(scr_width + (60 * col) + 40, (60 * row) + 40, image)
            col += 1
            if col > 10:
                col = 0
                row += 1
        return button_dict

    def get_array(self):
        rows = self.ROWS
        cols = self.MAX_COLS
        world_data = []
        for row in range(rows):
            world_data.append(["0000"]*cols)     # Creates nested lists filled with 0

        # create ground
        for tile in range(cols):
            world_data[rows-1][tile] = "1016"
        return world_data

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

        # Schreibt die Daten
        # with open(f"levels/{name}.json", "w") as f:   # alternative JSON output parser
        #     opts = jsbeautifier.default_options()
        #     opts.indent_size = 2
        #     f.write(jsbeautifier.beautify(json.dumps(data), opts))

        with open(f"levels/{name}.json", "w") as f:
            data = json.dumps(data)
            data = "[\n [".join(data.split("[["))
            data = "], \n".join(data.split("],"))
            data = "]\n ]}".join(data.split("]]}"))
            f.write(data)

    def load(self):
        try:
            self.level = self.selected
            name = f"level{self.level}"
            with open(f"levels/{name}.json", "r") as f:
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
        self.screen.fill("mediumspringgreen")
        width = self.backgrounds[0].get_width()
        sky_img, mountain_img, pine1_img, pine2_img, *_ = self.backgrounds
        sr_height = self.SCREEN_HEIGHT
        scroll = self.scroll
        for x in range(4):
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
        pygame.draw.rect(screen, "mediumspringgreen", (scr_width, 0, margin, scr_height))
        for index, btn in btn_dict.items():
            if btn.draw(self.screen):
                self.current_tile = index
                # print(index, btn)
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
            self.load()

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
            load_new_game_process(self.selected)

        if b[6] == 1:
            print("layer")
            self.open_dialogs.append(("layer_box", self.dialog_boxes["layer_box"]))


        draw_text(f"Level: {self.level}", "black", (20, self.SCREEN_HEIGHT + 20), self.my_font, self.screen)
        draw_text("Press up or down", "black", (20, self.SCREEN_HEIGHT + 45), self.my_font2, self.screen)
        draw_text("to change level", "black", (20, self.SCREEN_HEIGHT + 60), self.my_font2, self.screen)
        draw_text(f"select: {self.selected}", "black", (20, self.SCREEN_HEIGHT+80), self.my_font2, self.screen)

    def draw_world(self):
        pictures = self.pictures
        world = self.world_data
        screen = self.screen
        tile_size = self.TILE_SIZE
        scroll = self.scroll
        for y, row in enumerate(world):
            for x, tile in enumerate(row):
                if (tile != "0000" and tile != "0"):
                    screen.blit(pictures[tile], (x * tile_size - scroll, y * tile_size))

    def change_world(self):
        pos = pygame.mouse.get_pos()
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
                if self.world_data[y][x] != self.current_tile:
                    self.world_data[y][x] = self.current_tile
            else:
                if self.world_data[y][x] == "0000":
                    self.world_data[y][x] = self.current_tile

        if pygame.mouse.get_pressed(3)[2] == 1:
            if (x, y) != self.pos:
                self.pos = (x, y)
                print(f"r {x, y}")
            if not save_mode:
                if self.world_data[y][x] != "0000":
                    self.world_data[y][x] = "0000"
            else:
                if self.world_data[y][x] == self.current_tile:
                    self.world_data[y][x] = "0000"

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_editor = True

            if len(self.open_dialogs) > 0:
                name, dialog = self.open_dialogs[0]
                results = dialog.handle_box_events(event)
                for _name, result in results.items():   # global scope for multiple boxes
                    if _name == "cancel" and result is True:
                        self.open_dialogs.pop(0)

                if name == "delete_box":    # individual handler for each box
                    if results["delete_world"] is True:
                        self.world_data = self.get_array()
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
                    if results["layer1"]:
                        print("layer1")
                        self.layer = 1
                        self.open_dialogs.pop(0)
                    elif results["layer2"]:
                        print("layer2")
                        self.layer = 2
                        self.open_dialogs.pop(0)
                    elif results["layer3"]:
                        print("layer3")
                        self.layer = 3
                        self.open_dialogs.pop(0)




            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = True
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = True
                    if event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
                        self.scroll_speed = 5
                    if event.key == pygame.K_UP:
                        self.selected += 1
                    if event.key == pygame.K_DOWN and self.selected > 0:
                        self.selected -= 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = False
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = False
                    if event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
                        self.scroll_speed = 1

            if self.exit_editor:
                events = self.exit_box.handle_box_events(event)
                if events["exit"] is True:
                    pygame.quit()
                    sys.exit(43)
                elif events["cancel"] is True:
                    self.exit_editor = False

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
