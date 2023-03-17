import os
import random

import pygame

from data.apple import Apple
from data.colors import Colors
from data.events import COUNT, MOVE_SNAKE, START_EVENT_COUNTDOWN
from data.forest import Forest
from data.fortifier import Fortifier
from data.snake import Snake
from data.states.base_state import BaseState
from data.thunder import Thunder
from db import is_high_score


class Game(BaseState):
    def __init__(self, block_count, block_size, score_height):
        BaseState.__init__(self)
        self.block_count = block_count
        self.block_size = block_size
        self.game_screen_size = block_count * block_size
        self.score_height = score_height
        self.modes = ["forest"]
        self.board_coordinates = self.get_all_coordinates()
        self.score_surface = pygame.Surface((self.game_screen_size, self.score_height))
        self.game_surface = pygame.Surface(
            (self.game_screen_size, self.game_screen_size)
        )
        self.apple_sound = pygame.mixer.Sound(
            os.path.join("resources", "apple_sound.wav")
        )
        self.forest = Forest(self)

    @property
    def in_pre_event_countdown(self):
        return self.mode == "normal" and self.counter > 0

    def check_collision(self):
        if self.snake.collides_with_self():
            self.end()
        if self.snake.overlaps(self.apple.position, head_only=True):
            self.on_apple_hit()
        if self.mode == "forest":
            self.forest.check_collision()

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        self.score_surface.fill(
            Colors.YELLOW if self.mode == "thunder" else Colors.WHITE
        )
        self.game_surface.fill(Colors.BLACK)

        self.apple.draw()
        self.snake.draw()
        self.draw_score()
        if self.counter > 0:
            self.draw_counter()
        if self.in_pre_event_countdown:
            self.draw_next_event()

        if self.mode == "forest":
            self.forest.draw_trees()

        screen.blit(self.score_surface, (0, 0))
        screen.blit(self.game_surface, (0, self.score_height))

    def draw_counter(self):
        self.render_text(
            self.score_surface,
            str(self.counter),
            Colors.BLACK,
            self.game_screen_size * 0.5,
            self.score_height / 2,
        )

    def draw_next_event(self):
        self.render_text(
            self.score_surface,
            f"next mode: {self.next_mode}".upper(),
            Colors.BLACK,
            self.game_screen_size * 0.25,
            self.score_height / 2,
        )

    def setup(self):
        self.counter = 0
        self.mode = "normal"
        self.next_mode = random.choice(self.modes)
        self.score = 0
        self.snake = Snake(self, size=self.block_size)
        self.apple = Apple(self)
        self.thunder = Thunder(self)
        self.fortifier = Fortifier(self)
        pygame.time.set_timer(MOVE_SNAKE, 90)
        pygame.time.set_timer(START_EVENT_COUNTDOWN, 3000, loops=1)

    def cleanup(self):
        pygame.time.set_timer(MOVE_SNAKE, 0)
        pygame.time.set_timer(START_EVENT_COUNTDOWN, 0)
        pygame.time.set_timer(COUNT, 0)

    def get_all_coordinates(self):
        block_count = self.game_screen_size // self.block_size
        coordinates = []
        for i in range(block_count):
            for j in range(block_count):
                coordinates.append(pygame.Vector2(i, j))
        return coordinates

    def end(self):
        if is_high_score(self.score):
            self.next = "name_entry"
        else:
            self.next = "game_over"
        self.switch_state()

    def on_apple_hit(self):
        self.apple_sound.play()
        self.score += 1
        self.apple.update_coordinates()
        self.snake.extend()

    def draw_trees(self):
        pass

    def draw_score(self):
        self.render_text(
            self.score_surface,
            str(self.score),
            Colors.BLACK,
            self.game_screen_size * 0.9,
            self.score_height / 2,
        )

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.snake.add_direction_change(pygame.Vector2(1, 0))
            elif event.key == pygame.K_LEFT:
                self.snake.add_direction_change(pygame.Vector2(-1, 0))
            elif event.key == pygame.K_UP:
                self.snake.add_direction_change(pygame.Vector2(0, -1))
            elif event.key == pygame.K_DOWN:
                self.snake.add_direction_change(pygame.Vector2(0, 1))

        elif event.type == MOVE_SNAKE:
            self.snake.move()
            self.check_collision()
        elif event.type == START_EVENT_COUNTDOWN:
            self.counter = 5
            pygame.time.set_timer(COUNT, 1000, loops=5)
        elif event.type == COUNT:
            self.counter -= 1
            if self.counter == 0:
                if self.mode == "normal":
                    self.mode = self.next_mode
                    if self.mode == "thunder":
                        pygame.time.set_timer(MOVE_SNAKE, 50)
                    elif self.mode == "forest":
                        self.forest.update_tree_locations()
                    self.counter = 3
                    pygame.time.set_timer(COUNT, 1000, loops=10)
                else:
                    if self.mode == "thunder":
                        pygame.time.set_timer(MOVE_SNAKE, 90)
                    self.mode = "normal"
                    pygame.time.set_timer(START_EVENT_COUNTDOWN, 5000, loops=1)
