import pygame
from ..Objects import Tetrimino as Tetrimino
import numpy as np
import copy

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
        self.block_grid_arr = self.block_grid_arr = np.zeros(shape=(180), dtype=int)

        # Initialize the block grid
        for i in range(self.screen.get_height() // self.tetrimino.block_size):
            self.block_grid.append(
                [None] * (self.screen.get_width() // self.tetrimino.block_size))

    def move_left(self):
        if all(self.is_valid_move(block.rect.x - self.tetrimino.block_size, block.rect.y) for block in self.tetrimino.blocks):
            self.tetrimino.move("left")
        self.update_block_grid_arr()

    def move_right(self):
        if all(self.is_valid_move(block.rect.x + self.tetrimino.block_size, block.rect.y) for block in self.tetrimino.blocks):
            self.tetrimino.move("right")
        self.update_block_grid_arr()

    def move_down(self):
        if all(self.is_valid_move(block.rect.x, block.rect.y + self.tetrimino.block_size) for block in self.tetrimino.blocks):
            self.tetrimino.move("down")
        else:
            self.land()
        self.update_block_grid_arr()

    def get_predicted_punishment(self):
        # create a new tetrimino and move it down until it collides with something
        # after it collides we know where it would land if we "hard dropped"
        new_x = self.tetrimino.x
        new_y = self.tetrimino.y
        testrimino = Tetrimino.Tetrimino(new_x, new_y)
        while(True):
            if all(self.is_valid_move(block.rect.x, block.rect.y + self.tetrimino.block_size) for block in testrimino.blocks):
                testrimino.move("down")
            else:
                break
        temp_block_grid = []
        for i in range(20):
            temp_block_grid.append(
                [None] * (12))

        for block in testrimino.blocks:
            try:
                temp_block_grid[block.rect.y // self.tetrimino.block_size][block.rect.x //
                                                                       self.tetrimino.block_size] = block
            except IndexError:
                print("--------------------")
                print("Block out of bounds ::UNKNOWN ERROR::")
                print("Block y pos was: ", block.rect.y // self.tetrimino.block_size)
                print("Block x Pos was: ", block.rect.x // self.tetrimino.block_size)
                print("--------------------")

        del testrimino
        # get the holes, towers, and bumpiness of the block grid
        holes = self.get_holes(temp_block_grid)
        towers = self.get_towers(temp_block_grid)
        bumpiness = self.get_bumpiness(temp_block_grid)

        del temp_block_grid
        # calculate the score of the move
        score = -0.05 * holes - 2 * towers - 0.03 * bumpiness
        return score
    
    def rotate(self):
        # Temporarily rotate the tetrimino to check if the rotation is valid
        self.tetrimino.rotate()
        if all(self.is_valid_move(block.rect.x, block.rect.y) for block in self.tetrimino.blocks):
            # If the rotation is valid, keep the rotation
            return
        else:
            # If the rotation is not valid, revert the rotation
            self.tetrimino.unrotate()
        self.update_block_grid_arr()

    def is_valid_move(self, x, y):
        # Check if the move would cause a collision with the boundaries or other blocks
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

    def update_block_grid_arr(self):
        iter = 0
        # put all blocks into block_grid_arr as 1
        for i in range(len(self.block_grid)):
            for j in range(len(self.block_grid[i])):
                if self.block_grid[i][j] is not None:
                    self.block_grid_arr[iter] = 1
                else:
                    self.block_grid_arr[iter] = 0

    def update_block_grid(self):
        # add self.tetrimino to block grid
        for block in self.tetrimino.blocks:
            self.block_grid[block.rect.y // self.tetrimino.block_size][block.rect.x //
                                                                       self.tetrimino.block_size] = block

    def new_tetrimino(self):
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
                    self.block_grid[row][col] = None
                    self.block_grid[row + 1][col] = block
                    block.rect.y += self.tetrimino.block_size

    def land(self):
        pygame.event.post(pygame.event.Event(STOP_MOVE_EVENT))
        self.update_block_grid()
        rows = self.remove_full_rows()
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

    def debug_block_grid(self):
        for row in self.block_grid:
            for block in row:
                if (block is not None):
                    print("blok ", end="")
                else:
                    print("none ", end="")
            print("")
        print("")


    def get_holes(self, block_grid):
        holes = 0
        for col in range(len(block_grid[0])):
            found_block = False
            for row in range(len(block_grid)):
                if (block_grid[row][col] is not None):
                    found_block = True
                elif (found_block):
                    holes += 1
        return holes
    
    def get_towers(self, block_grid):
        towers = 0
        for col in range(len(block_grid[0])):
            found_block = False
            for row in range(len(block_grid)):
                if (block_grid[row][col] is not None):
                    found_block = True
                elif (found_block):
                    towers += 1
        return towers
    
    def get_bumpiness(self, block_grid):
        bumpiness = 0
        for col in range(len(block_grid[0]) - 1):
            height1 = 0
            height2 = 0
            for row in range(len(block_grid)):
                if (block_grid[row][col] is not None):
                    height1 = len(block_grid) - row
                    break
            for row in range(len(block_grid)):
                if (block_grid[row][col + 1] is not None):
                    height2 = len(block_grid) - row
                    break
            bumpiness += abs(height1 - height2)
        return bumpiness