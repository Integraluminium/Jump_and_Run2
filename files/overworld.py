from typing import *
import json
import pygame
from files.SpriteSheet import SpriteSheet, get_ratio_scaled_image

def load_level_config():
    with open("levels/level_config.json", "r") as f:
        data = json.load(f)
    return data


def sort_world(level_data, first_world):
    """Sorts the Worlds specified in JSON file in Dict to python list"""
    # print(level_data)
    current_level_data = level_data[first_world]
    l = [current_level_data]
    for i in range(len(level_data)):
        current_level_data = level_data[current_level_data["unlock"]]
        l.append(current_level_data)
        if current_level_data == level_data[current_level_data["unlock"]]:
            break

    # for i in l:
        # print(i["content"])
    return l


def scale_image(scale: int, img, old_img_size: Tuple[int, int]) -> pygame.Surface:
    """Scales the image to the responsive size, by keeping the ratio"""
    origin_size = 70  # original tile_size
    rat_x, rat_y = old_img_size
    x = round(rat_x / origin_size * scale)
    y = round(rat_y / origin_size * scale)
    return pygame.transform.scale(img, (x, y))


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(PlayerIcon, self).__init__()
        image = get_ratio_scaled_image(45, SpriteSheet("graphics/sprites/Spritesheet_most.png"), "p1_stand.png")
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    def update(self) -> None:
        self.rect.center = self.pos


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, text, disabled=False):
        super(Node, self).__init__()
        raw_image = pygame.image.load("graphics/picture_Node.png").convert_alpha()
        image = scale_image(8, raw_image, (1790, 994))
        surface = pygame.Surface(image.get_size())
        surface.fill("darkslategrey") if disabled else surface.fill("green4")
        surface.blit(image, (0, 0))
        x, y = image.get_size()
        surface.blit(*self.get_text(text, (10, y//4)))

        self.image = surface
        self.rect = self.image.get_rect(center=pos)


    def get_text(self, text, pos):
        my_font = pygame.font.SysFont("futura", 50)
        color = (140, 00, 140)
        txt_surface = my_font.render(text, True, color)
        txt_rect = txt_surface.get_rect(topleft=pos)
        return txt_surface, txt_rect


class Overworld:
    def __init__(self, screen: pygame.Surface, create_level):
        data = load_level_config()
        self.level_data: Dict[Dict[str]] = data["levels"]   # all data of all levels
        self.level_data_sorted = sort_world(data["levels"], data["settings"]["first_level"]) # level_data in list
        # self.current_level = data["settings"]["first_level"]    # levelname
        self.current_level = self.level_data[data["settings"]["first_level"]]   # all data of current level

        self.current_level_name: str = data["settings"]["first_level"]  # current level name
        self.unlocked_levelname_list: List[str] = [data["settings"]["first_level"]]  # list of all unlocked levelnames

        # print([name["unlock"] for name in self.level_data.values()])
        # self.unlocked_levelname_list.extend([name["unlock"] for name in self.level_data.values()]) # DEBUG

        self.selected = 0   # which level number is selected         # DEBUG
        self.max_level = self.max_level = len(self.unlocked_levelname_list)  # shows how many levels are unlocked    # DEBUG

        self.nodes = pygame.sprite.Group()
        self.icon = pygame.sprite.GroupSingle(PlayerIcon(self.current_level["node_pos"]))

        self.screen = screen

        bg_image = pygame.image.load("graphics/main_screen_background.png").convert()   # TODO CHANGE BACKGROUND
        # self.image = bg_image
        self.image = scale_image(31, bg_image, (3152, 1846))
        self.img_rect = self.image.get_rect()
        self.color = pygame.Color(0, 100, 50)

        self.setup_nodes()

        # movement
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.moving = False

        # communication
        self.create_level = create_level

    def setup_nodes(self):
        # q = self.screen.get_width() // (len(self.level_data)+1)
        for i, node in enumerate(self.level_data.values(), 1):
            x, y = node["node_pos"]
            # print(node["name"])
            self.nodes.add(Node((x, y,), node["name"], disabled=True if i > self.max_level else False))    # TODO find better ways to organize the responsive data

    def draw_lines(self, color="red"):
        positions = [point["node_pos"] for i, point in enumerate(self.level_data.values(), 1) if i <= self.max_level]
        if len(positions) <= 1:
            return
        pygame.draw.lines(self.screen, color, closed=False, points=positions, width=6)

    # def animate(self):
    #     x, y, z, *_ = self.color
    #     x += 1
    #     if x % 2 == 0:
    #         y += 1
    #     if y % 2 == 0:
    #         z += 1
    #     if z >= 255:
    #         y += 1
    #         z = 0
    #     if y >= 255:
    #         x += 1
    #         y = 0
    #     if x >= 255:
    #         x = 0
    #     self.color = pygame.Color(round(x), round(y), round(z))

    def key_input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT or pygame.K_d] and self.selected < self.max_level-1 and self.selected < len(
                    self.nodes)-1:
                self.move_direction = self.get_direction(True)
                self.selected += 1
                self.moving = True
                self.current_level = self.level_data_sorted[self.selected]
                print("Right")
            elif keys[pygame.K_LEFT or pygame.K_a] and self.selected > 0:
                print("left")
                self.move_direction = self.get_direction(False)
                self.selected -= 1
                self.moving = True
                self.current_level = self.level_data_sorted[self.selected]
            elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                print("load Level")
                # print(self.selected)
                print(self.current_level["level_file_name"])
                self.create_level(self.current_level["level_file_name"])

    def unlock_new_level(self):
        if self.current_level_name == self.unlocked_levelname_list[-1]:
            print("unlock new Level")
            next_level = self.current_level["unlock"]
            # print(f"{next_level=}")

            if next_level in self.unlocked_levelname_list:
                # print("nothing to do")
                return False
            print(next_level)
            self.unlocked_levelname_list.append(next_level)
            self.current_level_name = next_level
            self.current_level = self.level_data[next_level]

            self.max_level = len(self.unlocked_levelname_list)
            self.selected += 1
            self.icon.sprite.pos = self.nodes.sprites()[self.selected].rect.center
            self.setup_nodes()
            return True


        else:
            print("no new level to unlock")
        # if next_level and self.selected < self.max_level - 1:
        #     if self.max_level < len(self.level_data_sorted):
        #         self.max_level += 1
        #     self.setup_nodes()
        #     self.selected += 1
        #     self.current_level = self.level_data_sorted[self.selected]
        #     self.icon.sprite.pos = self.nodes.sprites()[self.selected].rect.center


    def move_player_icon(self):
        # l = self.nodes.sprites()
        # self.icon.sprite.rect.center = self.nodes.sprites()[self.selected].rect.center
        if self.moving:
            self.icon.sprite.pos += self.move_direction * self.speed
            if self.icon.sprite.rect.collidepoint(self.nodes.sprites()[self.selected].rect.center):
                self.move_direction = pygame.math.Vector2(0, 0)
                self.moving = False
                self.icon.sprite.pos = self.nodes.sprites()[self.selected].rect.center

    def get_direction(self, right: bool):
        i = 1 if right else -1
        start = pygame.math.Vector2(self.nodes.sprites()[self.selected].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.selected + i].rect.center)
        return (end - start).normalize()

    def run(self):
        self.key_input()
        self.move_player_icon()
        self.icon.update()
        # self.animate()
        self.screen.fill(self.color)
        self.screen.blit(self.image, self.img_rect)

        self.draw_lines()
        self.nodes.draw(self.screen)
        self.icon.draw(self.screen)

