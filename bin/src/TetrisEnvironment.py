import pygame
from src.controllers import TetriminoController

SPEED = 30 # speed (number between 1-60)

class TetrisEnvironment:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 720))
        pygame.display.set_caption("Tetris Learner")
        self.tetrimino_controller = TetriminoController.TetriminoController(self.screen)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.score = 0
        self.last_punishment = 0

    def reset(self):
        self.score = 0
        self.last_score = 0
        self.tetrimino_controller = TetriminoController.TetriminoController(self.screen)
        self.dt = 0

    def get_state(self):
        return self.tetrimino_controller.block_grid_arr
    
    def step(self, action):

        self.reward = 0

        is_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == TetriminoController.END_GAME_EVENT:
                is_over = True
                self.reward = -100
                self.reset()
            if event.type == TetriminoController.STOP_MOVE_EVENT:
                self.tetrimino_controller.new_tetrimino()
            if event.type == TetriminoController.TETRIS_EVENT:
                self.score += 100
                self.reward += 10
            if event.type == TetriminoController.TETRIS_COMBO_DOUBLE_EVENT:
                self.score += 250
                self.reward += 25
            if event.type == TetriminoController.TETRIS_COMBO_TRIPLE_EVENT:
                self.score += 400
                self.reward += 40
            if event.type == TetriminoController.TETRIS_COMBO_QUADRUPLE_EVENT:
                self.score += 600
                self.reward += 60
        
        match(action):
            case 0: self.tetrimino_controller.move_left()
            case 1: self.tetrimino_controller.move_right()
            case 2: self.tetrimino_controller.move_down()
            case 3: self.tetrimino_controller.rotate()
            case _: ValueError("Invalid action")
        
        # after we move we get the reward
        punishment = self.tetrimino_controller.get_predicted_punishment()
        # last punishmen = -0.1
        # punishment = 0.1
        
        self.reward = punishment + self.last_punishment
        self.last_punishment = punishment

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

        return self.reward, is_over, self.score
