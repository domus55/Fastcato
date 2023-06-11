import pygame

import Screen
from InnerTimer import InnerTime


class Camera:
    borderLeft = 50
    borderRight = 1000
    DELTA_X = 500
    SMOOTHNESS = 60

    posX = 0
    posY = 0


    @staticmethod
    def update(player):
        #TODO make camera movement smother
        destination, _ = player.pos
        cameraShift = 0

        if player._isFacingRight:
            cameraShift = (destination - Camera.DELTA_X - Camera.posX) / Camera.SMOOTHNESS
        else:
            cameraShift = (destination - 650 - Camera.posX) / Camera.SMOOTHNESS

        if abs(cameraShift) > 20:
            cameraShift = 0
            Camera.posX = destination - 800

        if abs(cameraShift) < 0.2:
            if abs(cameraShift) < 0.01:
                cameraShift = 0
            else:
                cameraShift = 0.2 if cameraShift > 0 else -0.2

        Camera.posX += cameraShift * InnerTime.deltaTime / 5

        if Camera.posX < Camera.borderLeft:
            Camera.posX = Camera.borderLeft

        if Camera.posX > Camera.borderRight - 1600:
            Camera.posX = Camera.borderRight - 1600

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
