import os

import pygame

from data.colors import Colors
from data.states.base_state import BaseState


class StartMenu(BaseState):
    def __init__(self, size):
        BaseState.__init__(self)
        self.next = "game"
        self.screen_width, self.screen_height = size
        self.background_sound = pygame.mixer.Sound(
            os.path.join("resources", "background_music.wav")
        )

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_state()

    def setup(self):
        self.background_sound.play(-1, 0)

    def cleanup(self):
        self.background_sound.stop()

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
            title=True,
        )
        self.render_text(
            screen,
            "Press space to start",
            Colors.WHITE,
            self.screen_width / 2,
            self.screen_height * 0.5,
        )
