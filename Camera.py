import LevelManager

class Camera:
    posX = 0
    posY = -200

    @staticmethod
    def update(player):
        #TODO make camera movement smother
        Camera.posX, Camera.posY = player.rect.center
        Camera.posX -= 800
        Camera.posY -= 500
        pass

    @staticmethod
    def relativePosition(pos):
        return pos[0] - Camera.posX, pos[1] - Camera.posY
