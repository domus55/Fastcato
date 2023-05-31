import pygame
import time
from random import randrange

import Camera
from InnerTimer import InnerTime
from Obstacles.Obstacle import Obstacle
from Screen import screen


class Dog(Obstacle):
    IDLE_ANIMATION_RIGHT = []
    IDLE_ANIMATION_LEFT = []

    WALK_ANIMATION_RIGHT = []
    WALK_ANIMATION_LEFT = []
    _animationWasSetUp = False

    def __init__(self, pos, walkDistance = 400):
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
        self.walkDistance = walkDistance
        self._isFacingRight = True if walkDistance > 0 else False
        self.startX = pos[0] * 50
        self.WALK_SPEED = 2.75
        self.idleStartTime = time.time()
        self.IDLE_TIME = 1 #in sec
        self.isIdle = True

        self._lastAnimationFrame = 0
        self._animationDeltaTime = randrange(10) / 10      # used to make other animals move differently then this one
        self._animationSpeed = 4

    @staticmethod
    def _setUpAnimation():
        SIZE = 90
        NUMBER_OF_IMAGES = 4

        #idle
        for i in range(NUMBER_OF_IMAGES):
            img = pygame.image.load(f"images/dog/idle/{i+1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Dog.IDLE_ANIMATION_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Dog.IDLE_ANIMATION_RIGHT)):
            flippedImage = pygame.transform.flip(Dog.IDLE_ANIMATION_RIGHT[i], True, False)
            Dog.IDLE_ANIMATION_LEFT.append(flippedImage)

        #walk
        for i in range(6):
            img = pygame.image.load(f"images/dog/walk/{i+1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Dog.WALK_ANIMATION_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Dog.WALK_ANIMATION_RIGHT)):
            flippedImage = pygame.transform.flip(Dog.WALK_ANIMATION_RIGHT[i], True, False)
            Dog.WALK_ANIMATION_LEFT.append(flippedImage)

        Dog._animationWasSetUp = True


    def update(self):
        self._animate()
        self._move()
        self.hitbox.center = self.rect.center

    def _move(self):
        if time.time() > self.idleStartTime + self.IDLE_TIME:
            self.isIdle = False
            distance = InnerTime.deltaTime * self.WALK_SPEED / 10
            if not self._isFacingRight:
                distance *= -1
            self.rect.centerx += distance

            if self._isFacingRight and self.startX + self.walkDistance <= self.rect.centerx:
                self._isFacingRight = False
                self.isIdle = True
                self.idleStartTime = time.time()
            if not self._isFacingRight and self.startX >= self.rect.centerx:
                self._isFacingRight = True
                self.isIdle = True
                self.idleStartTime = time.time()


    def _animate(self):
        currentTime = int((time.time() + self._animationDeltaTime) * self._animationSpeed)

        animation = None
        if self.isIdle:
            self._animationSpeed = 4
            if self._isFacingRight:
                animation = Dog.IDLE_ANIMATION_RIGHT
            else:
                animation = Dog.IDLE_ANIMATION_LEFT
        else:
            self._animationSpeed = 12
            if self._isFacingRight:
                animation = Dog.WALK_ANIMATION_RIGHT
            else:
                animation = Dog.WALK_ANIMATION_LEFT


        if currentTime % 4 != self._lastAnimationFrame:
            self._lastAnimationFrame = currentTime % len(animation)
            self.image = animation[self._lastAnimationFrame]
