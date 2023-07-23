import time
import pygame

import Camera
import Credits
import LevelManager
from HUD import Deadline
from InnerTimer import InnerTime
from ProjectCommon import PATH
from Screen import screen


class CatSmall:
    ANIMATION_LAY_LEFT = []
    ANIMATION_WALK_LEFT = []
    ANIMATION_SIT_LEFT = []
    ANIMATION_SIT_TRANSITION = []

    _instance = None
    _animationWasSetUp = False

    def __init__(self):
        if not CatSmall._animationWasSetUp:
            CatSmall._setUpAnimation()
        self.image = CatSmall.ANIMATION_LAY_LEFT[0]
        self.pos = [0, 0]
        self.speed = 1.5
        self._velocityX = 0

        # Animation
        self._sittingPhase = 0  # 0 - standing, 1 - between standing and sitting, 2 - sitting
        self._sittingAnimationFrame = 0
        self._isFacingRight = True
        self._lastAnimationFrame = 0
        self._animationSpeed = 2.5

    @staticmethod
    def getInstance():
        if CatSmall._instance is None:
            CatSmall._instance = CatSmall()
        return CatSmall._instance

    @staticmethod
    def _setUpAnimation():
        SIZE = 100

        # laying
        for i in range(8):
            img = pygame.image.load(f"{PATH}images/catSmall/lay/{i + 1}.png")
            img = pygame.transform.scale(img, (SIZE, SIZE))
            flippedImage = pygame.transform.flip(img, True, False)
            CatSmall.ANIMATION_LAY_LEFT.append(flippedImage.convert_alpha())

        for i in range(len(CatSmall.ANIMATION_LAY_LEFT) - 2, 0, -1):
            CatSmall.ANIMATION_LAY_LEFT.append(CatSmall.ANIMATION_LAY_LEFT[i])

        # walking
        for i in range(4):
            img = pygame.image.load(f"{PATH}images/catSmall/walk/{i + 1}.png")
            img = pygame.transform.scale(img, (SIZE, SIZE))
            flippedImage = pygame.transform.flip(img, True, False)
            CatSmall.ANIMATION_WALK_LEFT.append(flippedImage.convert_alpha())

        # sit transition
        for i in range(4):
            img = pygame.image.load(f"{PATH}images/catSmall/sitTransition/{i + 1}.png")
            img = pygame.transform.scale(img, (SIZE, SIZE))
            flippedImage = pygame.transform.flip(img, True, False)
            CatSmall.ANIMATION_SIT_TRANSITION.append(flippedImage.convert_alpha())

        # sit
        for i in range(24):
            img = pygame.image.load(f"{PATH}images/catSmall/sit/{i + 1}.png")
            img = pygame.transform.scale(img, (SIZE, SIZE))
            flippedImage = pygame.transform.flip(img, True, False)
            CatSmall.ANIMATION_SIT_LEFT.append(flippedImage.convert_alpha())


    def restart(self, pos):
        self.pos = pos
        self._sittingPhase = 0
        self._sittingAnimationFrame = 0

    def update(self):
        if LevelManager.LevelManager.currentLevel == 7:
            self._isFacingRight = False
            self._move()
            self._animate()

    def render(self):
        if LevelManager.LevelManager.currentLevel == 7:
            screen.blit(self.image, Camera.Camera.relativePosition(self.pos))

    def _move(self):
        time = Deadline.Deadline.time()
        self._velocityX = 0

        if time > 17 and self.pos[0] > 900:
            self._velocityX = -self.speed

        self.pos[0] += self._velocityX * InnerTime.deltaTime / 10.0

    def _animate(self):
        if self._velocityX != 0:
            animation = CatSmall.ANIMATION_WALK_LEFT
            self._animationSpeed = 8
        elif self.pos[0] > 1000:
            animation = CatSmall.ANIMATION_LAY_LEFT
            self._animationSpeed = 2.5
        elif self._sittingPhase != 2:
            animation = CatSmall.ANIMATION_SIT_TRANSITION
            self._animationSpeed = 5
            if self._sittingPhase == 0:
                Credits.Credits.start()
                self._sittingPhase = 1
                self._sittingAnimationFrame = -1
        else:
            animation = CatSmall.ANIMATION_SIT_LEFT
            self._animationSpeed = 4

        currentTime = int(time.time() * self._animationSpeed)

        if currentTime % len(animation) != self._lastAnimationFrame:
            self._lastAnimationFrame = currentTime % len(animation)
            if self._sittingPhase != 1:
                self.image = animation[self._lastAnimationFrame]
            else:  # this lines make sure that sitting transition animation will start from 0 frame and and at the last one
                self._sittingAnimationFrame += 1
                if self._sittingAnimationFrame + 1 > len(animation):
                    self._sittingPhase = 2
                    self._sittingAnimationFrame = self._sittingAnimationFrame - 1
                self.image = animation[self._sittingAnimationFrame]


