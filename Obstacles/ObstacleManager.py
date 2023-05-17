from enum import Enum

from Obstacles import Hedgehog


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



