import LevelManager

class Camera:
    posX = 0
    posY = 0

    @staticmethod
    def update(player):
        #TODO make camera movement smother
        #Camera.posX, Camera.posY = player.getCenter()
        #Camera.posX -= 800
        #Camera.posY -= 450
        pass

    @staticmethod
    def relativePosition(pos):
        return pos[0] - Camera.posX, pos[1] - Camera.posY
