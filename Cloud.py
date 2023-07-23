from random import randrange
import pygame

import Camera
from InnerTimer import InnerTime
from ProjectCommon import PATH
from Screen import screen


class Cloud:
    IMAGES = []
    _NUMBER_OF_IMAGES = 6
    _loadedImages = False

    def __init__(self, posX):
        super().__init__()
        if not Cloud._loadedImages:
            Cloud._loadImages()
            Cloud._loadedImages = True

        #it's used to tell how far from camera it is. The further it is the slower it will move and will be smaller
        #0.5 - 2
        self.distance = randrange(50, 150) / 100
        self._setImage()
        self.width = self.image.get_rect().size[0]
        self.posX = posX
        self.posY = randrange(-50, 150)
        if self.distance > 1:
            self.posY += randrange(50, 200)
        self.speed = randrange(-60, 60) / 1000 * self.distance

    @staticmethod
    def _loadImages():
        for i in range(Cloud._NUMBER_OF_IMAGES):
            img = pygame.image.load(f"{PATH}images/clouds/{i+1}.png")

            Cloud.IMAGES.append(img.convert_alpha())

    def update(self):
        self.posX += self.speed * InnerTime.deltaTime / 10
        if self.posX < -300 or self.posX > 16000:
            self.speed *= -1

    def render(self):
        screen.blit(self.image, (self.getXPosition(), self.posY))

    def getXPosition(self):
        return -Camera.Camera.posX / self.distance / 20 + self.posX

    def _setImage(self):
        scale = randrange(30, 50) / 10 / self.distance
        img = Cloud.IMAGES[randrange(Cloud._NUMBER_OF_IMAGES)]
        sizeX, sizeY = img.get_rect().size
        sizeX *= scale
        sizeY *= scale
        readyImg = pygame.transform.scale(img, (sizeX, sizeY))
        self.image = readyImg



