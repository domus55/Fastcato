import pygame
import time
from random import randrange

import Camera
from Obstacles.Obstacle import Obstacle
from Screen import screen


class Headgehog(Obstacle):
    IDLE_ANIMATION = []
    _animationWasSetUp = False

    def __init__(self, pos):
        super().__init__()
        if not Headgehog._animationWasSetUp:
            Headgehog._setUpAnimation()

        self.image = Headgehog.IDLE_ANIMATION[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50 + 12
        self.hitbox = pygame.Rect(self.rect)
        HITBOX_DOWNSIZE = 0.7
        self.hitbox.size = (HITBOX_DOWNSIZE * self.hitbox.size[0],  HITBOX_DOWNSIZE * self.hitbox.size[1])
        self.hitbox.center = self.rect.center
        self.hitbox.centery += 5
        self._lastAnimationFrame = 0
        self._animationDeltaTime = randrange(10) / 10      #used to make other headgehog move differently then this one
        self._animationBooster = randrange(80, 120) / 100  # used so each animation will be at a little different speed
        self._animationSpeed = 3 * self._animationBooster

    @staticmethod
    def _setUpAnimation():
        SIZE = 25
        NUMBER_OF_IMAGES = 4

        for i in range(NUMBER_OF_IMAGES):
            img = pygame.image.load(f"images/hedgehog/idle/{i+1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Headgehog.IDLE_ANIMATION.append(readyImg.convert_alpha())

        for i in range(len(Headgehog.IDLE_ANIMATION)):
            Headgehog.IDLE_ANIMATION.append(Headgehog.IDLE_ANIMATION[i])

        for i in range(len(Headgehog.IDLE_ANIMATION)):
            flippedImage = pygame.transform.flip(Headgehog.IDLE_ANIMATION[i], True, False)
            Headgehog.IDLE_ANIMATION.append(flippedImage)
        Headgehog._animationWasSetUp = True


    def update(self):
        self._animate()

    def _animate(self):
        currentTime = int((time.time() + self._animationDeltaTime) * self._animationSpeed)

        if currentTime % 4 != self._lastAnimationFrame:
            self._lastAnimationFrame = currentTime % len(Headgehog.IDLE_ANIMATION)
            self.image = Headgehog.IDLE_ANIMATION[self._lastAnimationFrame]
