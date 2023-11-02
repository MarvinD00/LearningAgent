import gymnasium  as gym
import numpy as np
from gymnasium import spaces

class TetrisEnvironment(gym.Env):
    def __init__(self, game_controller):
        super(TetrisEnvironment, self).__init__()

        # Define your action and observation space
        self.action_space = spaces.Discrete(4) 
        self.action_space = np.array(["moveLeft", "moveRight", "rotate", "moveDown"])
        self._max_episode_steps = 1000  
        self.game_controller = game_controller
        self.grid_width = 10
        self.grid_height = 18
        self.observation_space = spaces.Box(0, 1, shape=(self.grid_height, self.grid_width), dtype=np.float32)

    def reset(self):
        # Reset the game controller
        self.game_controller.reset()
        obs = self.get_observation()
        # Return the initial observation
        return obs

    def step(self, action):
        # Execute one time step within the environment
        reward,done = self.game_controller.step(action)
        obs = self.get_observation()
        return obs, reward, done

    def render(self, mode='human'):
        # Render the game controller
        return self.game_controller.render()

    def get_observation(self):
        # Get the observation from the game controller
        return self.game_controller.tetrimino_controller.block_grid_arr