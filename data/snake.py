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

    def draw(self):
        for x, y in self.body:
            rect = pygame.Rect(
                x * self.body_part_size,
                y * self.body_part_size,
                self.body_part_size,
                self.body_part_size,
            )
            pygame.draw.rect(self.game.game_surface, Colors.GREEN, rect, 0)
