import pygame.sprite

from files.SpriteSheet import SpriteSheet


def load_images(spritesheet: SpriteSheet, size) -> dict:
    animations = {
        'idle': [
            pygame.transform.scale(frame, (size, size)) for frame in (
                spritesheet.get_sprites("p1_front.png", "p1_front.png", "p1_stand.png","p1_stand.png"))
        ],
        'run': [
            pygame.transform.scale(frame, (size, size)) for frame in (
                spritesheet.get_sprites(*[f"p1_walk{i:02d}.png" for i in range(1, 7)]))
        ],
        'jump': [pygame.transform.scale(frame, (size, size)) for frame in (spritesheet.get_sprites("p1_jump.png"))],
    }
    return animations


def load_dust_animation_images() -> dict:
    dust_sheet = SpriteSheet("graphics/animations/dust_particles.png")
    images = {
        "jump": dust_sheet.get_sprites(*[f"jump_{i:01d}.png" for i in range(1, 7)]),
        "land": dust_sheet.get_sprites(*[f"land_{i:01d}.png" for i in range(1, 6)]),
        "run": dust_sheet.get_sprites(*[f"run_{i:01d}.png" for i in range(1, 6)]),
    }
    return images


class Player(pygame.sprite.Sprite):
    def __init__(self,  pos, size, sp_sheet: SpriteSheet, surface: pygame.Surface, particle_method):
        super(Player, self).__init__()
        self.size = size - 2
        self.animations = load_images(sp_sheet, self.size)
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=pos)

        # animations
        self.frame_index = 0
        self.state = "idle"
        self.face_left = False
        # dust particles
        self.dust_particles = load_dust_animation_images()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_particles = particle_method

        self.on_ground = False
        self.health = 100

        # Constants, can changed
        self.max_speed = 4
        self.gravity = 0.8
        self.jump_speed = -16

        # Player movement
        self.speed = self.max_speed
        self.direction = pygame.math.Vector2(0, 0)
        self.on_ladder = False
        self.climbing = False
        self.jump_of_ladder = False

        self.collided_sprites = []  # list saves the sprites the player is colliding

    def get_input(self, scroll):
        keys = pygame.key.get_pressed()

        # left and right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            if self.on_ground:
                self.state = "run"
            self.face_left = False
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (scroll + self.rect.size[0] < self.rect.centerx):
            self.direction.x = -1
            if self.on_ground:
                self.state = "run"
            self.face_left = True

        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ladder:
            # print("ladder up")
            self.direction.y = -2
            self.climbing = True

        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.on_ladder:
            # print("ladder down")
            self.direction.y = 2
            self.climbing = True


        elif keys[pygame.K_SPACE] and self.on_ladder:
            self.on_ladder = False
            self.climbing = False
            self.jump_of_ladder = True

        elif self.on_ladder:    # else statement for on ladder
            self.direction.y = 0
            self.direction.x = 0
            self.climbing = False

        else:
            self.direction.x = 0
            self.state = "idle"
            self.climbing = False

        # jump
        # print(self.on_ground)
        if keys[pygame.K_SPACE] and self.on_ground:
            # print("pressed")
            self.jump(self.jump_speed)
            self.create_particles(self.rect.midbottom)

        if not self.on_ground:
            self.state = "jump"

    def apply_gravity(self):
        if not self.on_ladder:
            self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self, jump_speed):
        self.direction.y = jump_speed
        self.state = "jump"

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.animations[self.state]):
            self.frame_index = 0
        self.image = pygame.transform.flip(
            self.animations[self.state][int(self.frame_index)], self.face_left, False)

    def dust_animation(self):
        if self.state == "run" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_particles["run"]):
                self.dust_frame_index = 0
            dust_size = (self.size//3, self.size//5)
            dust_image = pygame.transform.scale(self.dust_particles["run"][int(self.dust_frame_index)], dust_size)
            # dust_particle: pygame.Surface = pygame.transform.scale(
            #     self.dust_particles["run"][int(self.dust_frame_index)], (self.size//2, self.size//2))

            if not self.face_left:  # Faces right --> going x positive
                dust_particle: pygame.Surface = pygame.transform.flip(dust_image, False, False)
                pos = self.rect.bottomleft - pygame.math.Vector2(-12, 0)

            else:    # Faces right --> going x negative
                dust_particle: pygame.Surface = pygame.transform.flip(dust_image, True, False)
                pos = self.rect.bottomright - pygame.math.Vector2(12, 0)

            p = dust_particle.get_rect(midbottom=pos)
            self.display_surface.blit(dust_particle, p)

        #     pygame.draw.rect(self.display_surface, (0, 255, 0), p, 1)  # Borders dust
        # pygame.draw.rect(self.display_surface, (255, 255, 255), self.rect, 1)  # Borders player

    def get_hurt(self, damage):
        self.health -= damage
        print("damage", self.health)

    def update(self, scroll) -> None:
        self.get_input(scroll)
        self.animate()
        self.dust_animation()


