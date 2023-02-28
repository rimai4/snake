import pygame

from data.colors import Colors
from data.states.base_state import BaseState
from db import select_high_scores


class GameOverScreen(BaseState):
    def __init__(self, game):
        BaseState.__init__(self)
        self.next = "game"
        self.game = game
        self.high_scores = []

    def setup(self):
        self.high_scores = select_high_scores()

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_state()

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        size = self.game.game_screen_size
        screen.fill(Colors.BLACK)
        self.render_text(
            screen, "Game over", Colors.WHITE, size / 2, size * 0.15, title=True
        )
        self.render_text(screen, "High scores", Colors.WHITE, size / 2, size * 0.3)

        for i, score in enumerate(self.high_scores):
            self.render_text(
                screen,
                f"{score[0]} - {score[1]}",
                Colors.WHITE,
                size / 2,
                size * (0.4 + (0.1 * i)),
            )

        self.render_text(
            screen, "Press space to start new game", Colors.WHITE, size / 2, size * 0.95
        )
