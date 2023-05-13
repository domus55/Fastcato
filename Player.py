import math

import pygame
from Screen import *
from InnerTimer import *
from Camera import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        tempImage = pygame.image.load("images/cat.png")
        self.width = 80
        self.height = 100
        self.image = pygame.transform.scale(tempImage, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = 100, 100
        self._velocityX = 0
        self._velocityY = 0
        self.speed = 10

    def update(self, keyPressed):
        self._velocityX = 0
        self._velocityY = 0

        if keyPressed[pygame.K_a]:
            self._velocityX -= self.speed
        if keyPressed[pygame.K_d]:
            self._velocityX += self.speed
        if keyPressed[pygame.K_w]:
            self._velocityY -= self.speed
        if keyPressed[pygame.K_s]:
            self._velocityY += self.speed

        self.rect.centerx += self._velocityX * Timer.deltaTime / 10
        self.rect.centery += self._velocityY * Timer.deltaTime / 10

    def render(self):
        screen.blit(self.image, (self.rect.centerx - Camera.posX, self.rect.centery - Camera.posY))

    def getCenter(self):
        centerX, centerY = self.rect.center
        centerX += self.width / 2
        centerY += self.height / 2
        return (centerX, centerY)

