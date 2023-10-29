# Example file showing a circle moving on screen
import pygame
import random
import src.Objects
import src.controllers
from src.Objects import Tetrimino as Tetrimino
from src.controllers import TetriminoController as TetriminoController
from src.controllers import GameController as gc
from src.controllers import AgentController as ac

# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 720))
pygame.display.set_caption("Tetris Learner")

# game loop
GameController = gc.GameController(screen)
pygame.quit()