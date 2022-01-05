from typing import List
import pygame.sprite


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, particle_images: List[pygame.Surface]):
        super(ParticleEffect, self).__init__()
        self.pos = pos
        self.frames = particle_images
        self.frame_index = 0
        self.animation_speed = 0.5

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > len(self.frames)-1:
            self.kill()
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift) -> None:
        self.animate()
        self.rect.x += x_shift

