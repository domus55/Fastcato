import math

import pygame

import Block
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
        self.speed = 3
        self.canJump = False

    def update(self, keyPressed):
        self._move(keyPressed)
        self._collision()

    def render(self):
        screen.blit(self.image, Camera.relativePosition(self.rect.topleft))

    def _move(self, keyPressed):
        self._velocityX = 0
        self._velocityY += 0.1 * Timer.deltaTime / 10

        if keyPressed[pygame.K_a]:
            self._velocityX -= self.speed
        if keyPressed[pygame.K_d]:
            self._velocityX += self.speed
        if keyPressed[pygame.K_w] and self.canJump:
            self._velocityY = - self.speed * 2.5
            self.canJump = False

        self.rect.centerx += self._velocityX * Timer.deltaTime / 10
        self.rect.centery += self._velocityY * Timer.deltaTime / 10

    def _collision(self):
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



