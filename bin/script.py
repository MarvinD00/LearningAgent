import pygame
import random
import src.controllers
from src.controllers import GameController as gc


# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 720))
pygame.display.set_caption("Tetris Learner")

# game loop
GameController = gc.GameController(screen)
pygame.quit()