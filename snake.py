import pygame

from colors import *


class Snake:
    TIMEOUTS = {"normal": 100, "fast": 50, "blazing": 25}

    def __init__(self, game, size):
        self.game = game
        self.body_part_size = size
        self.initialize_body()
        self.last_move = None
        self.last_tail = self.body[-1]
        self.direction_changes = []
        self.has_changed_direction = False
        self.timeout = Snake.TIMEOUTS["normal"]
        self.max_length = self.game.game_screen_size / self.body_part_size

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

    def set_speed(self, speed):
        self.timeout = Snake.TIMEOUTS[speed]

    def overlaps(self, coords, head_only=False):
        if head_only:
            return self.head == coords
        return coords in self.body

    def add_direction_change(self, direction):
        self.direction_changes.append(direction)

    def change_direction(self):
        if self.direction_changes and not self.has_changed_direction:
            self.direction = self.direction_changes.pop(0)
            self.has_changed_direction = True

    def move(self):
        now = pygame.time.get_ticks()
        if self.last_move and now - self.last_move < self.timeout:
            return

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
        self.last_move = now
        self.has_changed_direction = False

    def extend(self):
        self.body.insert(0, self.last_tail)

    def collides_with_self(self):
        """
        Check if head collides with body, including the last tail position.
        """
        targets = [self.last_tail] + self.body[:-1]
        return self.head in targets

    def draw(self, surface):
        for x, y in self.body:
            rect = pygame.Rect(
                x * self.body_part_size,
                y * self.body_part_size,
                self.body_part_size,
                self.body_part_size,
            )
            pygame.draw.rect(surface, Colors.GREEN, rect, 0)
