from enum import Enum

import Camera
from Screen import *


class BlockType(Enum):
    GRASS = 1


class Block(pygame.sprite.Sprite):
    allBlocks = []
    grassLayout = [[0 for col in range(21)] for row in range(200)]

    IMG_GRASS1 = pygame.image.load("images/grass/1.png").convert()
    IMG_GRASS2 = pygame.image.load("images/grass/2.png").convert()
    IMG_GRASS3 = pygame.image.load("images/grass/3.png").convert()
    IMG_GRASS4 = pygame.image.load("images/grass/4.png").convert()
    IMG_GRASS5 = pygame.image.load("images/grass/5.png").convert()
    IMG_GRASS6 = pygame.image.load("images/grass/6.png").convert()
    IMG_GRASS7 = pygame.image.load("images/grass/7.png").convert()
    IMG_GRASS8 = pygame.image.load("images/grass/8.png").convert()
    IMG_GRASS9 = pygame.image.load("images/grass/9.png").convert()
    IMG_GRASS10 = pygame.image.load("images/grass/10.png").convert()
    IMG_GRASS11 = pygame.image.load("images/grass/11.png").convert()
    IMG_GRASS12 = pygame.image.load("images/grass/12.png").convert()
    IMG_GRASS16 = pygame.image.load("images/grass/16.png").convert()

    def __init__(self, img, pos):
        super().__init__()
        self.size = 50
        self.image = pygame.transform.scale(img, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50

    @staticmethod
    def createBlock(type, pos):

        if type == BlockType.GRASS:
            Block.grassLayout[pos[0]][pos[1]] = True

    @staticmethod
    def setBlocks():
        Block._setGrass()


    @staticmethod
    def renderAll():
        for i in Block.allBlocks:
            i.render()

    def render(self):
        screen.blit(self.image, Camera.Camera.relativePosition(self.rect.topleft))

    @staticmethod
    def _setGrass():
        for i, block in enumerate(Block.grassLayout):
            for j, exists in enumerate(block):
                if exists:
                    #Select correct image
                    img = Block.IMG_GRASS16

                    if Block.grassLayout[i][j + 1]: #if there is block below
                        if Block.grassLayout[i][j - 1]: #if there is block above and below
                            if not Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS4
                            elif Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS5
                            elif Block.grassLayout[i-1][j] and not Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS6

                        else:   #if there is block below but not above
                            if not Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS1
                            elif Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS2
                            elif Block.grassLayout[i-1][j] and not Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS3

                    else:   #if there is no block below
                        if Block.grassLayout[i][j - 1]:  # if there is block above but not below
                            if not Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS7
                            elif Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS8
                            elif Block.grassLayout[i-1][j] and not Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS9
                        else: # if there is no block above and not below
                            if not Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS10
                            elif Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS11
                            elif Block.grassLayout[i-1][j] and not Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS12


                    b = Block(img, (i, j))
                    Block.allBlocks.append(b)


