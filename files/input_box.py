from typing import *
import sys

import pygame

pygame.init()


class Element:      # Superior class
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    COLOR_DISABLED = pygame.Color(200, 200, 200)
    COLOR_BACKGROUND = pygame.Color(150, 150, 150)
    COLOR_TEXT = pygame.Color(0, 0, 0)
    COLOR_BORDER = pygame.Color(0, 0, 0)
    my_font = pygame.font.SysFont("futura", 30)

    def __init__(self, x, y, w=340, h=32, text="", text_color="black", color=None, top_left_corner_surface=(0, 0),
                 font=None):
        # relative
        self.size = (w, h)
        self.pos = (x, y)
        self.surface = pygame.Surface((w, h))
        self.rect = self.surface.get_rect(center=(x, y))
        # absolute
        # print(top_left_corner_surface, "element")
        self.support_point = top_left_corner_surface
        if top_left_corner_surface != (0, 0):
            self.calculate_abs_pos()
        self.abs_rect = None
        self.calculate_abs_pos()

        # Color
        self.color = InputField.COLOR_INACTIVE
        self.text_color = pygame.color.Color(text_color)

        # Text
        self.txt_surface = InputField.my_font.render(text, True, self.text_color)
        self.txt_rect = self.txt_surface.get_rect(center=self.rect.center)

        # var
        self.active = False
        self.disabled = False
        self.click = False

    def calculate_abs_pos(self):
        pos_x, pos_y = self.rect.topleft
        rel_x, rel_y = self.support_point
        w, h = self.size

        abs_rect = pygame.Rect(rel_x * 0 + pos_x, rel_y * 0 + pos_y, w, h)
        abs_rect.topleft = (rel_x + pos_x, rel_y + pos_y)
        self.abs_rect = abs_rect

    def set_abs_pos(self, topleft_corner_super: Tuple[int, int]):
        self.support_point = topleft_corner_super
        self.calculate_abs_pos()

    def handle_event(self, eventloop_event: pygame.event) -> bool:
        raise NotImplementedError("this Class is a super Class, it is not supposed to use this Class")
        # return self.active

    def _update_self_box(self):
        pass

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def draw(self, surface_screen):
        self._update_self_box()
        surface_screen.blit(self.surface, self.rect)

class ButtonBox:
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    COLOR_BACKGROUND = pygame.Color(150, 150, 150)
    COLOR_TEXT = pygame.Color(0, 0, 0)
    COLOR_BORDER = pygame.Color(0, 0, 0)
    my_font = pygame.font.SysFont("futura", 30)

    def __init__(self, x, y, w, h, elements: dict, text="", font=None):
        # Positions
        self.surface = pygame.Surface((w, h))
        self.rect = self.surface.get_rect(center=(x, y))

        # Color
        self.color = ButtonBox.COLOR_TEXT

        # Text
        self._text_list = list(text.strip().split("/n"))
        if font is None:
            font = ButtonBox.my_font
        else:
            font = font
        self.texts = []
        for i, text in enumerate(self._text_list):
            txt_surface = font.render(text, True, self.color, None)
            txt_rect = txt_surface.get_rect(topleft=(25, 25+50*i))
            self.texts.append((txt_surface, txt_rect))

        # elements
        self.elements = elements
        for element in self.elements.values():   # calculate the absolute position of every element
            element.set_abs_pos(self.rect.topleft)

    def update_self_box(self):
        self.surface.fill(ButtonBox.COLOR_BACKGROUND)
        pygame.draw.rect(self.surface, ButtonBox.COLOR_BORDER, self.surface.get_rect(), 3)

        for element in self.elements.values():
            element.draw(self.surface)
        for text, text_rect in self.texts:
            self.surface.blit(text, text_rect)

    def draw(self, surface_screen):
        self.update_self_box()
        surface_screen.blit(self.surface, self.rect)

    def handle_box_events(self, eventloop_event) -> dict:
        event_log = {}
        for name, element in self.elements.items():
            event_log[name] = element.handle_event(eventloop_event)
        return event_log


