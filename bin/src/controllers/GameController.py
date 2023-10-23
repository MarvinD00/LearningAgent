import pygame
from . import TetriminoController


class GameController:

    def __init__(self, screen):
        self.screen = screen
        self.tetrimino_controller = TetriminoController.TetriminoController(screen)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.run()

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == TetriminoController.END_GAME_EVENT:
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
                    elif event.key == pygame.K_w:
                        self.tetrimino_controller.rotate()
                    elif event.key == pygame.K_UP:
                        self.tetrimino_controller.rotate()
                if event.type == TetriminoController.STOP_MOVE_EVENT:
                    self.tetrimino_controller.new_tetrimino()

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")

            # every second increase score by 10
            if self.dt > 1:
                self.score += 10
                self.label = self.myfont.render(
                    "Score: " + str(self.score), 1, (255, 255, 0))
                self.dt = 0

            # draw label
            # render text
            self.myfont = pygame.font.Font(None, 30)
            self.label = self.myfont.render(f"Score: {self.score}", 1, (255, 255, 0))
            self.screen.blit(self.label, (0, 0))

            # every second move down
            # and draw
            self.tetrimino_controller.draw()
            self.tetrimino_controller.move_down()

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = self.clock.tick(60) / 1000
