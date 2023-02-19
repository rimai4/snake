import pygame

from base_state import BaseState
from colors import Colors


class GameOverScreen(BaseState):
    def __init__(self, game):
        BaseState.__init__(self)
        self.next = "game"
        self.game = game

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_state()

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        width = self.game.game_screen_size
        screen.fill(Colors.BLACK)
        self.render_text(screen, "Game over", Colors.WHITE, width / 2, width / 2)
