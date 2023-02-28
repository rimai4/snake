import os

import pygame


class BaseState:
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.title_font = pygame.font.Font(
            os.path.join("resources", "retro-gaming.ttf"), 32
        )
        self.font = pygame.font.Font(os.path.join("resources", "retro-gaming.ttf"), 16)

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        pass

    def render_text(self, surface, text, color, x, y, title=False):
        font = self.font
        if title:
            font = self.title_font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def switch_state(self):
        self.done = True

    def setup(self):
        pass

    def cleanup(self):
        pass
