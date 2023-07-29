import copy
from enum import Enum

import Camera
from Screen import *
from ProjectCommon import  PATH


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
        Block._setImages(BlockType.GRASS)
        Block._setColliders()
        Block.grassLayout = [[sum(x) for x in zip(Block.grassLayout[i], Block.grassBackgroundLayout[i])] for i in range(len(Block.grassLayout))]
        Block._setImages(BlockType.GRASS_BACKGROUND)
        Block.grassLayout = [[0 for col in range(21)] for row in range(1000)]
        Block.grassBackgroundLayout = [[0 for col2 in range(21)] for row2 in range(1000)]

    @staticmethod
    def renderBackground():
        if GameInfo.GameInfo.BUILD_TYPE != GameInfo.BuildType.WEB and GameInfo.GameInfo.BUILD_TYPE != GameInfo.BuildType.ANDROID:
            for i in Block.allBackgroundBlocks:
                if Camera.Camera.isOnScreen(i.rect):
                    screen.blit(i.image, Camera.Camera.relativePosition(i.rect.topleft))

    @staticmethod
    def renderBlocks():
        for i in Block.allBlocks:
            if Camera.Camera.isOnScreen(i.rect):
                screen.blit(i.image, Camera.Camera.relativePosition(i.rect.topleft))

        #Renders all colliders
        '''for i in Block.allColliders:
            color = (i.top + i.left * 20 + i.size[0]) % 255
            pygame.draw.rect(Screen.screen, (color, color, color, 100), pygame.Rect(Camera.Camera.relativePosition(i.topleft), i.size))'''

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
    def _setImages(type):
        for i, block in enumerate(Block.grassLayout):
            for j, exists in enumerate(block):
                if exists:
                    # Select correct image
                    img = Block.IMG_GRASS[0]

                    if Block.grassLayout[i][j + 1]:  # if there is block below
                        if Block.grassLayout[i][j - 1]:  # if there is block above and below
                            if not Block.grassLayout[i - 1][j] and Block.grassLayout[i + 1][j]:
                                img = Block.IMG_GRASS[4]
                            elif Block.grassLayout[i - 1][j] and Block.grassLayout[i + 1][j]:
                                if not Block.grassLayout[i - 1][j - 1] and Block.grassLayout[i + 1][j - 1]:
                                    img = Block.IMG_GRASS[24]
                                elif Block.grassLayout[i - 1][j - 1] and not Block.grassLayout[i + 1][j - 1]:
                                    img = Block.IMG_GRASS[23]
                                elif Block.grassLayout[i - 1][j + 1] and not Block.grassLayout[i + 1][j + 1]:
                                    img = Block.IMG_GRASS[21]
                                elif not Block.grassLayout[i - 1][j + 1] and Block.grassLayout[i + 1][j + 1]:
                                    img = Block.IMG_GRASS[22]
                                else:
                                    img = Block._getCenterBlock(i, j)
                            elif Block.grassLayout[i - 1][j] and not Block.grassLayout[i + 1][j]:
                                img = Block.IMG_GRASS[6]
                            else:
                                img = Block.IMG_GRASS[14]

                        else:  # if there is block below but not above
                            if not Block.grassLayout[i - 1][j] and Block.grassLayout[i + 1][j]:
                                if Block.grassLayout[i][j + 1] and not Block.grassLayout[i + 1][j + 1]:
                                    img = Block.IMG_GRASS[17]
                                else:
                                    img = Block.IMG_GRASS[1]
                            elif Block.grassLayout[i - 1][j] and Block.grassLayout[i + 1][j]:
                                img = Block.IMG_GRASS[2]
                            elif Block.grassLayout[i - 1][j] and not Block.grassLayout[i + 1][j]:
                                if Block.grassLayout[i][j + 1] and not Block.grassLayout[i - 1][j + 1]:
                                    img = Block.IMG_GRASS[18]
                                else:
                                    img = Block.IMG_GRASS[3]

                    else:  # if there is no block below
                        if Block.grassLayout[i][j - 1]:  # if there is block above but not below
                            if not Block.grassLayout[i - 1][j] and Block.grassLayout[i + 1][j]:
                                if not Block.grassLayout[i + 1][j - 1]:
                                    img = Block.IMG_GRASS[19]
                                else:
                                    img = Block.IMG_GRASS[7]
                            elif Block.grassLayout[i - 1][j] and Block.grassLayout[i + 1][j]:
                                img = Block.IMG_GRASS[8]
                            elif Block.grassLayout[i - 1][j] and not Block.grassLayout[i + 1][j]:
                                if not Block.grassLayout[i - 1][j - 1]:
                                    img = Block.IMG_GRASS[20]
                                else:
                                    img = Block.IMG_GRASS[9]
                            else:
                                img = Block.IMG_GRASS[15]
                        else:  # if there is no block above and not below
                            if not Block.grassLayout[i - 1][j] and Block.grassLayout[i + 1][j]:
                                img = Block.IMG_GRASS[10]
                            elif Block.grassLayout[i - 1][j] and Block.grassLayout[i + 1][j]:
                                img = Block.IMG_GRASS[11]
                            elif Block.grassLayout[i - 1][j] and not Block.grassLayout[i + 1][j]:
                                img = Block.IMG_GRASS[12]

                    if type == BlockType.GRASS:
                        b = Block(img, (i, j))
                        Block.allBlocks.append(b)
                    if type == BlockType.GRASS_BACKGROUND:
                        b = Block(img, (i, j), True)
                        Block.allBackgroundBlocks.append(b)

    @staticmethod
    def _setColliders():
        #layoutCopy = Block.grassLayout.copy()
        layoutCopy = copy.deepcopy(Block.grassLayout)
        for i, b in enumerate(layoutCopy):
            for j, block in enumerate(b):
                if layoutCopy[i][j] is True and not Block._isSurroundedByBlocks(i, j): #if block exists and is not surrounded, then create collider
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
        if Block.grassLayout[i][j + 1] and Block.grassLayout[i][j - 1] and \
                Block.grassLayout[i + 1][j] and Block.grassLayout[i - 1][j]:
            return True
        else:
            return False

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
