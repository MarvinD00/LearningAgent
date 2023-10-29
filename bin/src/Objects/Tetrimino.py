import pygame
import random
from . import Block
from . import Shapes


def get_random_color():
    colors = [pygame.Color(255, 0, 0), pygame.Color(
        0, 255, 0), pygame.Color(0, 0, 255)]
    return random.choice(colors)


def get_random_shape():
    shapes = [Shapes.I_SHAPE, Shapes.J_SHAPE, Shapes.L_SHAPE,
              Shapes.O_SHAPE, Shapes.S_SHAPE, Shapes.T_SHAPE, Shapes.Z_SHAPE]
    return random.choice(shapes)


class Tetrimino(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.blocks = []
        self.block_size = Block.BLOCK_SIZE
        self.x = x
        self.y = y
        self.color = get_random_color()
        self.shape = get_random_shape()
        self.current_rotation = 0

        # Initialize with the first shape
        self.set_shape(self.shape[self.current_rotation])

    def draw(self, screen):
        for block in self.blocks:
            block.draw(screen)

    def move(self, direction):
        if direction == 'left':
            self.move_left()
        elif direction == 'right':
            self.move_right()
        elif direction == 'down':
            self.move_down()

    def move_left(self):
        self.x -= Block.BLOCK_SIZE
        for block in self.blocks:
            block.rect.x -= Block.BLOCK_SIZE

    def move_right(self):
        self.x += Block.BLOCK_SIZE
        for block in self.blocks:
            block.rect.x += Block.BLOCK_SIZE

    def move_down(self):
        self.y += Block.BLOCK_SIZE
        for block in self.blocks:
            block.rect.y += Block.BLOCK_SIZE

    def rotate(self):
        # Increment the rotation index to switch to the next rotation.
        self.current_rotation = (self.current_rotation + 1) % len(self.shape)

        # Update the blocks based on the new rotation.
        self.set_shape(self.shape[self.current_rotation])

    def unrotate(self):
        # Decrement the rotation index to switch to the previous rotation.
        self.current_rotation = (self.current_rotation - 1) % len(self.shape)

        # Update the blocks based on the new rotation.
        self.set_shape(self.shape[self.current_rotation])

    def set_shape(self, shape):
        # Clear the existing blocks
        self.blocks = []

        for relative_pos in shape:
            block_x = self.x + relative_pos[0] * Block.BLOCK_SIZE
            block_y = self.y + relative_pos[1] * Block.BLOCK_SIZE
            self.blocks.append(Block.Block(self.color, block_x, block_y))
