import pygame
from files.SpriteSheet import SpriteSheet, get_ratio_scaled_image, get_ratio_images, scale_img


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super(Tile, self).__init__()
        self.image = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        # self.image.fill("grey")
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, scroll) -> None:
        self.rect.x += scroll


class StaticTile(Tile):     # loads all static images with collisions
    def __init__(self, pos, size, file, sp_sheet):
        super(StaticTile, self).__init__(pos, size)
        self.image = pygame.transform.scale(sp_sheet.parse_sprite(file), (size, size))


class HalfStaticTile(Tile):
    def __init__(self, pos, size: int, file, sp_sheet):
        super(Tile, self).__init__()
        self.image = pygame.transform.scale(sp_sheet.parse_sprite(file), (size, size))
        # print(self.image.get_size())
        ov = pygame.math.Vector2(pos)
        rv = pygame.math.Vector2(size, int(size * 0.6))
        self.rect = pygame.rect.Rect(ov, rv)


class Crate(StaticTile):
    def __init__(self, pos, size, file, sp_sheet):  # TODO make Box smaller, evtl
        super(Crate, self).__init__(pos, size, file, sp_sheet)
        self.offset = 0
        self.moving = False

    def update(self, scroll) -> None:
        # self.offset = 1
        # print(self.offset)
        self.rect.x += (scroll + int(self.offset))


class Coin(StaticTile):
    def __init__(self, pos, size, file, sp_sheet, value):  # TODO make Coin rotating
        super(Coin, self).__init__(pos, size, file, sp_sheet)
        self.value = value
        rv = pygame.math.Vector2(int(size*0.5), int(size * 0.5))
        self.collide_rect = pygame.rect.Rect((0, 0), rv)
        self.collide_rect.center = self.rect.center

    def update(self, scroll) -> None:
        self.rect.x += scroll
        self.collide_rect.x += scroll


class Springboard(StaticTile):
    def __init__(self, pos, size, file, sp_sheet: SpriteSheet):
        super(Springboard, self).__init__(pos, size, file, sp_sheet)
        self.frames = [pygame.transform.scale(img, (size, size)) for
                       img in sp_sheet.get_sprites("springboardUp.png", "springboardDown.png")]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.triggered = False
        self.animation_index = 0

    def animation(self):
        if self.triggered:
            self.animation_index += 0.2
            if self.animation_index > 1:
                self.animation_index = 0
                self.image = self.frames[0]
                self.triggered = False

    def trigger(self):
        self.triggered = True
        self.image = self.frames[1]
        self.animation_index = 0

    def update(self, scroll) -> None:
        self.animation()
        self.rect.x += scroll


class Spikes(StaticTile):
    def __init__(self, pos, size, file, sp_sheet):
        super(Spikes, self).__init__(pos, size, file, sp_sheet)
        # ov = pygame.math.Vector2(pos[0], pos[1]+size)
        rv = pygame.math.Vector2(size, int(size * 0.5))
        # self.rect = pygame.rect.Rect(ov, rv)
        # self.image = pygame.transform.scale(sp_sheet.parse_sprite(file), (size, size))
        self.collide_rect = pygame.rect.Rect((0, 0), rv)
        self.collide_rect.midbottom = self.rect.midbottom

    def update(self, scroll) -> None:
        self.rect.x += scroll
        self.collide_rect.x += scroll


class Ladder(StaticTile):
    def __init__(self, pos, size, file, sp_sheet, top: bool = False):
        super(Ladder, self).__init__(pos, size, file, sp_sheet)
        self.top = top


class Door(Tile):
    def __init__(self, pos, size, sp_sheet, closed=True):
        super(Door, self).__init__(pos, size)
        filename_part = "closed" if closed else "open"
        self.images = get_ratio_images(size, sp_sheet, f"door_{filename_part}Mid.png", f"door_{filename_part}Top.png")
        x, y = pos
        width, height = self.images[0].get_size()
        self.rect = pygame.Rect((x, y-size), (width, height*2))
        img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        img.blit(self.images[0], (0, height))
        img.blit(self.images[1], (0, 0))
        self.image = img
        self.collide_rect = pygame.Rect((x, y-(size//2)), (width, int(height*1.5)))

    def update(self, scroll) -> None:
        self.rect.x += scroll
        self.collide_rect.x += scroll



class AnimatedTile(Tile):
    def __init__(self, pos, size, sp_sheet: SpriteSheet, file_names: [tuple, list], animation_speed: float = 0.2):
        super(AnimatedTile, self).__init__(pos, size)
        self.frames = [pygame.transform.scale(img, (size, size)) for img in sp_sheet.get_sprites(*file_names)]
        self.frame_index = 0

        self.animation_speed = animation_speed

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        # print(self.frame_index)

    def update(self, scroll) -> None:
        self.animate()
        self.rect.x += scroll


class Liquid(AnimatedTile):
    def __init__(self, pos, size, sp_sheet, file_name):
        super(Liquid, self).__init__(pos, size, sp_sheet, (), animation_speed=0.025)
        # self.frames = [pygame.transform.scale(sp_sheet.parse_sprite(file_name), (size, size))]
        self.frames = get_ratio_images(size, sp_sheet, file_name)
        self.frames.append(pygame.transform.flip(self.frames[0], True, False))
        self.image = self.frames[0]
        # print(self.image.get_size())
        self.collide_rect = pygame.Rect((0, 0), (size, round(2/3*size)))
        self.collide_rect.midbottom = self.rect.midbottom
        # print(self.collide_rect)
        # self.collide_rect.height = round(2/3*size)


class Flag(AnimatedTile):
    def __init__(self, pos, size, sp_sheet, color):
        super(Flag, self).__init__(pos, size, sp_sheet, (f"flag{color}.png", f"flag{color}2.png"), animation_speed=0.1)
        self.image = pygame.transform.scale(sp_sheet.parse_sprite(f"flag{color}Hanging.png"), (size, size))

        # Rectangle Collision player
        rv = pygame.math.Vector2(int(size * 0.5), size)
        self.collide_rect = pygame.rect.Rect((0, 0), rv)
        self.collide_rect.bottomleft = self.rect.bottomleft

        # status
        self.triggered = False

    def animate(self):
        if self.triggered:
            self.frame_index += self.animation_speed
            if self.frame_index > len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]
            # print(int(self.frame_index), self.frames)

    def trigger(self):
        self.triggered = True

    def update(self, scroll) -> None:
        self.animate()
        self.rect.x += scroll
        self.collide_rect.x += scroll


class Log(Tile):
    def __init__(self, pos, size: int, file, sp_sheet):
        super(Tile, self).__init__()
        surface = pygame.transform.scale(sp_sheet.parse_sprite(file), (size, size))
        x, y = pos
        # y += int(size * 0.6)
        ov = pygame.math.Vector2(x, y)
        rv = pygame.math.Vector2(size, int(size * 0.4))

        sprite = pygame.Surface(rv, pygame.SRCALPHA)
        sprite.blit(surface, (0, 0), pygame.Rect((0, int(size * 0.6)), rv))
        self.image = sprite
        print(self.image.get_size())
        self.rect = pygame.rect.Rect(ov, rv)

