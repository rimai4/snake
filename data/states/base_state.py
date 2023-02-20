import pygame


class BaseState:
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.font = pygame.font.SysFont("Liga SFMono Nerd Font", 16)

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        pass

    def render_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def switch_state(self):
        self.done = True

    def setup(self):
        pass

    def cleanup(self):
        pass
