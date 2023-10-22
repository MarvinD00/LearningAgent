import pygame
from ..Objects import Tetrimino as Tetrimino

STOP_MOVE_EVENT = pygame.USEREVENT + 1


class TetriminoController:

    def __init__(self, screen, tetrimino=Tetrimino.Tetrimino(0, 0)):
        self.tetrimino = tetrimino
        self.screen = screen
        self.last_fall_time = pygame.time.get_ticks()
        self.fall_interval = 250
        self.block_grid = []
        self.landed_tetriminos = []

        # Initialize the block grid
        for i in range(self.screen.get_height() // self.tetrimino.block_size):
            self.block_grid.append(
                [None] * (self.screen.get_width() // self.tetrimino.block_size))

    def move_left(self):
        if all(self.is_valid_move(block.rect.x - self.tetrimino.block_size, block.rect.y) for block in self.tetrimino.blocks):
            self.tetrimino.move("left")

    def move_right(self):
        if all(self.is_valid_move(block.rect.x + self.tetrimino.block_size, block.rect.y) for block in self.tetrimino.blocks):
            self.tetrimino.move("right")

    def move_down(self):
        self.update_block_grid()
        if all(self.is_valid_move(block.rect.x, block.rect.y + self.tetrimino.block_size) for block in self.tetrimino.blocks):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_fall_time >= self.fall_interval:
                print("move down")
                self.last_fall_time = current_time
                self.tetrimino.move_down()

    def rotate(self):
        self.update_block_grid()
        if all(self.is_valid_move(block.rect.x, block.rect.y) for block in self.tetrimino.blocks):
            self.tetrimino.rotate()

    def is_valid_move(self, x, y):
        # Check if the move would cause a collision with the boundaries or other blocks
        for block in self.tetrimino.blocks:
            if (x >= self.screen.get_width()):
                return False
            if (y >= self.screen.get_height()
                    or self.block_grid[y // self.tetrimino.block_size][x // self.tetrimino.block_size] is not None
                    ):
                print("landed")
                pygame.event.post(pygame.event.Event(STOP_MOVE_EVENT))
                return False
            if (
                x < 0
            ):
                return False
        return True

    def update_block_grid(self):
        # Clear the old position of the Tetrimino's blocks in the grid
        for row in range(len(self.block_grid)):
            for col in range(len(self.block_grid[row])):
                if self.block_grid[row][col] in self.tetrimino.blocks:
                    self.block_grid[row][col] = None

        # Update the game grid with the new position of the Tetrimino's blocks
        for tetrimino in self.landed_tetriminos:
            for block in tetrimino.blocks:
                row = block.rect.y // self.tetrimino.block_size
                col = block.rect.x // self.tetrimino.block_size
                self.block_grid[row][col] = block

    def new_tetrimino(self):
        self.landed_tetriminos.append(self.tetrimino)
        self.tetrimino = Tetrimino.Tetrimino(0, 0)

    def draw(self):
        self.tetrimino.draw(self.screen)
        for tetrimino in self.landed_tetriminos:
            tetrimino.draw(self.screen)
