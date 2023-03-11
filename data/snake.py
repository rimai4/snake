import os

import pygame

from data.colors import Colors


class Snake:
    def __init__(self, game, size):
        self.game = game
        self.body_part_size = size
        self.initialize_body()
        self.last_tail = self.body[-1]
        self.direction_changes = []
        self.max_length = self.game.game_screen_size / self.body_part_size
        self.head_down = pygame.image.load(
            os.path.join("resources", "snake_head_down.png")
        )
        self.head_right = pygame.image.load(
            os.path.join("resources", "snake_head_right.png")
        )
        self.head_up = pygame.image.load(os.path.join("resources", "snake_head_up.png"))
        self.head_left = pygame.image.load(
            os.path.join("resources", "snake_head_left.png")
        )

    @property
    def tail(self):
        return self.body[0]

    @property
    def head(self):
        return self.body[-1]

    @property
    def is_moving_horizontally(self):
        return self.direction in ["left", "right"]

    @property
    def is_moving_vertically(self):
        return self.direction in ["down", "up"]

    def initialize_body(self):
        self.body = [(1, 5), (2, 5), (3, 5), (4, 5)]
        self.direction = "right"

    def overlaps(self, coords, head_only=False):
        if head_only:
            return self.head == coords
        return coords in self.body

    def add_direction_change(self, direction):
        self.direction_changes.append(direction)

    def change_direction(self):
        if self.direction_changes:
            direction = self.direction_changes.pop(0)
            if (direction in ["up", "down"] and self.is_moving_horizontally) or (
                direction in ["right", "left"] and self.is_moving_vertically
            ):
                self.direction = direction

    def move(self):
        self.change_direction()

        self.last_tail = self.tail
        self.body.pop(0)

        head = self.body[-1]
        head_x, head_y = head
        new_head = None
        if self.direction == "left":
            new_head = ((head_x - 1) % self.max_length, head[1])
        if self.direction == "right":
            new_head = ((head_x + 1) % self.max_length, head[1])
        if self.direction == "down":
            new_head = (head[0], (head_y + 1) % self.max_length)
        if self.direction == "up":
            new_head = (head[0], (head_y - 1) % self.max_length)

        self.body.append(new_head)

    def extend(self):
        self.body.insert(0, self.last_tail)

    def collides_with_self(self):
        """
        Check if head collides with body, including the last tail position.
        """
        targets = [self.last_tail] + self.body[:-1]
        return self.head in targets

    def get_coordinates(self, position):
        x, y = position
        return (x * self.body_part_size, y * self.body_part_size)

    def draw_head(self):
        head_coordinates = self.get_coordinates(self.head)

        if self.direction == "left":
            self.game.game_surface.blit(self.head_left, head_coordinates)
        if self.direction == "right":
            self.game.game_surface.blit(self.head_right, head_coordinates)
        if self.direction == "down":
            self.game.game_surface.blit(self.head_down, head_coordinates)
        if self.direction == "up":
            self.game.game_surface.blit(self.head_up, head_coordinates)

    def draw_tail(self):
        tail_x, tail_y = self.tail
        after_tail_x, after_tail_y = self.body[1]
        if tail_x == after_tail_x:
            rect = pygame.Rect(
                (tail_x * self.body_part_size) + (self.body_part_size / 4),
                tail_y * self.body_part_size,
                self.body_part_size / 2,
                self.body_part_size,
            )
        else:
            rect = pygame.Rect(
                tail_x * self.body_part_size,
                (tail_y * self.body_part_size) + (self.body_part_size / 4),
                self.body_part_size,
                self.body_part_size / 2,
            )

        pygame.draw.rect(self.game.game_surface, Colors.GREEN, rect, 0)

    def draw(self):
        self.draw_tail()

        for x, y in self.body[1:-1]:
            rect = pygame.Rect(
                x * self.body_part_size,
                y * self.body_part_size,
                self.body_part_size,
                self.body_part_size,
            )
            pygame.draw.rect(self.game.game_surface, Colors.GREEN, rect, 0)

        self.draw_head()
