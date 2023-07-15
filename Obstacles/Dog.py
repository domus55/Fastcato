import pygame
import time
from random import randrange

from HUD import Deadline
from InnerTimer import InnerTime
from Obstacles.Obstacle import Obstacle


class Dog(Obstacle):
    _ANIMATION_IDLE_RIGHT = []
    _ANIMATION_IDLE_LEFT = []

    _ANIMATION_WALK_RIGHT = []
    _ANIMATION_WALK_LEFT = []
    _animationWasSetUp = False

    def __init__(self, pos, walkDistance = 400):
        super().__init__()
        if not Dog._animationWasSetUp:
            Dog._setUpAnimation()

        self.image = Dog._ANIMATION_IDLE_RIGHT[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50 - 20
        self.hitbox = pygame.Rect(0, 0, 68, 31)
        self.hitbox.center = self.rect.center
        self.hitboxOffset = (-10, 25)
        self.hitbox.centerx += self.hitboxOffset[0]
        self.hitbox.centery += self.hitboxOffset[1]
        self._isFacingRight = True if walkDistance > 0 else False
        if not self._isFacingRight:
            self.startX = pos[0] * 50 + walkDistance
            self.walkDistance = walkDistance * -1
        else:
            self.startX = pos[0] * 50
            self.walkDistance = walkDistance
        self.WALK_SPEED = 4
        self.idleStartTime = time.time()
        self.IDLE_TIME = 1 #in sec
        self.isIdle = True

        self._lastAnimationFrame = 0
        self._animationDeltaTime = randrange(10) / 10      # used to make other animals move differently then this one
        self._animationSpeed = 4

    @staticmethod
    def _setUpAnimation():
        SIZE = 90

        #idle
        for i in range(4):
            img = pygame.image.load(f"images/dog/idle/{i+1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Dog._ANIMATION_IDLE_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Dog._ANIMATION_IDLE_RIGHT)):
            flippedImage = pygame.transform.flip(Dog._ANIMATION_IDLE_RIGHT[i], True, False)
            Dog._ANIMATION_IDLE_LEFT.append(flippedImage)

        #walk
        for i in range(6):
            img = pygame.image.load(f"images/dog/walk/{i+1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Dog._ANIMATION_WALK_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Dog._ANIMATION_WALK_RIGHT)):
            flippedImage = pygame.transform.flip(Dog._ANIMATION_WALK_RIGHT[i], True, False)
            Dog._ANIMATION_WALK_LEFT.append(flippedImage)

        Dog._animationWasSetUp = True


    def update(self):
        self._animate()
        self._move()
        self.hitbox.center = self.rect.center
        self.hitbox.centerx += self.hitboxOffset[0]
        self.hitbox.centery += self.hitboxOffset[1]

    def _move(self):
        if Deadline.Deadline.isRunning is False:
            self.idleStartTime = time.time()

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
                animation = Dog._ANIMATION_IDLE_RIGHT
            else:
                animation = Dog._ANIMATION_IDLE_LEFT
        else:
            self._animationSpeed = 14
            if self._isFacingRight:
                animation = Dog._ANIMATION_WALK_RIGHT
            else:
                animation = Dog._ANIMATION_WALK_LEFT


        if currentTime % 4 != self._lastAnimationFrame:
            self._lastAnimationFrame = currentTime % len(animation)
            self.image = animation[self._lastAnimationFrame]
