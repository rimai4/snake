import pygame
from pygame.locals import *
import sys
import random

pygame.init()

FPS = 60
clock = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_SIZE = 400
SCORE_SIZE = 50
SNAKE_SIZE = 20
assert (
    SCREEN_SIZE / SNAKE_SIZE
) % 1 == 0, "snake size must be divisible by screen size"
MAX_SNAKE_LENGTH = SCREEN_SIZE // SNAKE_SIZE

DISPLAYSURF = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + SCORE_SIZE))
SCORESURF = pygame.Surface((SCREEN_SIZE, SCORE_SIZE))
GAMESURF = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
SCREEN_CENTER = (SCREEN_SIZE / 2, SCREEN_SIZE / 2)
title_font = pygame.font.SysFont("Liga SFMono Nerd Font", 32)
body_font = pygame.font.SysFont("Liga SFMono Nerd Font", 16)
pygame.display.set_caption("Snake")
apple_image = pygame.image.load("apple.png")
scaled_apple = pygame.transform.scale(apple_image, (20, 20)).convert()


class Snake:
    TIMEOUTS = {"normal": 100, "fast": 50, "blazing": 25}

    def __init__(self, speed="normal"):
        self.initialize_body()
        self.surface = GAMESURF
        self.last_move = pygame.time.get_ticks()
        self.last_tail = self.body[-1]
        self.direction_changes = []
        self.has_changed_direction = False
        self.timeout = Snake.TIMEOUTS[speed]

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
        if now - self.last_move < self.timeout:
            return

        self.last_tail = self.tail
        self.body.pop(0)

        head = self.body[-1]
        head_x, head_y = head
        new_head = None
        if self.direction == "left":
            new_head = ((head_x - 1) % MAX_SNAKE_LENGTH, head[1])
        if self.direction == "right":
            new_head = ((head_x + 1) % MAX_SNAKE_LENGTH, head[1])
        if self.direction == "down":
            new_head = (head[0], (head_y + 1) % MAX_SNAKE_LENGTH)
        if self.direction == "up":
            new_head = (head[0], (head_y - 1) % MAX_SNAKE_LENGTH)

        self.body.append(new_head)
        self.last_move = now
        self.has_changed_direction = False

    def extend(self):
        self.body.insert(0, self.last_tail)

    def collides_with_self(self):
        return len(set(self.body)) != len(self.body)

    def draw(self):
        for x, y in self.body:
            rect = pygame.Rect(x * SNAKE_SIZE, y * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE)
            pygame.draw.rect(self.surface, GREEN, rect, 0)


class TextRenderer:
    def __init__(self, surface):
        self.default_surface = surface

    def render(
        self, text, color=WHITE, font=body_font, surface=None, **location_kwargs
    ):
        if surface is None:
            surface = self.default_surface
        text_surface = font.render(text, True, color)
        title_rect = text_surface.get_rect(**location_kwargs)
        surface.blit(text_surface, title_rect)


class Game:
    SPEED_KEYS = {"n": "normal", "f": "fast", "b": "blazing"}

    def __init__(self):
        self.game_over = False
        self.started = False
        self.board_coordinates = self.get_all_coordinates()
        self.snake = Snake()
        self.spawn_apple()
        self.surface = GAMESURF
        self.score_surface = SCORESURF
        self.text_renderer = TextRenderer(self.surface)

    def start(self, speed):
        self.started = True
        self.game_over = False
        self.score = 0
        self.snake.initialize_body()
        self.snake.set_speed(speed)

    def get_all_coordinates(self):
        block_count = SCREEN_SIZE // SNAKE_SIZE
        coordinates = []
        for i in range(block_count):
            for j in range(block_count):
                coordinates.append((i, j))
        return coordinates

    def on_apple_hit(self):
        self.score += 1
        self.spawn_apple()
        self.snake.extend()

    def spawn_apple(self):
        possible_locations = list(set(self.board_coordinates) - set(self.snake.body))
        self.apple = random.choice(possible_locations)

    def draw_apple(self):
        topleft = [(loc * SNAKE_SIZE) for loc in self.apple]
        self.surface.blit(scaled_apple, topleft)

    def draw_start_screen(self):
        self.text_renderer.render(
            "SNAKE", font=title_font, center=(SCREEN_SIZE / 2, 100)
        )
        self.text_renderer.render(
            "Press key to start game", center=(SCREEN_SIZE / 2, 200)
        )
        self.text_renderer.render(
            "n = normal, f = fast, b = very fast",
            center=(SCREEN_SIZE / 2, 300),
        )

    def draw_game_over(self):
        self.text_renderer.render(
            "Game over", font=title_font, center=(SCREEN_SIZE / 2, 100)
        )
        self.text_renderer.render(
            "Press key to start game", center=(SCREEN_SIZE / 2, 200)
        )
        self.text_renderer.render(
            "n = normal, f = fast, b = very fast",
            center=(SCREEN_SIZE / 2, 300),
        )

    def draw_score(self):
        self.text_renderer.render(
            str(self.score),
            surface=self.score_surface,
            color=BLACK,
            font=title_font,
            center=(SCREEN_SIZE / 2, SCORE_SIZE / 2),
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                character = pygame.key.name(event.key)
                if event.key == K_RIGHT and self.snake.is_moving_vertically:
                    self.snake.add_direction_change("right")
                if event.key == K_LEFT and self.snake.is_moving_vertically:
                    self.snake.add_direction_change("left")
                if event.key == K_UP and self.snake.is_moving_horizontally:
                    self.snake.add_direction_change("up")
                if event.key == K_DOWN and self.snake.is_moving_horizontally:
                    self.snake.add_direction_change("down")

                if (not self.started or self.game_over) and character in "nfb":
                    speed = self.SPEED_KEYS[character]
                    self.start(speed)


def start():
    game = Game()
    snake = game.snake

    while True:
        game.handle_events()
        game.score_surface.fill(WHITE)
        GAMESURF.fill(BLACK)
        if not game.started:
            game.draw_start_screen()
        elif game.game_over:
            GAMESURF.fill(BLACK)
            game.draw_game_over()
            game.draw_score()
        else:
            snake.change_direction()
            snake.move()
            if snake.collides_with_self():
                game.game_over = True

            if snake.overlaps(game.apple, head_only=True):
                game.on_apple_hit()

            game.draw_apple()
            snake.draw()
            game.draw_score()

        DISPLAYSURF.blit(game.score_surface, (0, 0))
        DISPLAYSURF.blit(game.surface, (0, SCORE_SIZE))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    start()
