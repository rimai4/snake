import os
import random

import pygame

from data.base_modifier import BaseModifier
from data.events import MOVE_SNAKE


class Thunder(BaseModifier):
    def __init__(self, game):
        self.game = game
        self.name = "thunder"
        self.image = pygame.image.load(os.path.join("resources", "thunder.png"))

    def set_icon_location(self):
        possible_locations = list(
            set(self.game.board_coordinates)
            - set(self.game.snake.body + [self.game.apple.position])
        )
        self.position = random.choice(possible_locations)
        x, y = self.position
        self.coordinates = (x * self.game.block_size, y * self.game.block_size)

    def hide(self):
        self.position = []
        self.coordinates = []

    def draw(self):
        if self.coordinates:
            self.game.game_surface.blit(self.image, self.coordinates)

    def modify(self):
        pygame.time.set_timer(MOVE_SNAKE, 60)

    def reset(self):
        pygame.time.set_timer(MOVE_SNAKE, 100)
