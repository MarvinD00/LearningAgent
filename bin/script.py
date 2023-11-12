import pygame
from src.Objects import Tetrimino as Tetrimino
from src.controllers import TetriminoController as TetriminoController
from src.controllers import GameController as GameController
from src import TetrisAgent as Agent

agent = Agent.TetrisAgent()

agent.train()

pygame.quit()