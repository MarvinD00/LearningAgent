import pygame
from src.controllers import TetriminoController
import numpy as np

SPEED = 55 # speed (number between 1-60)

class TetrisEnvironment:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 720))
        pygame.display.set_caption("Tetris Learner")
        self.tetrimino_controller = TetriminoController.TetriminoController(self.screen)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.score = 0

    def reset(self):
        self.score = 0
        self.tetrimino_controller = TetriminoController.TetriminoController(self.screen)
        self.dt = 0

    def get_reward(self):
        return self.tetrimino_controller.get_reward()

    def get_state(self):
        block_grid = self.tetrimino_controller.block_grid_arr
        tetrimino_arr = self.tetrimino_controller.get_tetrimino()

        block_grid = np.append(block_grid, tetrimino_arr)

        return block_grid
    
    def step(self, action):

        reward = -1

        is_over = False
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == TetriminoController.END_GAME_EVENT:
                is_over = True
                reward = -100
            if event.type == TetriminoController.STOP_MOVE_EVENT:
                self.tetrimino_controller.new_tetrimino()
            if event.type == TetriminoController.TETRIS_EVENT:
                self.score += 100
                reward = 1
            if event.type == TetriminoController.TETRIS_COMBO_DOUBLE_EVENT:
                self.score += 250
                reward = 2
            if event.type == TetriminoController.TETRIS_COMBO_TRIPLE_EVENT:
                self.score += 400
                reward = 4
            if event.type == TetriminoController.TETRIS_COMBO_QUADRUPLE_EVENT:
                self.score += 600
                reward = 6
        
        match(action):
            case 0: self.tetrimino_controller.move_left()
            case 1: self.tetrimino_controller.move_right()
            case 2: self.tetrimino_controller.rotate()
            case 3: do_nothing = True
            case _: ValueError("Invalid action")

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("purple")

        # every second increase score by 10 and move down
        self.dt += 1
        if self.dt >= 61-SPEED:
            self.score += 1
            self.dt = 0
            self.tetrimino_controller.move_down()
            self.label = self.myfont.render(
                "Score: " + str(self.score), 1, (255, 255, 0))
        # draw label
        # render text
        self.myfont = pygame.font.Font(None, 30)
        self.label = self.myfont.render(
            f"Score: {self.score}", 1, (255, 255, 0))
        self.screen.blit(self.label, (0, 0))

        # every second move down and draw
        self.tetrimino_controller.draw()

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = self.clock.tick(60) / 1000

        return reward, is_over, self.score
