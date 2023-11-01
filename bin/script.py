import pygame
import random
import src.controllers
from src.controllers import GameController as gc
from src.controllers import AgentController as ac
from src.controllers import TetrisEnvironment as te

pygame.init()
screen = pygame.display.set_mode((400, 720))
pygame.display.set_caption("Tetris Learner")

gc = gc.GameController(screen)
env = te.TetrisEnvironment(gc)
agent = ac.Agent(env)
agent.run()
pygame.quit()

