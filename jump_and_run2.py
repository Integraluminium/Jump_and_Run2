from typing import *
import json
import sys
import pygame

from files.level import Level
from files.overworld import Overworld


class JumpAndRun:
    ROWS = 16
    SCREEN_WIDTH = 1200
    FPS = 60

    def __init__(self):
        pygame.init()

        def load_config():
            with open(f"config.json", "r") as f:
                data = json.load(f)
            return data["tile_size"]

        self.TILE_SIZE = load_config()
        self.SCREEN_HEIGHT = self.TILE_SIZE * self.ROWS     # Tile_size in config from 30 - 50
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Jump'n Run2")     # TODO Icon
        # pygame.mouse.set_visible(False)

        self.scroll = 0


        # Images


        # self.backgrounds = load_background()
        self.status = "overworld"
        self.overworld = Overworld(self.screen, self.create_level)
        self.level = None   # Level("level5.json", self.screen)

    def create_level(self, current_level):
        # self.level = Level("level5.json", self.screen)
        self.level = Level(current_level, self.screen, self.get_back)
        self.status = "level"

    def get_back(self, next_level: bool):   # TODO entweder nach jedem Level zurück
        # TODO in die Lobby oder weiter ins nächste Level?
        # print(f"{next_level=}")
        if next_level:  # and self.overworld.selected < self.overworld.max_level-1:
            if not self.overworld.unlock_new_level():
                # print("ok")
                self.status = "overworld"
                return
            self.create_level(self.overworld.current_level["level_file_name"])
        else:
            self.status = "overworld"

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exit")
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.event_loop()

            self.screen.fill((0, 255, 0))

            # self.status = ""    # TODO DEBUG

            if self.status == "overworld":
                self.overworld.run()
            else:
                self.level.run()
                self.level.draw(self.screen)

            pygame.display.update()
            self.clock.tick(self.FPS)


def main():
    game = JumpAndRun()
    game.run()


if __name__ == '__main__':
    main()
