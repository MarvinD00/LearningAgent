import numpy as np
from TetriminoController import TetriminoController
from ..Objects import Tetrimino as Tetrimino
import pygame

# Basic constructors for the agent to work with
screen = pygame.display.set_mode((400, 720))
t = Tetrimino(0,0)
tc = TetriminoController(screen, t)

class Agent:

    def __init__(self):
        self.action_space = np.array([0,1,2]) # 0: move left, 1: move right, 2: rotate
        self.observation_space = np.zeros(shape=(400, 720))
        self.state = tc.block_grid
        # self.memory = np.array([[0,0,0]]) TODO: Might be important later.

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
            case 0:
                tc.move_left()
                reward = 0
            case 1:
                tc.move_right()
            case 2:
                pass
        
        return (action, reward, self.state)

        pass # TODO: Implement what the agent does and calculate the reward

    def reset(self) -> None:
        """
        Resets the environment to the default settings.

        Returns
        -
        None
        """
        pass # TODO: Implement the reset of the state and reset the rewards

agent = Agent()