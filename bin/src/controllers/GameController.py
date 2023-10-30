import pygame
from . import TetriminoController
from . import AgentController as ac
import random

class GameController:

    def __init__(self, screen):
        self.screen = screen
        self.tetrimino_controller = TetriminoController.TetriminoController(screen)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lastScore = 0
        self.Agent = ac.Agent()
        self.run()

    def run(self):
        while self.running:
            self.Agent.block_grid = self.tetrimino_controller.block_grid
            self.Agent.cur_block_grid_pos = self.tetrimino_controller.cur_block_grid_pos
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == TetriminoController.END_GAME_EVENT:
                    self.Agent.reset()
                    self.reset()
                if event.type == pygame.QUIT:
                    self.Agent.write_q_table()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.tetrimino_controller.move_left()
                    elif event.key == pygame.K_d:
                        self.tetrimino_controller.move_right()
                    elif event.key == pygame.K_LEFT:
                        self.tetrimino_controller.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.tetrimino_controller.move_right()
                    elif event.key == pygame.K_s:
                        self.tetrimino_controller.move_down()
                        self.score += 5
                    elif event.key == pygame.K_DOWN:
                        self.tetrimino_controller.move_down()
                        self.score += 5
                    elif event.key == pygame.K_w:
                        self.tetrimino_controller.rotate()
                    elif event.key == pygame.K_UP:
                        self.tetrimino_controller.rotate()
                if event.type == TetriminoController.STOP_MOVE_EVENT:
                    self.tetrimino_controller.new_tetrimino()
                if event.type == TetriminoController.TETRIS_EVENT:
                    self.score += 100
                if event.type == TetriminoController.TETRIS_COMBO_DOUBLE_EVENT:
                    self.score += 250
                if event.type == TetriminoController.TETRIS_COMBO_TRIPLE_EVENT:
                    self.score += 400
                if event.type == TetriminoController.TETRIS_COMBO_QUADRUPLE_EVENT:
                    self.score += 600
                if event.type == ac.GET_REWARD_EVENT:
                    self.Agent.reward = self.score - self.lastScore
                    self.lastScore = self.score                    


            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")

            # every second increase score by 10 and move down
            self.dt += 1
            if self.dt >= 60:
                self.score += 10
                self.dt = 0
                self.tetrimino_controller.move_down()
                self.label = self.myfont.render(
                    "Score: " + str(self.score), 1, (255, 255, 0))
                print(self.Agent.get_q_table())
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

            #step
            self.Agent.step(random.choice(self.Agent.action_space))
                
            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = self.clock.tick(60) / 1000

    def reset(self):
        self.tetrimino_controller = TetriminoController.TetriminoController(self.screen)
        self.dt = 0
        self.running = True
        self.score = 0
        self.lastScore = 0
        self.run()