class Button(Element):
    def __init__(self, x, y, w=340, h=32, text="", text_color="black", active=False, disabled=False,
                 top_left_corner_surface=(0, 0)):
        super(Button, self).__init__(x, y, w, h, text, text_color, top_left_corner_surface=top_left_corner_surface)
        # relative
        # self.size = (w, h)
        # self.pos = (x, y)
        # self.surface = pygame.Surface((w, h))
        # self.rect = self.surface.get_rect(center=(x, y))
        # # absolute
        # self.support_point = top_left_corner_surface
        # self.abs_rect = None
        # self.calculate_abs_pos()
        #
        # # Color
        # self.color = InputField.COLOR_INACTIVE
        # self.text_color = pygame.color.Color(text_color)
        #
        # # Text
        # self.txt_surface = InputField.my_font.render(text, True, self.text_color)
        # self.txt_rect = self.txt_surface.get_rect(center=self.rect.center)

        # var
        self.active = active
        self.disabled = disabled
        self.click = False

    def handle_event(self, eventloop_event):
        if self.disabled:
            return None
        self.active = False
        if eventloop_event.type == pygame.MOUSEBUTTONDOWN:
            if self.abs_rect.collidepoint(eventloop_event.pos):
                self.click = True
            else:
                self.click = False
        if eventloop_event.type == pygame.MOUSEBUTTONUP:
            if self.abs_rect.collidepoint(eventloop_event.pos) and self.click is True:
                self.active = True
                # print("click")
                # Trigger
            self.click = False
        return self.active

    def draw(self, surface_screen):
        self.color = self.COLOR_INACTIVE if not self.click else self.COLOR_ACTIVE
        self.color = self.COLOR_DISABLED if self.disabled else self.color
        bg_color = ButtonBox.COLOR_BACKGROUND if not self.disabled else self.COLOR_DISABLED
        pygame.draw.rect(surface_screen,bg_color, self.rect, border_radius=4)
        pygame.draw.rect(surface_screen, self.color, self.rect, 5, 5)
        surface_screen.blit(self.txt_surface, self.txt_rect)


class ToggleButton(Button):
    def handle_event(self, eventloop_event):
        if eventloop_event.type == pygame.MOUSEBUTTONDOWN:
            if self.abs_rect.collidepoint(eventloop_event.pos):
                self.click = True
            else:
                self.click = False
        if eventloop_event.type == pygame.MOUSEBUTTONUP:
            if self.abs_rect.collidepoint(eventloop_event.pos) and self.click is True:
                self.active = not self.active
            self.click = False
        return self.active

    def draw(self, surface_screen):
        self.color = pygame.Color('green') if self.active else pygame.Color('red')
        pygame.draw.rect(surface_screen, ButtonBox.COLOR_BACKGROUND, self.rect, border_radius=4)
        pygame.draw.rect(surface_screen, self.color, self.rect, 5, 5)
        surface_screen.blit(self.txt_surface, self.txt_rect)


