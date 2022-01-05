import sys

import pygame
from pygame import colordict

pygame.init()
tile_size = 35
p_old = pygame.Vector2(0, 0)
other_size = tile_size+2
faktor_x = 40
faktor_y = len(pygame.colordict.THECOLORS.items()) // faktor_x + 1
print(faktor_y)
w, h = faktor_x , faktor_y
screen = pygame.display.set_mode((other_size * faktor_x +10, other_size*faktor_y))
clock = pygame.time.Clock()
Matrix = [["NULL" for x in range(w+1)] for y in range(h+1)]
for i, v in enumerate(pygame.colordict.THECOLORS.items()):
    name, color = v
    x, y = i % faktor_x, i // faktor_x
    s = pygame.Surface((tile_size, tile_size))
    s.fill(color)
    r = s.get_rect(topleft=(x*other_size, y*other_size))
    screen.blit(s, r)
    Matrix[y][x] = name

    if name == "mediumspringgreen":
        print(x, y)

print(Matrix)
pygame.display.update()
clock.tick(1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("exit")
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            # x, y = event.pos
            # x = x // 40
            # y = y // 40
            # print(x, y)
            p = pygame.Vector2(event.pos)
            p = p // other_size
            if p != p_old:
                x, y = p.xy
                x = int(x)
                y = int(y)
                print(Matrix[int(y)][int(x)], (x, y))
            p_old = p


