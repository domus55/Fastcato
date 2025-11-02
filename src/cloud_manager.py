from random import randrange

from src.cloud import Cloud


class CloudManager:
    _allClouds = []
    _numberOfClouds = 5

    @staticmethod
    def initialize():
        CloudManager._allClouds.clear()
        CloudManager._numberOfClouds = 5 + randrange(100)

        for i in range(CloudManager._numberOfClouds):
            obj = Cloud(randrange(0, 16000))
            CloudManager._allClouds.append(obj)

    @staticmethod
    def update():
        for i in CloudManager._allClouds:
            i.update()

    @staticmethod
    def renderBeforeMountains():
        for i in CloudManager._allClouds:
            if i.distance > 1:
                if CloudManager.isOnScreen(i):
                    i.render()

    @staticmethod
    def renderAfterMountains():
        for i in CloudManager._allClouds:
            if i.distance <= 1:
                if CloudManager.isOnScreen(i):
                    i.render()

    @staticmethod
    def isOnScreen(cloud):
        if 0 > cloud.getXPosition() + cloud.width:
            return False
        if 1600 < cloud.getXPosition() - cloud.width:
            return False
        return True

