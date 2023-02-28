import pygame

from data.colors import Colors
from data.states.base_state import BaseState
from db import add_high_score, should_delete_last_score


class NameEntry(BaseState):
    def __init__(self, game):
        BaseState.__init__(self)
        self.next = "game_over"
        self.game = game
        self.text = ""

    def setup(self):
        self.text = ""

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                delete_last_score = should_delete_last_score()
                add_high_score(
                    self.text,
                    self.game.score,
                    remove_last=delete_last_score,
                )
                self.switch_state()
            elif event.key == pygame.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]
            elif len(self.text) < 10:
                self.text += event.unicode

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        size = self.game.game_screen_size
        screen.fill(Colors.BLACK)
        self.render_text(screen, "High score!", Colors.WHITE, size / 2, size * 0.25)
        self.render_text(
            screen,
            "Enter name and press enter to submit",
            Colors.WHITE,
            size / 2,
            size * 0.5,
        )
        self.render_text(
            screen, "Max 10 characters", Colors.WHITE, size / 2, size * 0.6
        )
        self.render_text(screen, self.text, Colors.WHITE, size / 2, size * 0.75)
