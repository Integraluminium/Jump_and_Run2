from typing import *
import json
import pygame
from typing import List, Dict


class SpriteSheet:
    def __init__(self, filename, color_key=(0, 0, 0)):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.color_key = color_key
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()
        # print("load Spritesheet")   # TODO DEBUG

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        # sprite.set_colorkey(self.color_key)
        sprite.blit(self.sprite_sheet, (0, 0), pygame.Rect(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image

    def get_sprites(self, *names: str) -> List[pygame.Surface]:
        return [self.parse_sprite(str(name)) for name in names]

    def get_ratio(self, name) -> Dict[str, int]:
        return self.data['frames'][name]['sourceSize']


def scale_img(size: Tuple[int, int], *images: pygame.Surface) -> List[pygame.Surface]:
    return [pygame.transform.scale(img, size) for img in images]


def get_ratio_scaled_image(base_size: int, sprite_sheet: SpriteSheet, name: str) -> pygame.Surface:
    """Scales the image to the responsive size, by keeping the ratio"""
    origin_size = 70    # original tile_size
    img = sprite_sheet.parse_sprite(name)
    rat_x, rat_y = sprite_sheet.get_ratio(name).values()
    x = round(rat_x/origin_size*base_size)
    y = round(rat_y/origin_size*base_size)
    return pygame.transform.scale(img, (x, y))


def get_ratio_images(base_size: int, sprite_sheet: SpriteSheet, *names: str) -> List[pygame.Surface]:
    return [get_ratio_scaled_image(base_size, sprite_sheet, img_name) for img_name in names]

