import pygame

from data.apple import Apple
from data.colors import Colors
from data.events import (DISABLE_THUNDER_MODE, HIDE_THUNDER_EVENT,
                         SPAWN_THUNDER_EVENT)
from data.snake import Snake
from data.states.base_state import BaseState
from data.thunder import Thunder
from db import is_high_score


class Game(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.thunder_mode = False
        self.game_screen_size = 400
        self.score_height = 50
        self.snake_size = 20
        self.board_coordinates = self.get_all_coordinates()
        self.score_surface = pygame.Surface((self.game_screen_size, self.score_height))
        self.game_surface = pygame.Surface(
            (self.game_screen_size, self.game_screen_size)
        )

    def update(self, screen, dt):
        self.snake.change_direction()
        self.snake.move()

        if self.snake.collides_with_self():
            self.on_self_hit()
        if self.snake.overlaps(self.apple.position, head_only=True):
            self.on_apple_hit()
        if self.snake.overlaps(self.thunder.position, head_only=True):
            self.on_thunder_hit()

        self.draw(screen)

    def setup(self):
        self.score = 0
        self.snake = Snake(self, size=self.snake_size)
        self.apple = Apple(self)
        self.thunder = Thunder(self)
        pygame.time.set_timer(SPAWN_THUNDER_EVENT, 10000, loops=1)

    def cleanup(self):
        pygame.time.set_timer(SPAWN_THUNDER_EVENT, 0)
        pygame.time.set_timer(HIDE_THUNDER_EVENT, 0)
        pygame.time.set_timer(DISABLE_THUNDER_MODE, 0)

    def start(self):
        self.score = 0
        self.snake.initialize_body()

    def get_all_coordinates(self):
        block_count = self.game_screen_size // self.snake_size
        coordinates = []
        for i in range(block_count):
            for j in range(block_count):
                coordinates.append((i, j))
        return coordinates

    def on_self_hit(self):
        if is_high_score(self.score):
            self.next = "name_entry"
        else:
            self.next = "game_over"
        self.switch_state()

    def on_apple_hit(self):
        self.score += 2 if self.thunder_mode else 1
        self.apple.update_coordinates()
        self.snake.extend()

    def on_thunder_hit(self):
        self.thunder_mode = True
        self.thunder.hide()
        self.snake.set_speed("fast")
        pygame.time.set_timer(DISABLE_THUNDER_MODE, 8000, loops=1)
        pygame.time.set_timer(HIDE_THUNDER_EVENT, 0)

    def draw(self, screen):
        self.score_surface.fill(Colors.YELLOW if self.thunder_mode else Colors.WHITE)
        self.game_surface.fill(Colors.BLACK)
        self.apple.draw()
        self.snake.draw()
        self.thunder.draw()
        self.draw_score()
        screen.blit(self.score_surface, (0, 0))
        screen.blit(self.game_surface, (0, self.score_height))

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
            elif event.key == pygame.K_LEFT and self.snake.is_moving_vertically:
                self.snake.add_direction_change("left")
            elif event.key == pygame.K_UP and self.snake.is_moving_horizontally:
                self.snake.add_direction_change("up")
            elif event.key == pygame.K_DOWN and self.snake.is_moving_horizontally:
                self.snake.add_direction_change("down")

        elif event.type == SPAWN_THUNDER_EVENT:
            self.thunder.update_location()
            pygame.time.set_timer(HIDE_THUNDER_EVENT, 6000, loops=1)
        elif event.type == HIDE_THUNDER_EVENT:
            self.thunder.hide()
            pygame.time.set_timer(SPAWN_THUNDER_EVENT, 10000, loops=1)
        elif event.type == DISABLE_THUNDER_MODE:
            self.thunder_mode = False
            self.snake.set_speed("normal")
            pygame.time.set_timer(SPAWN_THUNDER_EVENT, 10000, loops=1)
