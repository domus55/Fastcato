class ObstacleManager:
    allObstacles = []

    @staticmethod
    def addObstacle(obj):
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



