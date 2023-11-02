import pygame
from . import TetriminoController

class GameController:

    def __init__(self, screen):
        self.screen = screen
        self.tetrimino_controller = TetriminoController.TetriminoController(screen)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.score = 0

    def reset(self):
        self.tetrimino_controller = TetriminoController.TetriminoController(self.screen)
        self.dt = 0
        self.score = 0
        return self.tetrimino_controller.block_grid_arr

    def step(self, action):
        done = False
        reward = 0
        for event in pygame.event.get():
            if event.type == TetriminoController.END_GAME_EVENT:
                self.reset()
                reward = -1000
                done = True
            if event.type == pygame.QUIT:
                return 0,True
            if event.type == TetriminoController.STOP_MOVE_EVENT:
                self.tetrimino_controller.new_tetrimino()
                reward = self.getPunishment()
            if event.type == TetriminoController.TETRIS_EVENT:
                self.score += 100
            if event.type == TetriminoController.TETRIS_COMBO_DOUBLE_EVENT:
                self.score += 250
            if event.type == TetriminoController.TETRIS_COMBO_TRIPLE_EVENT:
                self.score += 400
            if event.type == TetriminoController.TETRIS_COMBO_QUADRUPLE_EVENT:
                self.score += 600
        match action:
            case "moveLeft":
                self.tetrimino_controller.move_left()
            case "moveRight":
                self.tetrimino_controller.move_right()
            case "rotate":
                self.tetrimino_controller.rotate()
            case "moveDown":
                self.tetrimino_controller.move_down()
            case _:
                print("Invalid action")
        return reward,done
            
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
