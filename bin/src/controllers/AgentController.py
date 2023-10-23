import numpy as np
from TetriminoController import TetriminoController
from ..Objects import Tetrimino as Tetrimino
import pygame
from GameController import GameController

# Basic constructors for the agent to work with
screen = pygame.display.set_mode((400, 720))
t = Tetrimino(0,0)
tc = TetriminoController(screen, t)
gc = GameController(screen)

class Agent:

    def __init__(self):
        self.action_space = np.array(["left", "right", "rotate"]) # 0: move left, 1: move right, 2: rotate
        self.observation_space = np.zeros(shape=(400, 720))
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
                tc.move_left()
                self.sequence.append((gc.dt, 0))
                reward = gc.score
                self.qvalues[self.curStep][0] = reward
            case "right":
                tc.move_right()
                self.sequence.append((gc.dt, 1))
                reward = gc.score
                self.qvalues[self.curStep][1] = reward
            case "rotate":
                self.sequence.append((gc.dt, 2))
                reward = gc.score
                self.qvalues[self.curStep][2] = reward
        
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