import random
import pygame.sprite
from files.SpriteSheet import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, sprite_sheet: SpriteSheet, *files, animation_speed: float = 0.2):
        super(Enemy, self).__init__()
        self.image = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        self.image.fill("red")  # TODO Enemy is not finished
        self.rect = self.image.get_rect(topleft=pos)
        self.collide_rect = self.rect

        self.frames = sprite_sheet.get_sprites(*files)

        self.animation_speed = animation_speed
        self.frame_index = 0

    def animate(self):
        self.frame_index += self.animation_speed
        if int(self.frame_index) > len(self.frames)-1:
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        # print(self.frame_index)

    def update(self, scroll) -> None:
        self.animate()
        self.rect.x += scroll
        self.collide_rect.x += scroll


class Slime(Enemy):
    def __init__(self, pos, size, sprite_sheet, name="slime"):
        # (f"{name}.png", f"{name}_dead.png", f"{name}_hit.png", f"{name}_squashed.png", f"{name}_walk.png")
        super(Slime, self).__init__(pos, size, animation_speed=0.035, sprite_sheet=sprite_sheet)

        self.frames = get_ratio_images(round(size*1.25), sprite_sheet, f"{name}.png", f"{name}_walk.png")
        self.dead = get_ratio_scaled_image(size, sprite_sheet, f"{name}_squashed.png")

        self.image = self.frames[1]
        get_ratio_scaled_image(size, sprite_sheet, f"{name}.png")

        # self.tile_rect = pygame.rect.Rect(pos, (size, size))
        # self.collide_rect = self.image.get_rect(midbottom=self.tile_rect.midbottom)
        # # self.rect is updating itself in the animation
        self.height_attributes = pos[1], size
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.y += size-self.rect.height

        self.speed = random.choice((random.randint(9, 15), -1*random.randint(9, 15)))

    def move(self):
        # self.tile_rect.x += round(self.speed/10)
        self.rect.x += round(self.speed/10)

    def reverse(self):
        self.speed *= -1

    def animate(self):
        self.frame_index += self.animation_speed
        if int(self.frame_index) > len(self.frames)-1:
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

        # print(self.frame_index)

    def update(self, scroll) -> None:
        self.animate()
        self.move()
        # self.rect = self.image.get_rect(midbottom=self.tile_rect.midbottom)
        self.rect.x += scroll
        self.rect.y = self.height_attributes[0] + self.height_attributes[1] - self.image.get_height()
        # self.tile_rect.x += scroll
        self.collide_rect = self.rect
