import sys

import pygame

from control import Control
from game import Game
from game_over import GameOverScreen
from start_menu import StartMenu

pygame.init()
pygame.display.set_caption("Snake")

settings = {"size": (400, 450), "fps": 60}
app = Control(**settings)
game = Game()
state_dict = {
    "start": StartMenu(settings),
    "game": game,
    "game_over": GameOverScreen(game),
}
app.setup_states(state_dict, "start")
app.game_loop()
pygame.quit()
sys.exit()
