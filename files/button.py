import pygame


class Button:  # needs Pygame
    def __init__(self, x, y, image, hovered_image=False):
        self.x = x
        self.y = y
        self.normal_image = image
        self.hovered_image = hovered_image
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.clicked = False

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)
        return self.check_collision()

    def check_collision(self):
        clicked = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.hovered_image:
                self.image = self.hovered_image
            if pygame.mouse.get_pressed(3)[0] == 1 and self.clicked == False:
                clicked = True
                # print("CLICKED")

        if pygame.mouse.get_pressed(3)[0] == 0:
            self.clicked = False

        return clicked


class Button2(Button):
    def __init__(self, x, y, image, hovered_image = False):
        super(Button2, self).__init__(x, y, image=image, hovered_image=hovered_image)
        self.rect = self.image.get_rect(topleft=(x, y))


class ToggleButton(Button):
    def __init__(self, x, y, image, toggled_image, hovered_image=False, hovered_toggled_image=False):
        super(ToggleButton, self).__init__(x, y, image, hovered_image=False)

        self.normal_image = image
        self.toggled_image = toggled_image

        self.hovered_image = hovered_image
        self.hovered_toggled_image = hovered_toggled_image
        self.clicked = False
        self.state = False

        self.image = self.normal_image

    def draw(self, screen: pygame.surface.Surface):
        if not self.state:
            self.image = self.normal_image
            # print("normal")
        else:
            self.image = self.toggled_image
            # print("toggled")

        screen.blit(self.image, self.rect)
        self.check_collision()
        return self.state

    def check_collision(self):
        clicked = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.hovered_image:
                self.image = self.hovered_image
            if pygame.mouse.get_pressed(3)[0] == 1 and not self.clicked:
                clicked = True
                # print("CLICKED")
                self.state = not self.state
                self.clicked = True

        if pygame.mouse.get_pressed(3)[0] == 0:
            # print("not clicked")
            self.clicked = False

        return clicked