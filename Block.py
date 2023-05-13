import pygame
from enum import Enum

import Camera
from Screen import *


class Block(Enum):
    GRASS = 1


class Block(pygame.sprite.Sprite):
    allBlocks = []

    IMG_GRASS1 = pygame.image.load("images/Grass/1.png")
    IMG_GRASS2 = pygame.image.load("images/Grass/2.png")
    IMG_GRASS3 = pygame.image.load("images/Grass/3.png")

    def __init__(self, pos):
        super().__init__()
        self.size = 50
        self.image = pygame.transform.scale(Block.IMG_GRASS2, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    @staticmethod
    def renderAll():
        for b in Block.allBlocks:
            b.render()

    def render(self):
        screen.blit(self.image, self.rect.topleft)
        #print(self.rect.size)

