import LevelManager

class Camera:
    posX = 0
    posY = 0

    @staticmethod
    def update(player):
        #TODO make camer movement smother
        Camera.posX, Camera.posY = player.getCenter()
        Camera.posX -= 800
        Camera.posY -= 450
