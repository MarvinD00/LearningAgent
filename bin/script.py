# Example file showing a circle moving on screen
import pygame
import random
import src.Objects
import src.controllers
from src.Objects import Tetrimino as Tetrimino
from src.controllers import TetriminoController as TetriminoController

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Tetris Learner")
clock = pygame.time.Clock()
running = True
dt = 0

# create a tetrimino
tetrimino = Tetrimino.Tetrimino(0, 0)
# create a tetrimino controller
tetrimino_controller = TetriminoController.TetriminoController(
    tetrimino, screen)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                tetrimino_controller.move_left()
            elif event.key == pygame.K_d:
                tetrimino_controller.move_right()
            elif event.key == pygame.K_LEFT:
                tetrimino_controller.move_left()
            elif event.key == pygame.K_RIGHT:
                tetrimino_controller.move_right()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # every second move down
    tetrimino_controller.move_down()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
