import numpy as np
from tf_agents.trajectories import time_step as ts
from src.controllers import TetriminoController as tc
import tf_agents as tfa
import pygame
import time

class TetrisEnvironment(tfa.environments.PyEnvironment):

    def __init__(self):
        self._action_spec = tfa.specs.array_spec.BoundedArraySpec(
            shape=(), 
            dtype=np.int32, 
            minimum=0, 
            maximum=3, 
            )
        self._observation_spec = tfa.specs.array_spec.BoundedArraySpec(
            shape=(18,10), 
            dtype=np.int32, 
            minimum=0, 
            maximum=1,
            )
        self._episode_ended = False
        self.screen = pygame.display.set_mode((400, 720))
        self.tetrimino_controller = tc.TetriminoController(self.screen)
        self.move_down_interval = 0.2
        self.last_move_down_time = 0.0
        self.clock = pygame.time.Clock()
        self.score = 0

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self.tetrimino_controller = tc.TetriminoController(self.screen)
        self.dt = 0
        self.score = 0
        self._episode_ended = False
        return ts.restart(self.getState())

    def getState(self):
        return self.tetrimino_controller.block_grid_arr
        
    def _step(self, action):
        self.render()

        if self._episode_ended:
            return self.reset()
        
        reward = 0
        episode_ended = False
        for event in pygame.event.get():
            if event.type == tc.END_GAME_EVENT:
                episode_ended = True
            if event.type == pygame.QUIT:
                return 0,True
            if event.type == tc.STOP_MOVE_EVENT:
                self.tetrimino_controller.new_tetrimino()
            if event.type == tc.TETRIS_EVENT:
                reward += 100
            if event.type == tc.TETRIS_COMBO_DOUBLE_EVENT:
                reward += 250
            if event.type == tc.TETRIS_COMBO_TRIPLE_EVENT:
                reward += 400
            if event.type == tc.TETRIS_COMBO_QUADRUPLE_EVENT:
                reward += 600
        match action:
            case 0:
                self.tetrimino_controller.move_left()
            case 1:
                self.tetrimino_controller.move_right()
            case 2:
                self.tetrimino_controller.rotate()
            case 3:
                self.tetrimino_controller.move_down()
            case _:
                print("Invalid action")
        
        current_time = time.time()
        if current_time - self.last_move_down_time >= self.move_down_interval:
            self.tetrimino_controller.move_down()
            self.last_move_down_time = current_time

        if episode_ended:
            self._episode_ended = True
            return ts.termination(observation=self.getState(), reward=reward+self.getPunishment())
        else:
            return ts.transition(observation=self.getState(), reward=reward, discount=1.0)

    def render(self):
        self.screen.fill("purple")
        self.tetrimino_controller.draw()
        pygame.display.flip()

    def getPunishment(self):
        holes = self.tetrimino_controller.get_holes()
        towers = self.tetrimino_controller.get_towers()
        bumpiness = self.tetrimino_controller.get_bumpiness()
        punishment = -0.05 * holes - 0.07 * bumpiness - 0.03 * towers
        return punishment
