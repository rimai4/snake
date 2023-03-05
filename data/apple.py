import os
import random

import pygame


class Apple:
    def __init__(self, game):
        self.game = game
        apple_image = pygame.image.load(os.path.join("resources", "apple.png"))
        self.image = pygame.transform.scale(apple_image, (20, 20)).convert()
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
