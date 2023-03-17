import os

import pygame
from pygame import Vector2


class Snake:
    def __init__(self, game, size):
        self.game = game
        self.body_part_size = size
        self.initialize_body()
        self.last_tail = self.body[-1]
        self.direction_changes = []
        self.max_length = self.game.game_screen_size / self.body_part_size

        self.body_horizontal = pygame.image.load(
            os.path.join("resources", "body_horizontal.png")
        )
        self.body_vertical = pygame.image.load(
            os.path.join("resources", "body_vertical.png")
        )

        self.tail_down = pygame.image.load(os.path.join("resources", "tail_down.png"))
        self.tail_right = pygame.image.load(os.path.join("resources", "tail_right.png"))
        self.tail_up = pygame.image.load(os.path.join("resources", "tail_up.png"))
        self.tail_left = pygame.image.load(os.path.join("resources", "tail_left.png"))

        self.head_down = pygame.image.load(os.path.join("resources", "head_down.png"))
        self.head_right = pygame.image.load(os.path.join("resources", "head_right.png"))
        self.head_up = pygame.image.load(os.path.join("resources", "head_up.png"))
        self.head_left = pygame.image.load(os.path.join("resources", "head_left.png"))

        self.tl = pygame.image.load(os.path.join("resources", "tl.png"))
        self.tr = pygame.image.load(os.path.join("resources", "tr.png"))
        self.br = pygame.image.load(os.path.join("resources", "br.png"))
        self.bl = pygame.image.load(os.path.join("resources", "bl.png"))

    @property
    def tail(self):
        return self.body[0]

    @property
    def head(self):
        return self.body[-1]

    @property
    def is_moving_horizontally(self):
        return self.direction in [Vector2(1, 0), Vector2(-1, 0)]

    @property
    def is_moving_vertically(self):
        return self.direction in [Vector2(0, 1), Vector2(0, -1)]

    def initialize_body(self):
        self.body = [
            Vector2(1, 5),
            Vector2(2, 5),
            Vector2(3, 5),
            Vector2(4, 5),
        ]
        self.direction = Vector2(1, 0)

    def overlaps(self, coords, head_only=False):
        if head_only:
            return self.head == coords
        return coords in self.body

    def add_direction_change(self, direction):
        self.direction_changes.append(direction)

    def change_direction(self):
        if self.direction_changes:
            direction = self.direction_changes.pop(0)
            if (
                direction in [Vector2(0, 1), Vector2(0, -1)]
                and self.is_moving_horizontally
            ) or (
                direction in [Vector2(1, 0), Vector2(-1, 0)]
                and self.is_moving_vertically
            ):
                self.direction = direction

    def move(self):
        self.change_direction()

        self.last_tail = self.tail
        self.body.pop(0)

        new_head = self.head + self.direction
        new_head.x = new_head.x % self.max_length
        new_head.y = new_head.y % self.max_length
        self.body.append(new_head)  # type: ignore

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

        if self.direction == Vector2(-1, 0):
            self.game.game_surface.blit(self.head_left, head_coordinates)
        if self.direction == Vector2(1, 0):
            self.game.game_surface.blit(self.head_right, head_coordinates)
        if self.direction == Vector2(0, 1):
            self.game.game_surface.blit(self.head_down, head_coordinates)
        if self.direction == Vector2(0, -1):
            self.game.game_surface.blit(self.head_up, head_coordinates)

    def draw_tail(self):
        tail_coordinates = self.get_coordinates(self.tail)
        tail_x, tail_y = self.tail
        after_tail_x, after_tail_y = self.body[1]

        if tail_x == after_tail_x:
            if after_tail_y > tail_y:
                self.game.game_surface.blit(self.tail_down, tail_coordinates)
            else:
                self.game.game_surface.blit(self.tail_up, tail_coordinates)

        else:
            if after_tail_x > tail_x:
                self.game.game_surface.blit(self.tail_right, tail_coordinates)
            else:
                self.game.game_surface.blit(self.tail_left, tail_coordinates)

    def draw(self):
        self.draw_tail()

        for i, part in enumerate(self.body):
            if i == 0 or i == len(self.body) - 1:
                continue
            coordinates = self.get_coordinates(part)
            x, y = part
            previous = self.body[i - 1]
            next = self.body[i + 1]
            if (next - previous == Vector2(-1, 1) and y == previous.y) or (
                next - previous == Vector2(1, -1) and x == previous.x
            ):
                self.game.game_surface.blit(self.tl, coordinates)
            elif (next - previous == Vector2(1, 1) and x == previous.x) or (
                next - previous == Vector2(-1, -1) and y == previous.y
            ):
                self.game.game_surface.blit(self.bl, coordinates)
            elif (next - previous == Vector2(1, -1) and y == previous.y) or (
                next - previous == Vector2(-1, 1) and x == previous.x
            ):
                self.game.game_surface.blit(self.br, coordinates)
            elif (next - previous == Vector2(-1, -1) and x == previous.x) or (
                next - previous == Vector2(1, 1) and y == previous.y
            ):
                self.game.game_surface.blit(self.tr, coordinates)
            elif next.y == y:
                self.game.game_surface.blit(self.body_horizontal, coordinates)
            elif next.x == x:
                self.game.game_surface.blit(self.body_vertical, coordinates)

        self.draw_head()
