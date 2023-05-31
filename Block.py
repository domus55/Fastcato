from enum import Enum

import Camera
import Screen
from Screen import *


class BlockType(Enum):
    GRASS = 1


class Block(pygame.sprite.Sprite):
    allBlocks = []
    grassLayout = [[0 for col in range(21)] for row in range(200)]

    IMG_GRASS = []

    _loadedImages = False

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
        if not Block._loadedImages:
            Block._loadImages()
        Block._setGrass()


    @staticmethod
    def renderAll():
        for i in Block.allBlocks:
            if Camera.Camera.isOnScreen(i.rect):
                i.render()

    def render(self):
        screen.blit(self.image, Camera.Camera.relativePosition(self.rect.topleft))

    @staticmethod
    def _loadImages():
        Block.IMG_GRASS.append(pygame.image.load(f"images/grass/13.png").convert_alpha()) #default image
        for i in range(24):
            img = pygame.image.load(f"images/grass/{i+1}.png").convert_alpha()
            Block.IMG_GRASS.append(img)

    @staticmethod
    def _setGrass():
        for i, block in enumerate(Block.grassLayout):
            for j, exists in enumerate(block):
                if exists:
                    #Select correct image
                    img = Block.IMG_GRASS[0]

                    if Block.grassLayout[i][j + 1]: #if there is block below
                        if Block.grassLayout[i][j - 1]: #if there is block above and below
                            if not Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS[4]
                            elif Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                if not Block.grassLayout[i-1][j-1] and Block.grassLayout[i+1][j-1]:
                                    img = Block.IMG_GRASS[24]
                                elif Block.grassLayout[i-1][j-1] and not Block.grassLayout[i+1][j-1]:
                                    img = Block.IMG_GRASS[23]
                                elif Block.grassLayout[i-1][j+1] and not Block.grassLayout[i+1][j+1]:
                                    img = Block.IMG_GRASS[21]
                                elif not Block.grassLayout[i-1][j+1] and Block.grassLayout[i+1][j+1]:
                                    img = Block.IMG_GRASS[22]
                                else:
                                    img = Block.IMG_GRASS[5]
                            elif Block.grassLayout[i-1][j] and not Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS[6]
                            else:
                                img = Block.IMG_GRASS[14]

                        else:   #if there is block below but not above
                            if not Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                if Block.grassLayout[i][j+1] and not Block.grassLayout[i+1][j+1]:
                                    img = Block.IMG_GRASS[17]
                                else:
                                    img = Block.IMG_GRASS[1]
                            elif Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS[2]
                            elif Block.grassLayout[i-1][j] and not Block.grassLayout[i+1][j]:
                                if Block.grassLayout[i][j+1] and not Block.grassLayout[i-1][j+1]:
                                    img = Block.IMG_GRASS[18]
                                else:
                                    img = Block.IMG_GRASS[3]

                    else:   #if there is no block below
                        if Block.grassLayout[i][j - 1]:  # if there is block above but not below
                            if not Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                if not Block.grassLayout[i+1][j-1]:
                                    img = Block.IMG_GRASS[19]
                                else:
                                    img = Block.IMG_GRASS[7]
                            elif Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS[8]
                            elif Block.grassLayout[i-1][j] and not Block.grassLayout[i+1][j]:
                                if not Block.grassLayout[i-1][j-1]:
                                    img = Block.IMG_GRASS[20]
                                else:
                                    img = Block.IMG_GRASS[9]
                            else:
                                img = Block.IMG_GRASS[15]
                        else: # if there is no block above and not below
                            if not Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS[10]
                            elif Block.grassLayout[i-1][j] and Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS[11]
                            elif Block.grassLayout[i-1][j] and not Block.grassLayout[i+1][j]:
                                img = Block.IMG_GRASS[12]


                    b = Block(img, (i, j))
                    Block.allBlocks.append(b)

        Block.grassLayout = [[0 for col in range(21)] for row in range(200)]


