import copy
from enum import Enum

import pygame

from src.camera import Camera
from src.project_common import PATH
from src.screen import screen


class BlockType(Enum):
    GRASS = 1
    GRASS_BACKGROUND = 2


class Block(pygame.sprite.Sprite):
    allBlocks = []
    allBackgroundBlocks = []
    allColliders = []
    grassLayout = [[0 for col in range(21)] for row in range(1000)]
    grassBackgroundLayout = [[0 for col2 in range(21)] for row2 in range(1000)]

    IMG_GRASS = []
    _IMG_GRASS_CENTER = []  # images of grass which is surrounded by other blocks

    _loadedImages = False

    def __init__(self, img, pos, isBackground = False):
        super().__init__()
        SIZE = 50
        self.image = pygame.transform.scale(img, (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50
        self.backgroundColor = pygame.Surface(self.image.get_size()).convert_alpha()
        if isBackground:
            c = 180
            self.backgroundColor.fill((c, c, c))
            self.image.blit(self.backgroundColor, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    @staticmethod
    def createBlock(type, pos):
        if type == BlockType.GRASS:
            Block.grassLayout[pos[0]][pos[1]] = True
        if type == BlockType.GRASS_BACKGROUND:
            Block.grassBackgroundLayout[pos[0]][pos[1]] = True

    @staticmethod
    def setBlocks():
        if not Block._loadedImages:
            Block._loadImages()
        Block._setImages(BlockType.GRASS, Block.grassLayout)
        Block._setColliders()

        Block._expandBackgroundLayer()
        Block._setImages(BlockType.GRASS_BACKGROUND, Block.grassBackgroundLayout)

        # Clear all layouts
        Block.grassLayout = [[0 for col in range(21)] for row in range(1000)]
        Block.grassBackgroundLayout = [[0 for col in range(21)] for row in range(1000)]

    @staticmethod
    def renderBackground():
        for i in Block.allBackgroundBlocks:
            if Camera.isOnScreen(i.rect):
                screen.blit(i.image, Camera.relativePosition(i.rect.topleft))

    @staticmethod
    def renderBlocks():
        for i in Block.allBlocks:
            if Camera.isOnScreen(i.rect):
                screen.blit(i.image, Camera.relativePosition(i.rect.topleft))

        #Renders all colliders
        '''for i in Block.allColliders:
            color = ((i.top + i.left * 20 + i.size[0]) % 155) + 100
            pygame.draw.rect(screen, (color, color/6, color/6, 100), pygame.Rect(camera.Camera.relativePosition(i.topleft), i.size))'''  # noqa: E501

    @staticmethod
    def _loadImages():
        Block.IMG_GRASS.append(pygame.image.load(f"{PATH}images/grass/13.png").convert_alpha())  # default image
        for i in range(24):
            img = pygame.image.load(f"{PATH}images/grass/{i + 1}.png").convert_alpha()
            Block.IMG_GRASS.append(img)
        for i in range(4):
            img = pygame.image.load(f"{PATH}images/grass/inside{i + 1}.png").convert()
            Block._IMG_GRASS_CENTER.append(img)

        Block._loadedImages = True

    @staticmethod
    def _setImages(type, layout):
        for i, block in enumerate(layout):
            for j, exists in enumerate(block):
                if exists:
                    # Select correct image
                    img = Block.IMG_GRASS[0]

                    if layout[i][j + 1]:  # if there is block below
                        if layout[i][j - 1]:  # if there is block above and below
                            if not layout[i - 1][j] and layout[i + 1][j]:
                                img = Block.IMG_GRASS[4]
                            elif layout[i - 1][j] and layout[i + 1][j]:
                                if not layout[i - 1][j - 1] and layout[i + 1][j - 1]:
                                    img = Block.IMG_GRASS[24]
                                elif layout[i - 1][j - 1] and not layout[i + 1][j - 1]:
                                    img = Block.IMG_GRASS[23]
                                elif layout[i - 1][j + 1] and not layout[i + 1][j + 1]:
                                    img = Block.IMG_GRASS[21]
                                elif not layout[i - 1][j + 1] and layout[i + 1][j + 1]:
                                    img = Block.IMG_GRASS[22]
                                else:
                                    img = Block._getCenterBlock(i, j)
                            elif layout[i - 1][j] and not layout[i + 1][j]:
                                img = Block.IMG_GRASS[6]
                            else:
                                img = Block.IMG_GRASS[14]

                        else:  # if there is block below but not above
                            if not layout[i - 1][j] and layout[i + 1][j]:
                                if layout[i][j + 1] and not layout[i + 1][j + 1]:
                                    img = Block.IMG_GRASS[17]
                                else:
                                    img = Block.IMG_GRASS[1]
                            elif layout[i - 1][j] and layout[i + 1][j]:
                                img = Block.IMG_GRASS[2]
                            elif layout[i - 1][j] and not layout[i + 1][j]:
                                if layout[i][j + 1] and not layout[i - 1][j + 1]:
                                    img = Block.IMG_GRASS[18]
                                else:
                                    img = Block.IMG_GRASS[3]

                    else:  # if there is no block below
                        if layout[i][j - 1]:  # if there is block above but not below
                            if not layout[i - 1][j] and layout[i + 1][j]:
                                if not layout[i + 1][j - 1]:
                                    img = Block.IMG_GRASS[19]
                                else:
                                    img = Block.IMG_GRASS[7]
                            elif layout[i - 1][j] and layout[i + 1][j]:
                                img = Block.IMG_GRASS[8]
                            elif layout[i - 1][j] and not layout[i + 1][j]:
                                if not layout[i - 1][j - 1]:
                                    img = Block.IMG_GRASS[20]
                                else:
                                    img = Block.IMG_GRASS[9]
                            else:
                                img = Block.IMG_GRASS[15]
                        else:  # if there is no block above and not below
                            if not layout[i - 1][j] and layout[i + 1][j]:
                                img = Block.IMG_GRASS[10]
                            elif layout[i - 1][j] and layout[i + 1][j]:
                                img = Block.IMG_GRASS[11]
                            elif layout[i - 1][j] and not layout[i + 1][j]:
                                img = Block.IMG_GRASS[12]

                    if type == BlockType.GRASS:
                        b = Block(img, (i, j))
                        Block.allBlocks.append(b)
                    if type == BlockType.GRASS_BACKGROUND:
                        if Block.grassLayout[i][j] and (img == Block.IMG_GRASS[1] or
                                                        img == Block.IMG_GRASS[3] or
                                                        img == Block.IMG_GRASS[10] or
                                                        img == Block.IMG_GRASS[12]):
                            continue
                        b = Block(img, (i, j), True)
                        Block.allBackgroundBlocks.append(b)

    @staticmethod
    def _setColliders():
        layoutCopy = copy.deepcopy(Block.grassLayout)
        for i, b in enumerate(layoutCopy):
            for j, block in enumerate(b):
                # if block exists and is not surrounded, then create collider
                if layoutCopy[i][j] is True and not Block._isSurroundedByBlocks(i, j):
                    deltaY = 1

                    while layoutCopy[i][j + deltaY] is True and Block._isSurroundedByBlocks(i, j + deltaY) is False:
                        deltaY += 1

                    if deltaY > 1:
                        for k in range(deltaY):
                            layoutCopy[i][j + k] = False
                        collider = pygame.Rect(i * 50 - 25, j * 50 - 25, 50, deltaY * 50)
                        Block.allColliders.append(collider)
                    else:
                        deltaX = 1

                        while layoutCopy[i + deltaX][j] is True and not Block._isSurroundedByBlocks(i + deltaX, j):
                            deltaX += 1

                        for k in range(deltaX):
                            layoutCopy[i + k][j] = False
                        collider = pygame.Rect(i * 50 - 25, j * 50 - 25, deltaX * 50,  50)
                        Block.allColliders.append(collider)

    @staticmethod
    def _isSurroundedByBlocks(i, j):
        return Block.grassLayout[i][j + 1] and Block.grassLayout[i][j - 1] and \
                Block.grassLayout[i + 1][j] and Block.grassLayout[i - 1][j]

    @staticmethod
    def _getCenterBlock(i, j):
        # here there is 10% chance of showing different block than default
        if not Block.grassLayout[i][j - 2] or not Block.grassLayout[i][j + 2] or not Block.grassLayout[i][j + 3] or \
                not Block.grassLayout[i - 2][j] or not Block.grassLayout[i + 2][j]:
            return Block.IMG_GRASS[5]
        else:
            pseudoRandNum = (pow(i, 3) + pow(j, 2)) % 40
            if pseudoRandNum < len(Block._IMG_GRASS_CENTER):
                return Block._IMG_GRASS_CENTER[pseudoRandNum]
            else:
                return Block.IMG_GRASS[5]

    @staticmethod
    def _expandBackgroundLayer():
        for c in range(2):
            clone = copy.deepcopy(Block.grassBackgroundLayout)
            for i, a in enumerate(clone):
                for j, exists in enumerate(a):
                    if exists:
                        if Block.grassLayout[i+1][j+1]:
                            Block.grassBackgroundLayout[i+1][j+1] = True
                        if Block.grassLayout[i+1][j]:
                            Block.grassBackgroundLayout[i+1][j] = True
                        if Block.grassLayout[i+1][j-1]:
                            Block.grassBackgroundLayout[i+1][j-1] = True
                        if Block.grassLayout[i][j+1]:
                            Block.grassBackgroundLayout[i][j+1] = True
                        if Block.grassLayout[i][j-1]:
                            Block.grassBackgroundLayout[i][j-1] = True
                        if Block.grassLayout[i-1][j+1]:
                            Block.grassBackgroundLayout[i-1][j+1] = True
                        if Block.grassLayout[i-1][j]:
                            Block.grassBackgroundLayout[i-1][j] = True
                        if Block.grassLayout[i-1][j-1]:
                            Block.grassBackgroundLayout[i-1][j-1] = True
