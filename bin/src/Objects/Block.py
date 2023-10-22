import pygame
import random
from . import Shapes

BLOCK_SIZE = 40


class Block:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    