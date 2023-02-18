import pygame

from apple import Apple
from base_state import BaseState
from colors import Colors
from snake import Snake

SCREEN_SIZE = 400
SCORE_SIZE = 50


class Game(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.next = "game_over"
        self.snake = Snake(self)
        self.game_screen_size = 400
        self.score_height = 50
        self.game_over = False
        self.board_coordinates = self.get_all_coordinates()
        self.apple = Apple(self)
        self.score_surface = pygame.Surface((SCREEN_SIZE, SCORE_SIZE))
        self.game_surface = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
        self.score = 0

    def update(self, screen, dt):
        self.snake.change_direction()
        self.snake.move()
        if self.snake.collides_with_self():
            self.switch_state()

        if self.snake.overlaps(self.apple.position, head_only=True):
            self.on_apple_hit()
        self.draw(screen)

    def reset(self):
        self.snake.initialize_body()
        self.score = 0

    def draw(self, screen):
        self.score_surface.fill(Colors.WHITE)
        self.game_surface.fill(Colors.BLACK)
        self.apple.draw()
        self.snake.draw(self.game_surface)
        self.draw_score()
        screen.blit(self.score_surface, (0, 0))
        screen.blit(self.game_surface, (0, self.score_height))

    def start(self):
        self.score = 0
        self.snake.initialize_body()

    def get_all_coordinates(self):
        block_count = self.game_screen_size // self.snake.body_part_size
        coordinates = []
        for i in range(block_count):
            for j in range(block_count):
                coordinates.append((i, j))
        return coordinates

    def on_apple_hit(self):
        self.score += 1
        self.apple.update_coordinates()
        self.snake.extend()

    def draw_score(self):
        self.render_text(
            self.score_surface,
            str(self.score),
            Colors.BLACK,
            self.game_screen_size / 2,
            self.score_height / 2,
        )

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.snake.is_moving_vertically:
                self.snake.add_direction_change("right")
            if event.key == pygame.K_LEFT and self.snake.is_moving_vertically:
                self.snake.add_direction_change("left")
            if event.key == pygame.K_UP and self.snake.is_moving_horizontally:
                self.snake.add_direction_change("up")
            if event.key == pygame.K_DOWN and self.snake.is_moving_horizontally:
                self.snake.add_direction_change("down")
