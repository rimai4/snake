import pygame

from base_state import BaseState
from colors import Colors


class StartScreen(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.next = "game"

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_state()

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        width = screen.get_width()
        screen.fill(Colors.BLACK)
        self.render_text(screen, "hallo", Colors.WHITE, width / 2, width / 2)
