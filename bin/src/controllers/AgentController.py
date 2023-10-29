import numpy as np
from TetriminoController import TetriminoController
from ..Objects import Tetrimino as Tetrimino
import pygame
from GameController import GameController
from Agent import ObservationSpace

# Basic constructors for the agent to work with
screen = pygame.display.set_mode((400, 720))
t = Tetrimino(0,0)
tc = TetriminoController(screen, t)
gc = GameController(screen)

class Agent:

    def __init__(self):
        self.action_space = np.array(["left", "right", "rotate", "down"]) # 0: move left, 1: move right, 2: rotate
        self.observation_space = ObservationSpace(gc.block_grid, gc.tetrimino_controller.tetrimino)
        self.state = gc.score
        self.ALPHA = 0.5
        self.QVALUE = 0
        self.sequence = []
        self.qvalues = [[0,0,0] for i in range(1000)] # TODO: Might be important later.
        self.curStep = 0

    def step(self, action) -> tuple:
        """
        Proceeds the action chosen by the agent.

        Parameters
        -
        action: int -> random value of self.action_space

        Returns
        -
        step: tuple -> (action, reward, state)
        """
        match action:
            case "left":
                pygame.event.post(pygame.event.Event(pygame.K_a))
                self.sequence.append((gc.dt, 0))
                reward = gc.score
                self.qvalues[self.curStep][0] = reward
            case "right":
                pygame.event.post(pygame.event.Event(pygame.K_d))
                self.sequence.append((gc.dt, 1))
                reward = gc.score
                self.qvalues[self.curStep][1] = reward
            case "rotate":
                pygame.event.post(pygame.event.Event(pygame.K_w))
                reward = gc.score
                self.qvalues[self.curStep][2] = reward
            case "down":
                pygame.event.post(pygame.event.Event(pygame.K_s))
                reward = gc.score
                self.qvalues[self.curStep][3] = reward

        
        return (action, reward, self.state)

    def reset(self) -> None:
        """
        Resets the environment to the default settings.

        Returns
        -
        None
        """
        pass # TODO: Implement the reset of the state and reset the rewards

    def getReward(self, reward):
        self.QVALUE = self.QVALUE + self.ALPHA * (reward + max(self.qvalues) - self.QVALUE)

agent = Agent()