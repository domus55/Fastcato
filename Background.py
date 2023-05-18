import pygame
import time
from random import randrange

import Camera
from Screen import screen


class Background:
    _instance = None

    def __init__(self):
        super().__init__()
        self.layerArr = []
        self.imageWidth = []
        self._loadImages()
        self.image = self.layerArr[0]
        self.rect = self.image.get_rect()

    @staticmethod
    def getInstance():
        if Background._instance is None:
            Background._instance = Background()
        return Background._instance


    def _loadImages(self):
        NUMBER_OF_IMAGES = 3

        for i in range(NUMBER_OF_IMAGES):
            size = 900
            img = pygame.image.load(f"images/background/{i+1}.png")
            readyImg = pygame.transform.scale(img, (size * 1.777, size))
            self.layerArr.append(readyImg.convert_alpha())
            self.imageWidth.append(self.layerArr[i].get_rect().width)

    def render(self):
        for i in range(len(self.layerArr)):
            positionX = 0
            movingSpeed = 0
            if i is 1:
                movingSpeed = 0.02
            if i is 2:
                movingSpeed = 0.1
            positionX = ((-Camera.Camera.posX * movingSpeed) % self.imageWidth[i]) - self.imageWidth[i]
            screen.blit(self.layerArr[i], (positionX, 0))
            screen.blit(self.layerArr[i], (positionX + self.imageWidth[i], 0))


    def update(self):
        pass