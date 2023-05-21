import pygame
import time
from random import randrange

import Camera
from Obstacles.Obstacle import Obstacle
from Screen import screen


class Dog(Obstacle):
    IDLE_ANIMATION_RIGHT = []
    IDLE_ANIMATION_LEFT = []
    _animationWasSetUp = False

    def __init__(self, pos):
        super().__init__()
        if not Dog._animationWasSetUp:
            Dog._setUpAnimation()

        self.image = Dog.IDLE_ANIMATION_RIGHT[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50 - 20
        self.hitbox = self.rect.scale_by(0.55, 0.35)
        self.hitbox.center = self.rect.center
        self.hitboxOffset = (-10, 25)
        self.hitbox.centerx += self.hitboxOffset[0]
        self.hitbox.centery += self.hitboxOffset[1]
        self._lastAnimationFrame = 0
        self._animationDeltaTime = randrange(10) / 10      # used to make other animals move differently then this one
        self._animationBooster = randrange(80, 120) / 100  # used so each animation will be at a little different speed
        self._animationSpeed = 3 * self._animationBooster

    @staticmethod
    def _setUpAnimation():
        SIZE = 90
        NUMBER_OF_IMAGES = 4

        for i in range(NUMBER_OF_IMAGES):
            img = pygame.image.load(f"images/dog/idle/{i+1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Dog.IDLE_ANIMATION_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Dog.IDLE_ANIMATION_RIGHT)):
            flippedImage = pygame.transform.flip(Dog.IDLE_ANIMATION_RIGHT[i], True, False)
            Dog.IDLE_ANIMATION_LEFT.append(flippedImage)
        Dog._animationWasSetUp = True


    def update(self):
        self._animate()

    def _animate(self):
        currentTime = int((time.time() + self._animationDeltaTime) * self._animationSpeed)

        if currentTime % 4 != self._lastAnimationFrame:
            self._lastAnimationFrame = currentTime % len(Dog.IDLE_ANIMATION_RIGHT)
            self.image = Dog.IDLE_ANIMATION_RIGHT[self._lastAnimationFrame]
