import os
import random

import pygame

from data.base_modifier import BaseModifier


class Thunder(BaseModifier):
    def __init__(self, game):
        self.game = game
        self.name = "thunder"
        thunder_image = pygame.image.load(os.path.join("resources", "thunder.png"))
        self.image = pygame.transform.scale(thunder_image, (20, 20)).convert()
        self.size = 20

    def set_icon_location(self):
        possible_locations = list(
            set(self.game.board_coordinates)
            - set(self.game.snake.body + [self.game.apple.position])
        )
        self.position = random.choice(possible_locations)
        x, y = self.position
        self.coordinates = (x * self.size, y * self.size)

    def hide(self):
        self.position = []
        self.coordinates = []

    def draw(self):
        if self.coordinates:
            self.game.game_surface.blit(self.image, self.coordinates)

    def modify(self):
        self.game.snake.set_speed("fast")

    def reset(self):
        self.game.snake.set_speed("normal")
