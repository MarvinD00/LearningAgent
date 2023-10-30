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
        self.q_table = pd.DataFrame(columns=["moveLeft", "moveRight", "moveDown", "rotate"], index=["State"])
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
                self.update_q_table(self.getState(), "moveLeft", self.reward)
            case "right":
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_d, 'mod': 0, 'unicode': 'd'})) 
                self.update_q_table(self.getState(), "moveRight", self.reward)
            case "rotate":
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_w, 'mod': 0, 'unicode': 'w'}))
                self.update_q_table(self.getState(), "rotate", self.reward)
            case "down":
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_s, 'mod': 0, 'unicode': 's'}))
                self.update_q_table(self.getState(), "moveDown", self.reward)
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

    def update_q_table(self, state, action, reward):
        if state not in self.q_table.index:
            # if state not in q table -> add a new row
            new_row = pd.Series([0] * (len(self.q_table.columns)), name=state, index=self.q_table.columns)
            self.q_table = pd.concat([self.q_table, new_row.to_frame().T])

        # update q value
        self.q_table.at[state, action] = reward

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
        return str(b)
    
    def get_q_table(self):
        return self.q_table
    
    def write_q_table(self):
        self.q_table.to_csv("q_table.csv")