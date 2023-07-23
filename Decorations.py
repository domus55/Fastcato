from enum import Enum

import GameInfo
import Camera
from ProjectCommon import PATH, loadImage
from Screen import screen


class Decorations:
    class Type(Enum):
        TREE_SMALL = 0
        TREE_BIG = 1
        BUSH = 2
        GRASS = 3
        STONE_SMALL = 4
        STONE_BIG = 5
        BALLOON = 6
        CAKE = 7

    allDecorations = []

    # Images
    IMG_TREE_SMALL1 = loadImage(f"{PATH}images/decorations/treeSmall1.png", (380, 430))
    IMG_TREE_SMALL2 = loadImage(f"{PATH}images/decorations/treeSmall2.png", (340, 360))
    IMG_TREE_SMALL3 = loadImage(f"{PATH}images/decorations/treeSmall3.png", (300, 350))
    IMG_TREE_SMALL4 = loadImage(f"{PATH}images/decorations/treeSmall4.png", (200, 300))
    IMG_TREE_BIG1 = loadImage(f"{PATH}images/decorations/treeBig1.png", (500, 500))
    IMG_TREE_BIG2 = loadImage(f"{PATH}images/decorations/treeBig2.png", (500, 500))
    IMG_BUSH1 = loadImage(f"{PATH}images/decorations/bush1.png", (75, 75))
    IMG_BUSH2 = loadImage(f"{PATH}images/decorations/bush2.png", (75, 50))
    IMG_BUSH3 = loadImage(f"{PATH}images/decorations/bush3.png", (75, 50))
    IMG_BUSH4 = loadImage(f"{PATH}images/decorations/bush4.png", (75, 50))
    IMG_BUSH5 = loadImage(f"{PATH}images/decorations/bush5.png", (75, 50))
    IMG_GRASS1 = loadImage(f"{PATH}images/decorations/grass1.png", (40, 40))
    IMG_GRASS2 = loadImage(f"{PATH}images/decorations/grass2.png", (40, 40))
    IMG_GRASS3 = loadImage(f"{PATH}images/decorations/grass3.png", (40, 40))
    IMG_STONE_SMALL1 = loadImage(f"{PATH}images/decorations/stoneSmall1.png", (20, 20))
    IMG_STONE_SMALL2 = loadImage(f"{PATH}images/decorations/stoneSmall2.png", (40, 25))
    IMG_STONE_SMALL3 = loadImage(f"{PATH}images/decorations/stoneSmall3.png", (50, 40))
    IMG_STONE_BIG1 = loadImage(f"{PATH}images/decorations/stoneBig1.png", (65, 45))
    IMG_STONE_BIG2 = loadImage(f"{PATH}images/decorations/stoneBig2.png", (60, 50))
    IMG_STONE_BIG3 = loadImage(f"{PATH}images/decorations/stoneBig3.png", (140, 80))
    IMG_BALLOON1 = loadImage(f"{PATH}images/decorations/balloon1.png", (100, 100))
    IMG_BALLOON2 = loadImage(f"{PATH}images/decorations/balloon2.png", (100, 100))
    IMG_BALLOON3 = loadImage(f"{PATH}images/decorations/balloon3.png", (100, 100))
    IMG_BALLOON4 = loadImage(f"{PATH}images/decorations/balloon4.png", (100, 100))
    IMG_CAKE = loadImage(f"{PATH}images/decorations/cake.png", (124, 124))


    def __init__(self, type, pos):
        typeStr = "Decorations.IMG_" + str(type)[5:]
        if type == Decorations.Type.TREE_SMALL:
            typeStr += str(pos[0] % 4 + 1)
        if type == Decorations.Type.TREE_BIG:
            typeStr += str(pos[0] % 2 + 1)
        elif type == Decorations.Type.BUSH:
            typeStr += str(pos[0] % 5 + 1)
        elif type == Decorations.Type.GRASS:
            typeStr += str(pos[0] % 3 + 1)
        elif type == Decorations.Type.STONE_SMALL:
            typeStr += str(pos[0] % 3 + 1)
        elif type == Decorations.Type.STONE_BIG:
            typeStr += str(pos[0] % 3 + 1)
        elif type == Decorations.Type.BALLOON:
            typeStr += str(pos[0] % 3 + 1)

        img = eval(typeStr)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50 + 25 - self.rect.size[1] / 2

    @staticmethod
    def add(type, pos):
        # Don't render trees if game is in WEB, then we can get around +25% FPS
        if GameInfo.GameInfo.BUILD_TYPE == GameInfo.BuildType.WEB:
            if type == Decorations.Type.TREE_SMALL or type == Decorations.Type.TREE_BIG:
                type = Decorations.Type.BUSH
        obj = Decorations(type, pos)
        Decorations.allDecorations.append(obj)

    @staticmethod
    def renderAll():
        for i in Decorations.allDecorations:
            if Camera.Camera.isOnScreen(i.rect):
                i.render()

    def render(self):
        screen.blit(self.image, Camera.Camera.relativePosition(self.rect.topleft))
