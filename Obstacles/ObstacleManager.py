from enum import Enum

from Obstacles import Hedgehog, Dog


class ObstacleType(Enum):
    HEADGEHOG = 1
    DOG = 2

class ObstacleManager:
    allObstacles = []

    @staticmethod
    def createObstacle(type, pos):
        obj = None
        if type is ObstacleType.HEADGEHOG:
            obj = Hedgehog.Headgehog(pos)
        if type is ObstacleType.DOG:
            obj = Dog.Dog(pos)

        if obj is not None:
            ObstacleManager.allObstacles.append(obj)

    @staticmethod
    def updateAll():
        for i in ObstacleManager.allObstacles:
            i.update()

    @staticmethod
    def renderAll():
        for i in ObstacleManager.allObstacles:
            i.render()