class InputField(Element):
    def __init__(self, x, y, w=340, h=32, text="", text_color="black", disabled=False, top_left_corner_surface=(0, 0)):
        super(InputField, self).__init__(x, y, w, h, text,
                                         text_color=text_color, top_left_corner_surface=top_left_corner_surface)

        # relative pos
        self.size = (w, h)
        self.pos = (x, y)
        self.surface = pygame.Surface((w, h))
        self.rect = self.surface.get_rect(topleft=(x, y))
        # self.calculate_abs_pos()
        # abs pos
        # self.support_point = top_left_corner_surface
        # self.abs_rect = None
        # self.calculate_abs_pos()

        # color
        self.color = InputField.COLOR_INACTIVE
        self.text_color = pygame.color.Color(text_color)

        # text
        self.text = text
        self.txt_surface = InputField.my_font.render(text, True, self.text_color)
        self.txt_rect = self.txt_surface.get_rect()

        # var
        self.active = False
        self.disabled = disabled

    def handle_event(self, eventloop_event):
        if self.disabled:
            return ""
        old_active = self.active
        if eventloop_event.type == pygame.MOUSEBUTTONDOWN:
            # print(eventloop_event.pos, self.abs_rect, self.abs_rect.collidepoint(eventloop_event.pos))
            if self.abs_rect.collidepoint(eventloop_event.pos):
                self.active = not self.active   # Toggle value
            else:
                self.active = False

        if type(self.text) != str:
            try:
                self.text = str(self.text)
            except TypeError:
                self.text = ""

        if self.active and eventloop_event.type == pygame.KEYDOWN:
            if eventloop_event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif eventloop_event.key == pygame.K_RETURN:
                self.active = False
                return self.text
            else:
                self.text += eventloop_event.unicode
        self.txt_surface = self.my_font.render(self.text, True, self.text_color)

        if old_active and not self.active:
            return self.text
        return ""

    def set_text(self, text):
        self.text = str(text)

    def _update_self_box(self):
        if self.disabled:
            self.color = InputField.COLOR_DISABLED
        else:
            if self.active:
                self.color = InputField.COLOR_ACTIVE
            else:
                self.color = InputField.COLOR_INACTIVE
        self.surface.fill(self.color)
        pygame.draw.rect(self.surface, ButtonBox.COLOR_BORDER, self.surface.get_rect(), 3)
        w, h = self.size
        x = self.my_font.get_height()
        self.txt_rect = self.txt_surface.get_rect(topleft=(5, h//2 - x//2))
        self.surface.blit(self.txt_surface, self.txt_rect)


class TextField(Element):
    def __init__(self, x, y, w=340, h=32, text="", text_color="black", color=None, top_left_corner_surface=(0, 0),
                 font=None, font_size=25):
        super(TextField, self).__init__(x, y, w, h, text, text_color, top_left_corner_surface)

        # relative pos
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(x, y))
        # # abs pos
        # self.support_point = top_left_corner_surface
        # # self.abs_rect = None
        # # self.calculate_abs_pos()

        # color
        self.color = pygame.Color(color) if color is not None else pygame.Color(0, 0, 0, 0)
        self.text_color = pygame.color.Color(text_color)

        # Font
        self.font = font if font is not None else pygame.font.SysFont("futura", font_size)

        # text
        self.text = text
        self.txt_surface = self.font.render(text, True, self.text_color)
        self.txt_rect = self.txt_surface.get_rect()

    def handle_event(self, eventloop_event: pygame.event) -> bool:
        pass

    def _update_self_box(self):
        self.surface.fill(self.color)
        self.surface.blit(self.txt_surface, self.txt_rect)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 640))
    clock = pygame.time.Clock()
    screen_height, screen_width = screen.get_size()

    abs_center_x, abs_center_y = screen_height // 2, screen_width // 2

    text_box = ButtonBox(abs_center_x, abs_center_y, 620, 200, {
                         "text": TextField(30, 60, text="Schönen guten Tag"),
                         "field": InputField(30, 90, 560, 32, "Hi"),
                         "button": Button(abs_center_y, 150, text="Ok")},
                         text="Please enter sth.")

    # text_box = ButtonBox(abs_center_x, abs_center_y, 420, 150, {
    #     "cancel": Button(int(abs_center_y*1/3), 100, 150, 34, text="cancel"),
    #     "exit": Button(int(abs_center_y*3/3), 100, 150, 34, text="exit")},
    #                      text="really exit?")

    while True:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            (text_box.handle_box_events(event))
        text_box.draw(screen)
        # pygame.draw.rect(surface_screen, "green", text_box.elements["field"].abs_rect)

        pygame.display.update()
        clock.tick(60)
