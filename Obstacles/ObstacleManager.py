import pygame
from enum import Enum

import Camera
from Obstacles import Hedgehog
from Screen import *


class ObstacleType(Enum):
    HEADGEHOG = 1

class ObstacleManager:
    allObstacles = []

    @staticmethod
    def createObstacle(type, pos):
        if type == ObstacleType.HEADGEHOG:
            obj = Hedgehog.Headgehog(pos)
            ObstacleManager.allObstacles.append(obj)

    @staticmethod
    def updateAll():
        for i in ObstacleManager.allObstacles:
            i.update()

    @staticmethod
    def renderAll():
        for i in ObstacleManager.allObstacles:
            i.render()



