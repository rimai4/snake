import os
import random

import pygame


class Thunder:
    def __init__(self, game):
        self.game = game
        thunder_image = pygame.image.load(os.path.join("resources", "thunder.png"))
        self.image = pygame.transform.scale(thunder_image, (20, 20)).convert()
        self.size = 20
        self.position = []
        self.coordinates = []

    def update_location(self):
        possible_locations = list(
            set(self.game.board_coordinates)
            - set(self.game.snake.body + [self.game.apple.position])
        )
        self.position = random.choice(possible_locations)
        self.coordinates = [coord * self.size for coord in self.position]

    def hide(self):
        self.position = []
        self.coordinates = []

    def draw(self):
        if self.coordinates:
            self.game.game_surface.blit(self.image, self.coordinates)
