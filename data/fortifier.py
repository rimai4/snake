import os
import random

import pygame

from data.base_modifier import BaseModifier
from data.colors import Colors


class Fortifier(BaseModifier):
    def __init__(self, game):
        self.name = "fortifier"
        self.game = game
        self.size = 20
        self.block_positions = self.get_block_positions()
        fortifier_image = pygame.image.load(os.path.join("resources", "fortifier.png"))
        self.image = pygame.transform.scale(fortifier_image, (20, 20)).convert()

    def set_icon_location(self):
        possible_locations = list(
            set(self.game.board_coordinates)
            - set(self.game.snake.body)
            - set(self.block_positions)
        )
        self.position = random.choice(possible_locations)
        x, y = self.position
        self.coordinates = (x * self.size, y * self.size)

    def get_block_positions(self):
        top_positions = [(i, 0) for i in range(20)]
        right_positions = [(19, i) for i in range(20)]
        bottom_positions = [(i, 19) for i in range(20)]
        left_positions = [(0, i) for i in range(20)]
        return [*top_positions, *right_positions, *bottom_positions, *left_positions]

    def check_block_hit(self):
        for block in self.block_positions:
            if self.game.snake.overlaps(block, head_only=True):
                self.game.end()

    def hide(self):
        self.position = []
        self.coordinates = []

    def draw(self):
        if self.coordinates:
            self.game.game_surface.blit(self.image, self.coordinates)

    def draw_blocks(self):
        for x, y in self.block_positions:
            rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
            pygame.draw.rect(self.game.game_surface, Colors.BLUE, rect, 0)
