import random

import pygame

from data.apple import Apple
from data.colors import Colors
from data.events import (DISABLE_MODIFIER, HIDE_MODIFIER, MOVE_SNAKE,
                         SPAWN_MODIFIER)
from data.fortifier import Fortifier
from data.snake import Snake
from data.states.base_state import BaseState
from data.thunder import Thunder
from db import is_high_score

Modifier = Thunder | Fortifier


class Game(BaseState):
    def __init__(self):
        BaseState.__init__(self)
        self.game_screen_size = 400
        self.score_height = 50
        self.snake_size = 20
        self.board_coordinates = self.get_all_coordinates()
        self.score_surface = pygame.Surface((self.game_screen_size, self.score_height))
        self.game_surface = pygame.Surface(
            (self.game_screen_size, self.game_screen_size)
        )

    @property
    def fortified_mode(self):
        return self.mode == "fortifier"

    @property
    def thunder_mode(self):
        return self.mode == "thunder"

    def check_collision(self):
        if self.snake.collides_with_self():
            self.end()
        if self.snake.overlaps(self.apple.position, head_only=True):
            self.on_apple_hit()
        if self.modifier and self.snake.overlaps(
            self.modifier.position, head_only=True
        ):
            self.on_modifier_hit()
        if self.fortified_mode and self.fortifier.check_block_hit():
            self.end()

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        self.score_surface.fill(Colors.YELLOW if self.thunder_mode else Colors.WHITE)
        self.game_surface.fill(Colors.BLACK)

        self.apple.draw()
        self.snake.draw()
        if self.modifier:
            self.modifier.draw()

        if self.fortified_mode:
            self.fortifier.draw_blocks()
        self.draw_score()
        screen.blit(self.score_surface, (0, 0))
        screen.blit(self.game_surface, (0, self.score_height))

    def setup(self):
        self.mode = "normal"
        self.score = 0
        self.snake = Snake(self, size=self.snake_size)
        self.apple = Apple(self)
        self.thunder = Thunder(self)
        self.fortifier = Fortifier(self)
        self.modifier: Modifier = None  # type: ignore
        pygame.time.set_timer(MOVE_SNAKE, 100)
        pygame.time.set_timer(SPAWN_MODIFIER, 3000, loops=1)

    def cleanup(self):
        pygame.time.set_timer(MOVE_SNAKE, 0)
        pygame.time.set_timer(SPAWN_MODIFIER, 0)
        pygame.time.set_timer(HIDE_MODIFIER, 0)
        pygame.time.set_timer(DISABLE_MODIFIER, 0)

    def get_all_coordinates(self):
        block_count = self.game_screen_size // self.snake_size
        coordinates = []
        for i in range(block_count):
            for j in range(block_count):
                coordinates.append((i, j))
        return coordinates

    def end(self):
        if is_high_score(self.score):
            self.next = "name_entry"
        else:
            self.next = "game_over"
        self.switch_state()

    def on_apple_hit(self):
        self.score += 2 if self.thunder_mode else 1
        self.apple.update_coordinates()
        self.snake.extend()

    def on_modifier_hit(self):
        self.mode = self.modifier.name
        self.modifier.hide()
        self.modifier.modify()
        pygame.time.set_timer(DISABLE_MODIFIER, 8000, loops=1)
        pygame.time.set_timer(HIDE_MODIFIER, 0)

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
            if event.key == pygame.K_RIGHT:
                self.snake.add_direction_change("right")
            elif event.key == pygame.K_LEFT:
                self.snake.add_direction_change("left")
            elif event.key == pygame.K_UP:
                self.snake.add_direction_change("up")
            elif event.key == pygame.K_DOWN:
                self.snake.add_direction_change("down")

        elif event.type == MOVE_SNAKE:
            self.snake.move()
            self.check_collision()
        elif event.type == SPAWN_MODIFIER:
            self.modifier = random.choice([self.thunder, self.fortifier])
            self.modifier.set_icon_location()
            pygame.time.set_timer(HIDE_MODIFIER, 10000, loops=1)
        elif event.type == HIDE_MODIFIER:
            self.modifier.hide()
            pygame.time.set_timer(SPAWN_MODIFIER, 10000, loops=1)
        elif event.type == DISABLE_MODIFIER:
            self.mode = "normal"
            self.modifier.reset()
            pygame.time.set_timer(SPAWN_MODIFIER, 10000, loops=1)
