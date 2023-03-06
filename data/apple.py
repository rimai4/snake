import os
import random

import pygame


class Apple:
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load(os.path.join("resources", "apple.png"))
        self.size = 20
        self.update_coordinates()

    def update_coordinates(self):
        possible_locations = list(
            set(self.game.board_coordinates) - set(self.game.snake.body)
        )
        self.position = random.choice(possible_locations)
        x, y = self.position
        self.coordinates = (x * self.size, y * self.size)

    def draw(self):
        self.game.game_surface.blit(self.image, self.coordinates)
