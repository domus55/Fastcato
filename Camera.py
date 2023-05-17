class Camera:
    LEFT_WALL = 0

    posX = 0
    posY = 0

    @staticmethod
    def update(player):
        #TODO make camera movement smother
        Camera.posX, _ = player.rect.center
        Camera.posX -= 800
        if Camera.posX < Camera.LEFT_WALL:
            Camera.posX = Camera.LEFT_WALL
        pass

    @staticmethod
    def relativePosition(pos):
        return pos[0] - Camera.posX, pos[1] - Camera.posY
