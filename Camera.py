import pygame

import Screen


class Camera:
    LEFT_WALL = 0
    DELTA_X = 500
    SMOOTHNESS = 60

    posX = 0
    posY = 0


    @staticmethod
    def update(player):
        #TODO make camera movement smother
        destination, _ = player.rect.center
        cameraShift = 0

        if player._isFacingRight:
            cameraShift = (destination - Camera.DELTA_X - Camera.posX) / Camera.SMOOTHNESS
        else:
            cameraShift = (destination - 800 - Camera.posX) / Camera.SMOOTHNESS

        if abs(cameraShift) < 0.2:
            if abs(cameraShift) < 0.01:
                cameraShift = 0
            else:
                cameraShift = 0.2 if cameraShift > 0 else -0.2

        Camera.posX += cameraShift

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
