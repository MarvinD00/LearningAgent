import numpy as np
import pandas as pd
import pygame

GET_REWARD_EVENT = pygame.USEREVENT + 7
RESET_GAME_EVENT = pygame.USEREVENT + 8

class Agent:

    def __init__(self):
        self.action_space = np.array(["left", "right", "rotate", "down"])
        self.ALPHA = 0.5
        self.QVALUE = 0
        self.reward = 0
        self.q_table_length = 1000
        self.q_table = pd.DataFrame({"State":np.zeros(self.q_table_length), "moveLeft":np.zeros(self.q_table_length), "moveRight":np.zeros(self.q_table_length), "moveDown":np.zeros(self.q_table_length), "rotate":np.zeros(self.q_table_length)})
        self.q_table.index = self.q_table["State"]
        self.cur_step = 0
        self.cur_block_grid_pos = []
        self.block_grid = []

    def step(self, action) -> tuple:
        """
        Proceeds the action chosen by the agent.

        Parameters
        -
        action: int -> random value of self.action_space

        Returns
        -
        reward: tuple -> (action, reward, state)
        """
        pygame.event.post(pygame.event.Event(GET_REWARD_EVENT))
        match action:
            case "left":
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a, 'mod': 0, 'unicode': 'a'}))
                self.q_table["moveLeft"][self.getState()] = self.reward
            case "right":
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_d, 'mod': 0, 'unicode': 'd'})) 
                self.q_table["moveRight"][self.getState()] = self.reward
            case "rotate":
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_w, 'mod': 0, 'unicode': 'w'}))
                self.q_table["rotate"][self.getState()] = self.reward
            case "down":
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_s, 'mod': 0, 'unicode': 's'}))
                self.q_table["moveDown"][self.getState()] = self.reward
        #setze state auf current state
        self.q_table["State"][self.getState()] = self.getState()
        return action

    def reset(self) -> None:
        """
        Resets the environment to the default settings.

        Returns
        -
        None
        """
        self.QVALUE = 0
        self.cur_step = 0

    def getReward(self, reward):
        self.QVALUE = self.QVALUE + self.ALPHA * (reward + max(self.q_table) - self.QVALUE)

    def getState(self):
        b = 0
        for row in self.block_grid:
            for block in row:
                b = b << 1
                if block is not None:
                    b = b | 1
        for row in self.cur_block_grid_pos:
            for block in row:
                b = b << 1
                if block is not None:
                    b = b | 1
        return b
    
    def get_q_table(self):
        return self.q_table