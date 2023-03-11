import sys

import pygame

from data.control import Control
from data.states.game import Game
from data.states.game_over import GameOverScreen
from data.states.name_entry import NameEntry
from data.states.start_menu import StartMenu

pygame.init()
pygame.display.set_caption("Snake")

block_count = 20
block_size = 30
score_height = 70
size = (block_count * block_size, (block_count * block_size + score_height))
fps = 60
app = Control(size, fps)
game = Game(block_count, block_size, score_height)
state_dict = {
    "start": StartMenu(size),
    "game": game,
    "name_entry": NameEntry(game),
    "game_over": GameOverScreen(game),
}
app.setup_states(state_dict, "start")
app.game_loop()
pygame.quit()
sys.exit()
