import gymnasium  as gym
import numpy as np
import pandas as pd
import pygame
from gymnasium import spaces

class TetrisEnvironment(gym.Env):
    def __init__(self, game_controller):
        super(TetrisEnvironment, self).__init__()

        # Define your action and observation space
        self.action_space = spaces.Discrete(4) 
        self.action_space = np.array(["moveLeft", "moveRight", "rotate", "moveDown"])
        self._max_episode_steps = 1000  
        self.game_controller = game_controller
        self.observation_space =  np.array(self.game_controller.tetrimino_controller.block_grid_arr)

    def reset(self):
        # Reset the game controller
        self.game_controller.reset()

        # Return the initial observation
        return self.game_controller.tetrimino_controller.block_grid_arr

    def step(self, action):
        # Execute one time step within the environment
        reward,done = self.game_controller.step(action)
        
        return self.game_controller.tetrimino_controller.block_grid_arr, reward, done

    def render(self, mode='human'):
        # Render the game controller
        return self.game_controller.render()
