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
        used_blocks = self.game.snake.body + [self.game.apple.position]
        possible_locations = [
            item for item in self.game.board_coordinates if item not in used_blocks
        ]
        self.position = random.choice(possible_locations)
        self.coordinates = (
            self.position.x * self.game.block_size,
            self.position.y * self.game.block_size,
        )

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
