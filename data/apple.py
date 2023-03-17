import os
import random

import pygame


class Apple:
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load(os.path.join("resources", "apple.png"))
        self.update_coordinates()

    def update_coordinates(self):
        used_blocks = self.game.snake.body + self.game.forest.tree_locations
        possible_locations = [
            item for item in self.game.board_coordinates if item not in used_blocks
        ]
        self.position = random.choice(possible_locations)
        self.coordinates = (
            self.position.x * self.game.block_size,
            self.position.y * self.game.block_size,
        )

    def draw(self):
        self.game.game_surface.blit(self.image, self.coordinates)
