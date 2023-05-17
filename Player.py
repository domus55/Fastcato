import Block
import LevelManager
from Obstacles import ObstacleManager
from Screen import *
from InnerTimer import *
import Camera


class Player(pygame.sprite.Sprite):
    instance = None

    def __init__(self):
        super().__init__()
        tempImage = pygame.image.load("images/cat.png").convert()
        self.width = 80
        self.height = 100
        self.image = pygame.transform.scale(tempImage, (self.width, self.height))
        self.rect = self.image.get_rect()
        self._velocityX = 0
        self._velocityY = 0
        self.speed = 3
        self.canJump = False
        self.startingPosition = (100, 100)
        self.restart()


    def update(self, keyPressed):
        self._move(keyPressed)
        self._isOutOfMap()
        self._collisionWithBlock()
        self._collisionWithObstacle()

    def render(self):
        screen.blit(self.image, Camera.Camera.relativePosition(self.rect.topleft))

    def restart(self):
        self.rect.center = self.startingPosition


    def _move(self, keyPressed):
        self._velocityX = 0
        self._velocityY += 0.2 * Timer.deltaTime / 10

        if keyPressed[pygame.K_a]:
            self._velocityX -= self.speed
        if keyPressed[pygame.K_d]:
            self._velocityX += self.speed
        if keyPressed[pygame.K_w] and self.canJump:
            self._velocityY = - self.speed * 3
            self.canJump = False

        self.rect.centerx += self._velocityX * Timer.deltaTime / 10
        self.rect.centery += self._velocityY * Timer.deltaTime / 10


    def _isOutOfMap(self):
        #Stop on the left wall
        if self.rect.centerx < Camera.Camera.LEFT_WALL:
            self.rect.centerx = Camera.Camera.LEFT_WALL

        #Fell out of the map
        if self.rect.centery > 1000:
            LevelManager.LevelManager.restartLevel()

    def _collisionWithBlock(self):
        self.canJump = False

        for i in Block.Block.allBlocks:
            if self.rect.colliderect(i.rect):
                halfBlockSize = i.rect.size[0] / 2, i.rect.size[1] / 2

                deltaX = i.rect.centerx - (self.rect.centerx )
                deltaY = i.rect.centery - (self.rect.centery )
                intersectX = abs(deltaX) - (halfBlockSize[0] + self.rect.size[0] / 2)
                intersectY = abs(deltaY) - (halfBlockSize[1] + self.rect.size[1] / 2)

                changePositionX = 0
                changePositionY = 0

                if intersectX < 0 and intersectY < 0:
                    if intersectX > intersectY:
                        if deltaX > 0:
                            changePositionX = intersectX
                            changePositionY = 0
                        else:
                            changePositionX = -intersectX
                            changePositionY = 0
                    else:
                        if deltaY > 0:
                            changePositionX = 0
                            changePositionY = intersectY
                        else:
                            changePositionX = 0
                            changePositionY = -intersectY

                self.rect.centerx += changePositionX
                self.rect.centery += changePositionY

                if(changePositionY < 0):
                    self.canJump = True
                    self._velocityY = 0


                if (changePositionY > 0):
                    self._velocityY = 0

    def _collisionWithObstacle(self):
        for i in ObstacleManager.ObstacleManager.allObstacles:
            if self.rect.colliderect(i.hitbox):
                LevelManager.LevelManager.restartLevel()





