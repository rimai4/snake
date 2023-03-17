import os
import random

import pygame


class Forest:
    def __init__(self, game):
        self.game = game
        self.tree_image = pygame.image.load(os.path.join("resources", "forest.png"))
        self.tree_locations = []

    def update_tree_locations(self):
        head = self.game.snake.head
        used_blocks = self.game.snake.body + [self.game.apple.position]

        possible_locations = [
            item
            for item in self.game.board_coordinates
            if item not in used_blocks
            and (abs(head.x - item.x) > 2 and abs(head.y - item.y) > 2)
        ]
        tree_count = 20
        if len(possible_locations) < 30:
            tree_count = len(possible_locations) // 2
        self.tree_locations = random.sample(possible_locations, tree_count)

    def draw_trees(self):
        for tree in self.tree_locations:
            self.game.game_surface.blit(
                self.tree_image,
                (tree.x * self.game.block_size, tree.y * self.game.block_size),
            )

    def check_collision(self):
        for tree in self.tree_locations:
            if self.game.snake.overlaps(tree):
                self.game.end()
