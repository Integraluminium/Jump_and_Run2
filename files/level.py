from typing import *
import json
import pygame.sprite

from files.tiles import *
from files.player import Player
from files.SpriteSheet import SpriteSheet
from files.particles import ParticleEffect
from files.enemy import *


def load_background() -> List[pygame.Surface]:
    sky_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/sky_cloud.png").convert_alpha())
    mountain_img = pygame.transform.scale2x(
        pygame.image.load("./graphics/background/mountain2.png").convert_alpha())
    pine1_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/pine1.png").convert_alpha())
    pine2_img = pygame.transform.scale2x(pygame.image.load("./graphics/background/pine2.png").convert_alpha())
    return [sky_img, mountain_img, pine1_img, pine2_img]


def load_config():
    with open(f"config.json", "r") as f:
        data = json.load(f)
    return data["tile_size"]


def load_level_file(file_name: str) -> [dict, list]:
    try:
        with open(f"levels/{file_name}", "r") as f:
            data = json.load(f)
        world_data = {
            "author": data["author"],
            "level_name": data["name"],
            "next_level": data["next_level"]
        }
        return world_data, data["level_data"]
    except FileNotFoundError as e:
        print(e)


def get_static_tiles() -> dict:
    with open("files/static_tiles.json") as f:
        static_tiles = json.load(f)
    return static_tiles


