import pygame
from ..Objects import Tetrimino as Tetrimino

STOP_MOVE_EVENT = pygame.USEREVENT + 1
END_GAME_EVENT = pygame.USEREVENT + 2
TETRIS_EVENT = pygame.USEREVENT + 3
TETRIS_COMBO_DOUBLE_EVENT = pygame.USEREVENT + 4
TETRIS_COMBO_TRIPLE_EVENT = pygame.USEREVENT + 5
TETRIS_COMBO_QUADRUPLE_EVENT = pygame.USEREVENT + 6

class TetriminoController:

    def __init__(self, screen, tetrimino=Tetrimino.Tetrimino(0, 0)):
        self.tetrimino = tetrimino
        self.screen = screen
        self.last_fall_time = pygame.time.get_ticks()
        self.fall_interval = 200
        self.block_grid = []
        self.cur_block_grid_pos = []

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
        print("move down")
        if all(self.is_valid_move(block.rect.x, block.rect.y + self.tetrimino.block_size) for block in self.tetrimino.blocks):
            self.tetrimino.move("down")
        else:
            print("landed")
            self.land()
            
    def rotate(self):
        # Temporarily rotate the tetrimino to check if the rotation is valid
        self.tetrimino.rotate()
        if all(self.is_valid_move(block.rect.x, block.rect.y) for block in self.tetrimino.blocks):
            # If the rotation is valid, keep the rotation
            return
        else:
            # If the rotation is not valid, revert the rotation
            self.tetrimino.unrotate()

    def is_valid_move(self, x, y):
        # Check if the move would cause a collision with the boundaries or other blocks
        for block in self.tetrimino.blocks:
            if (x >= self.screen.get_width()):
                return False
            if (y >= self.screen.get_height()
                or self.block_grid[y // self.tetrimino.block_size][x // self.tetrimino.block_size] is not None
                ):
                return False
            if (
                x < 0
            ):
                return False
        return True

    def update_block_grid(self):
        print("update block grid")
        self.cur_block_grid_pos = []
        # add self.tetrimino to block grid
        for block in self.tetrimino.blocks:
            self.block_grid[block.rect.y // self.tetrimino.block_size][block.rect.x //
                                                                       self.tetrimino.block_size] = block
            self.cur_block_grid_pos[block.rect.y // self.tetrimino.block_size][block.rect.x //
                                                                       self.tetrimino.block_size] = block
        
    def new_tetrimino(self):
        print("new tetrimino")
        self.tetrimino = Tetrimino.Tetrimino(
            self.screen.get_width() // 2, 0)
        if self.is_game_over():
            pygame.event.post(pygame.event.Event(END_GAME_EVENT))

    def draw(self):
        self.tetrimino.draw(self.screen)
        for row in self.block_grid:
            for block in row:
                if block is not None:
                    block.draw(self.screen)

    def is_game_over(self):
        # Check if the top row of the grid contains any filled cells
        return any(cell is not None for cell in self.block_grid[0])

    def remove_full_rows(self):
        removed_rows = []
        for row in range(len(self.block_grid) - 1, -1, -1):
            if all(cell is not None for cell in self.block_grid[row]):
                removed_rows.append(row)

        for row in removed_rows:
            for col in range(len(self.block_grid[row])):
                self.block_grid[row][col] = None
        return removed_rows

    def move_blocks_down(self):
        for row in reversed(range(len(self.block_grid) - 1)):
            for col in range(len(self.block_grid[row])):
                block = self.block_grid[row][col]
                if block is not None:
                    new_row = row
                    while (new_row < len(self.block_grid) - 1 and self.block_grid[new_row + 1][col] is None):
                        # Move the block down in the grid
                        self.block_grid[new_row + 1][col] = block
                        self.block_grid[new_row][col] = None
                        # Update the block's position
                        block.rect.y += self.tetrimino.block_size
                        new_row += 1
                    print("Block moved down")

    def land(self):
        pygame.event.post(pygame.event.Event(STOP_MOVE_EVENT))
        self.update_block_grid()
        self.debug_block_grid()
        rows = self.remove_full_rows()
        self.debug_block_grid()
        if (rows):
            self.move_blocks_down()
        if(len(rows) == 1):
            pygame.event.post(pygame.event.Event(TETRIS_EVENT))
        elif(len(rows) == 2):
            pygame.event.post(pygame.event.Event(TETRIS_COMBO_DOUBLE_EVENT))
        elif(len(rows) == 3):
            pygame.event.post(pygame.event.Event(TETRIS_COMBO_TRIPLE_EVENT))
        elif(len(rows) == 4):
            pygame.event.post(pygame.event.Event(TETRIS_COMBO_QUADRUPLE_EVENT))
        self.debug_block_grid()

    def debug_block_grid(self):
        for row in self.block_grid:
            for block in row:
                if (block is not None):
                    print("blok ", end="")
                else:
                    print("none ", end="")
            print("")
        print("")
