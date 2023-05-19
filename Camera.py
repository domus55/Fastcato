import pygame

import Screen


class Camera:
    LEFT_WALL = 0

    posX = 0
    posY = 0

    @staticmethod
    def update(player):
        #TODO make camera movement smother
        Camera.posX, _ = player.rect.center
        Camera.posX -= 800
        if Camera.posX < Camera.LEFT_WALL:
            Camera.posX = Camera.LEFT_WALL

    @staticmethod
    def relativePosition(pos):
        return pos[0] - Camera.posX, pos[1] - Camera.posY

    @staticmethod
    def isOnScreen(rect):
        if Camera.posX + 1600 < rect.left - rect.size[0] / 2:
            return False
        if Camera.posX > rect.right + rect.size[0] / 2:
            return False
        return True