class Level:
    def __init__(self, file_name, surface: pygame.Surface, get_back):
        self.display_surface = surface
        self.meta_data, self.level_data = load_level_file(file_name)
        self.tile_size = load_config()

        self.sprite_sheet = SpriteSheet("graphics/sprites/Spritesheet_most.png")
        self.backgrounds = load_background()
        self.world_shift = 0
        self.SCROLL = 0

        self.player_was_on_ground = False

        # Groups
        self.player = pygame.sprite.GroupSingle(
            Player((0, 0), self.tile_size, self.sprite_sheet, self.display_surface, self.create_jump_particles))
        self.tile_sprites = pygame.sprite.Group()
        self.decoration_sprites = pygame.sprite.Group()
        self.crate_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.springboard_group = pygame.sprite.Group()
        self.spike_group = pygame.sprite.Group()
        self.flag_group = pygame.sprite.Group()
        self.ladder_group = pygame.sprite.Group()

        self.enemy_group = pygame.sprite.Group()
        self.blocker_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()

        self.dust_sprite = pygame.sprite.GroupSingle()

        # end init
        self.parse_level(self.level_data)  # parses the level into the groups

        # method
        self.get_back = get_back

        self.keys = pygame.key.get_pressed()    # DEBUG for next level

    def parse_level(self, level_data: dict):
        enemy_sp_sheet = SpriteSheet("graphics/enemys/enemys.png")
        static_tiles = get_static_tiles()

        if type(level_data) == dict:
            for name, layer in level_data.items():
                # print(layer)
                self.parse_layer(enemy_sp_sheet, layer, name, static_tiles)

        else:   # Compatability with former level format
            self.parse_layer(enemy_sp_sheet, level_data, "Layer1", static_tiles)

    def parse_layer(self, enemy_sp_sheet, layer, name, static_tiles):
        for row_index, row in enumerate(layer):
            for tile_index, cell in enumerate(row):
                x = tile_index * self.tile_size
                y = row_index * self.tile_size
                size = self.tile_size
                sp_sheet = self.sprite_sheet
                pos = (x, y)
                # print(static_tiles["tiles_with_collision"])

                if name == "layer4":
                    self.background_group.add()

                if cell == "0000":  # air
                    continue

                elif cell in static_tiles["tiles_with_collision"]:  # static tiles like grass or dirt
                    self.tile_sprites.add(StaticTile(
                        pos=pos, size=size, sp_sheet=sp_sheet,
                        file=static_tiles["tiles_with_collision"][cell]["image"]))

                elif cell in static_tiles["half_tiles"]:  # static tiles like grass or dirt
                    self.tile_sprites.add(HalfStaticTile(
                        pos=pos, size=size, sp_sheet=sp_sheet,
                        file=static_tiles["half_tiles"][cell]["image"]))

                elif cell in static_tiles["decoration"]:  # decoration TODO Change ID to complete 19xx, now 19xx and
                    # TODO and 2000 -2003, 2015 - 2019
                    self.decoration_sprites.add(StaticTile(
                        pos=pos, size=size, sp_sheet=sp_sheet,
                        file=static_tiles["decoration"][cell]["image"]))

                elif cell in static_tiles["box"]:  # gold and silver coins, gems  1900 - 1909 reserved
                    data = static_tiles["box"][cell]
                    self.crate_group.add(Crate(pos, size, sp_sheet=sp_sheet, file=data["image"]))

                elif cell in static_tiles["coins"]:  # gold and silver coins, gems
                    data = static_tiles["coins"][cell]
                    self.coin_group.add(Coin(pos, size, sp_sheet=sp_sheet, file=data["image"], value=data["value"]))

                elif cell in static_tiles["liquid"]:  # liquid 1800 - 1805
                    self.lava_group.add(Liquid(
                        pos=pos, size=size, sp_sheet=sp_sheet,
                        file_name=static_tiles["liquid"][cell]["image"]))

                elif cell in static_tiles["ladder"]:  # ladder 1810 - 1811
                    data = static_tiles["ladder"][cell]
                    t = True if data["ladder_type"] == "top" else False
                    self.ladder_group.add(Ladder(pos, size, data["image"], sp_sheet, t))

                elif cell in static_tiles["flags"]:  # flags 2010 - 2013
                    data = static_tiles["flags"][cell]
                    self.flag_group.add(Flag(pos, size, sp_sheet, data["color"]))

                elif cell == "2022":
                    self.springboard_group.add(Springboard(pos, size, "springboardUp.png", sp_sheet))

                elif cell == "2020":
                    self.spike_group.add(Spikes(pos, size, "spikes.png", sp_sheet))

                elif cell == "0005":
                    self.enemy_group.add(Slime(pos, size, enemy_sp_sheet, name="slime"))
                elif cell == "0006":
                    self.enemy_group.add(Slime(pos, size, enemy_sp_sheet, name="slimeBlue"))
                elif cell == "0007":
                    self.enemy_group.add(Slime(pos, size, enemy_sp_sheet, name="slimeGreen"))
                elif cell == "0004":
                    self.blocker_group.add(Tile(pos, size))

                elif cell == "0001":  # Player
                    self.player.sprite.rect.topleft = (x, y)

                elif cell == "1904":
                    self.exit_group.add(Door(pos, size, sp_sheet, True))

                elif cell == "1903":
                    self.tile_sprites.add(Log(pos, size, sp_sheet=sp_sheet, file="bridgeLogs.png"))

                else:  # debug, shows other tiles
                    self.decoration_sprites.add(StaticTile(
                        pos=pos, size=size, sp_sheet=sp_sheet,
                        file="bomb.png"))
            # print(row)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        max_speed = player.max_speed
        screenwidth, _ = self.display_surface.get_size()

        if player_x < screenwidth//4 and direction_x < 0 < self.SCROLL:
            self.world_shift = 1 * max_speed
            player.speed = 0
        elif player_x > screenwidth-(screenwidth//4) and direction_x > 0:
            self.world_shift = -1 * max_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 1 * max_speed

    def draw_bg(self, screen):
        screen.fill("mediumspringgreen")
        _, sr_height = self.display_surface.get_size()
        sky_img, mountain_img, pine1_img, pine2_img, *_ = self.backgrounds
        width = sky_img.get_width()
        self.SCROLL -= self.world_shift
        scroll = self.SCROLL
        for x in range(5):
            screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
            screen.blit(mountain_img, ((x * width) - scroll * 0.6, sr_height - mountain_img.get_height() - 300))
            screen.blit(pine1_img, ((x * width) - scroll * 0.7, sr_height - pine1_img.get_height() - 150))
            screen.blit(pine2_img, ((x * width) - scroll * 0.8, sr_height - pine2_img.get_height()))

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tile_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                # horizontal
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

        for crate in self.crate_group.sprites():
            # TODO Buggy, can glitch into other tilings or player can bug through the box
            if crate.rect.colliderect(player.rect):
                crate.offset = player.direction.x * player.speed
                crate.moving = True

            else:
                crate.offset = 0
                crate.moving = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tile_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                # vertical
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

        for sprite in self.crate_group.sprites():
            if sprite.rect.colliderect(player.rect) and not sprite.moving:
                # vertical
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True


        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def create_jump_particles(self, pos):
        player = self.player.sprite
        dust_size = (int(player.size * 0.5), int(player.size * 0.25))
        particles = [pygame.transform.scale(img, dust_size) for img in player.dust_particles["jump"]]
        jump_particle_sprite = ParticleEffect(pos, particles)
        self.dust_sprite.add(jump_particle_sprite)
        # pygame.draw.rect(self.display_surface, (0, 0, 255), jump_particle_sprite.rect, 1)  # Borders dust

    def create_landing_particles(self):
        player = self.player.sprite
        if not self.player_was_on_ground and player.on_ground and not self.dust_sprite.sprites():
            dust_size = (int(player.size * 1), player.size // 3)
            particles = [pygame.transform.scale(img, dust_size) for img in player.dust_particles["land"]]
            fall_particle_sprite = ParticleEffect(player.rect.midbottom, particles)
            self.dust_sprite.add(fall_particle_sprite)

            # pygame.draw.rect(self.display_surface, (0, 0, 255), fall_particle_sprite.rect, 1)  # Borders dust

    def enemy_movement_collision(self):
        for enemy in self.enemy_group.sprites():
            for sprite in self.tile_sprites.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    # horizontal
                    enemy.reverse()
            for blocker in self.blocker_group.sprites():
                if blocker.rect.colliderect(enemy.rect):
                    enemy.reverse()
        # TODO STOPPER, enemys are running away

    def check_player_death(self) -> bool:
        if self.player.sprite.rect.top > self.display_surface.get_height()*1.05:
            return True
        elif group := pygame.sprite.spritecollide(self.player.sprite, self.lava_group, dokill=False):
            print("LAVA")
            for sprite in group:
                if self.player.sprite.rect.colliderect(sprite.collide_rect):
                    return True
        return False

    def check_player_hurt(self):
        if group := pygame.sprite.spritecollide(self.player.sprite, self.spike_group, dokill=False):
            # print("spike")
            already_collided = self.player.sprite.collided_sprites.copy()
            self.player.sprite.collided_sprites.clear()
            # print(already_collided, self.player.sprite.collided_sprites)
            for sprite in group:
                if self.player.sprite.rect.colliderect(sprite.collide_rect):
                    self.player.sprite.collided_sprites.append(sprite)
                    if sprite not in already_collided:
                        self.player.sprite.get_hurt(10)
                        # print("spike")
        else:
            self.player.sprite.collided_sprites.clear()

        if group := pygame.sprite.spritecollide(self.player.sprite, self.enemy_group, dokill=False):
            # print("blob")
            for sprite in group:
                if self.player.sprite.rect.colliderect(sprite.collide_rect):
                    pass

    def check_collision_flag(self):
        if group := pygame.sprite.spritecollide(self.player.sprite, self.flag_group, dokill=False):
            for sprite in group:
                if self.player.sprite.rect.colliderect(sprite.collide_rect):
                    sprite.trigger()

    def check_collision_ladder(self):
        if group := pygame.sprite.spritecollide(self.player.sprite, self.ladder_group, dokill=False):
            # print("ladder", self.player.sprite.on_ladder)
            player = self.player.sprite
            for sprite in group:
                if self.player.sprite.rect.colliderect(sprite.rect) and not player.jump_of_ladder:
                    self.player.sprite.on_ladder = True
                    self.player.sprite.state = "idle"   # TODO change
                    player_y0 = int((player.rect.centery+player.rect.bottom)/2)
                    player_y1 = player.rect.bottom
                    # print(sprite.top, sprite.rect.top, (player_y0, player_y1), sprite.rect.top in range(player_y0, player_y1) ,"asdf")
                    if sprite.top and sprite.rect.top in range(player_y0, player_y1) and not player.climbing:
                        # print("ladder_top")
                        self.player.sprite.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
        else:
            self.player.sprite.on_ladder = False
            self.player.sprite.jump_of_ladder = False
            # print("Reset")

    def check_player_win(self) -> bool:
        if group := pygame.sprite.spritecollide(self.player.sprite, self.exit_group, dokill=False):
            # print("win")
            for sprite in group:
                if self.player.sprite.rect.collidepoint(sprite.collide_rect.center):
                    return True
        return False

    def check_player_get_coin(self):
        if group := pygame.sprite.spritecollide(self.player.sprite, self.coin_group, dokill=True):
            # print("coin")
            for sprite in group:
                if self.player.sprite.rect.colliderect(sprite.collide_rect):
                    return True
        return False

    def check_player_spring_board(self):
        success = False
        if group := pygame.sprite.spritecollide(self.player.sprite, self.springboard_group, dokill=False):
            # print("springboard")
            for sprite in group:
                if self.player.sprite.rect.colliderect(sprite.rect):
                    sprite.trigger()
                    success = True
        return success

    def hud(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.get_back(False)

        self.keys = keys

    def run(self):
        self.hud()  # check key_input
        self.player_was_on_ground = True if self.player.sprite.on_ground else False  # was player on ground?

        if self.check_player_death():
            self.get_back(False)

        self.check_player_hurt()
        if self.check_player_win():
            self.get_back(True)

        if self.check_player_get_coin():
            pass

        if self.check_player_spring_board():
            self.player.sprite.jump(-22)
        self.check_collision_flag()
        # self.check_collision_ladder()




    def draw(self, screen):
        # bg images
        self.draw_bg(screen)

        # level tiles
        self.tile_sprites.update(self.world_shift)
        self.tile_sprites.draw(screen)
        self.scroll_x()

        #   decoration
        self.decoration_sprites.update(self.world_shift)
        self.decoration_sprites.draw(screen)

        # crates
        self.crate_group.update(self.world_shift)
        self.crate_group.draw(screen)

        # lava
        self.lava_group.update(self.world_shift)
        self.lava_group.draw(screen)

        # springboard
        self.springboard_group.update(self.world_shift)
        self.springboard_group.draw(screen)
        # spikes
        self.spike_group.update(self.world_shift)
        self.spike_group.draw(screen)
        # flags
        self.flag_group.update(self.world_shift)
        self.flag_group.draw(screen)

        # ladder
        self.ladder_group.update(self.world_shift)
        self.ladder_group.draw(screen)

        # exit
        self.exit_group.update(self.world_shift)
        self.exit_group.draw(screen)

        # coins
        self.coin_group.update(self.world_shift)
        self.coin_group.draw(screen)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player
        self.player.update(self.world_shift)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.check_collision_ladder()
        self.create_landing_particles()     # dust animation
        self.player.draw(screen)

        # enemy
        self.enemy_group.update(self.world_shift)
        self.enemy_group.draw(screen)
        self.enemy_movement_collision()
        self.blocker_group.update(self.world_shift)

        return


        for enemy in self.enemy_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 255, 255), enemy.rect, 1)   # border tiles rect
            pygame.draw.rect(self.display_surface, (255, 0, 0), enemy.collide_rect, 1)   # border tiles rect

        for blocker in self.blocker_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 0, 0), blocker.rect, 2)

        for tile in self.tile_sprites.sprites():
            pygame.draw.rect(self.display_surface, (0, 0, 255), tile.rect, 1)   # border tiles rect
        for tile in self.springboard_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 255, 255), tile.rect, 1)   # border tiles rect
        for tile in self.coin_group.sprites():
            pygame.draw.rect(self.display_surface, (255, 255, 255), tile.rect, 1)   # border tiles rect
            pygame.draw.rect(self.display_surface, (255, 0, 0), tile.collide_rect, 1)   # border tiles rect
        for tile in self.spike_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 255, 255), tile.rect, 1)   # border tiles rect
            pygame.draw.rect(self.display_surface, (255, 0, 0), tile.collide_rect, 1)   # border tiles rect
        for tile in self.flag_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 255, 255), tile.rect, 1)   # border tiles rect
            pygame.draw.rect(self.display_surface, (255, 0, 0), tile.collide_rect, 1)   # border tiles rect

        for tile in self.ladder_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 255, 255), tile.rect, 1)   # border tiles rect
            # pygame.draw.rect(self.display_surface, (255, 0, 0), tile.collide_rect, 1)   # border tiles rect
        for tile in self.exit_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 255, 255), tile.rect, 1)  # border tiles rect
            pygame.draw.rect(self.display_surface, (255, 0, 0), tile.collide_rect, 1)  # border tiles rect

        for tile in self.lava_group.sprites():
            pygame.draw.rect(self.display_surface, (0, 100, 255), tile.rect, 1)  # border tiles rect
            pygame.draw.rect(self.display_surface, (0, 0, 10), tile.collide_rect, 1)  # border tiles rect
        
