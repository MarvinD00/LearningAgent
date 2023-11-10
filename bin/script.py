import pygame
from src.Objects import Tetrimino as Tetrimino
from src.controllers import TetriminoController as TetriminoController
from src.controllers import GameController as GameController

# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 720))
pygame.display.set_caption("Tetris Learner")

# game loop
GameController = GameController.GameController(screen)

pygame.quit()