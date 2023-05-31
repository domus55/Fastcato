

from Obstacles import Hedgehog, Dog


class ObstacleManager:
    allObstacles = []

    @staticmethod
    def addObstackle(obj):
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



