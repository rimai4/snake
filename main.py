import sys

import pygame

from data.control import Control
from data.states.game import Game
from data.states.game_over import GameOverScreen
from data.states.name_entry import NameEntry
from data.states.start_menu import StartMenu

pygame.init()
pygame.display.set_caption("Snake")

settings = {"size": (400, 450), "fps": 60}
app = Control(**settings)
game = Game()
state_dict = {
    "start": StartMenu(settings),
    "game": game,
    "name_entry": NameEntry(game),
    "game_over": GameOverScreen(game),
}
app.setup_states(state_dict, "start")
app.game_loop()
pygame.quit()
sys.exit()
