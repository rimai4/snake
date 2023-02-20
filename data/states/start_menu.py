import pygame

from data.colors import Colors
from data.states.base_state import BaseState


class StartMenu(BaseState):
    def __init__(self, settings):
        BaseState.__init__(self)
        self.next = "game"
        self.screen_width, self.screen_height = settings["size"]

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_state()

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.fill(Colors.BLACK)
        self.render_text(
            screen,
            "Snake",
            Colors.WHITE,
            self.screen_width / 2,
            self.screen_height * 0.25,
        )
        self.render_text(
            screen,
            "Press space to start",
            Colors.WHITE,
            self.screen_width / 2,
            self.screen_height * 0.5,
        )
