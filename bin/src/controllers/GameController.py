import pygame
from . import TetriminoController


class GameController:

    def __init__(self, screen):
        self.screen = screen
        self.tetrimino_controller = TetriminoController.TetriminoController(
            screen)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.run()

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
            self.tetrimino_controller.move_down()

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")

            # every second move down
            self.tetrimino_controller.move_down()

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = self.clock.tick(60) / 1000
