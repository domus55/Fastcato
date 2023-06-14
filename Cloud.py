from random import randrange
import pygame

import Camera
from InnerTimer import InnerTime
from Screen import screen


class Cloud():
    IMGAGES = []
    NUMBER_OF_IMAGES = 6
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

        #print(f"Distance {self.distance}\tSpeed {self.speed}\tSize {self.image.get_rect().size}")

    @staticmethod
    def _loadImages():
        for i in range(Cloud.NUMBER_OF_IMAGES):
            img = pygame.image.load(f"images/clouds/{i+1}.png")

            Cloud.IMGAGES.append(img.convert_alpha())

    def update(self):
        self.posX += self.speed * InnerTime.deltaTime / 10
        if self.posX < -300 or self.posX > 16000:
            self.speed *= -1

    def render(self):
        screen.blit(self.image, (self.getXPosision(), self.posY))

    def getXPosision(self):
        return -Camera.Camera.posX / self.distance / 20 + self.posX

    def _setImage(self):
        scale = randrange(30, 50) / 10 / self.distance
        img = Cloud.IMGAGES[randrange(Cloud.NUMBER_OF_IMAGES)]
        sizeX, sizeY = img.get_rect().size
        sizeX *= scale
        sizeY *= scale
        readyImg = pygame.transform.scale(img, (sizeX, sizeY))
        self.image = readyImg



