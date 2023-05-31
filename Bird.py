import math
import time
from random import randrange

import pygame

import BirdCounter
import Camera
import Deadline
import GameInfo
import LevelManager
import Player
from InnerTimer import InnerTime
from Screen import screen


class Bird(pygame.sprite.Sprite):
    allBirds = []
    birdType = 0 #0 - raven, 1 - pigeon
    IMG_BIRD = pygame.image.load("images/bird2/idle/1.png").convert()
    DISAPPEARING_TIME = 2.5  # in sec

    PIGEON_FLY_ANIMATION_RIGHT = []
    PIGEON_FLY_ANIMATION_LEFT = []
    PIGEON_IDLE_ANIMATION = []

    CROW_FLY_ANIMATION_RIGHT = []
    CROW_FLY_ANIMATION_LEFT = []
    CROW_IDLE_ANIMATION = []
    _animationWasSetUp = False

    # Sounds
    SOUNDS_SCARE_RAVEN1 = pygame.mixer.Sound("sounds/scareBird/raven/1.wav")
    SOUNDS_SCARE_RAVEN2 = pygame.mixer.Sound("sounds/scareBird/raven/2.wav")

    SOUNDS_SCARE_PIGEON1 = pygame.mixer.Sound("sounds/scareBird/pigeon/1.wav")
    SOUNDS_SCARE_PIGEON2 = pygame.mixer.Sound("sounds/scareBird/pigeon/2.wav")

    def __init__(self, pos):
        super().__init__()
        if not Bird._animationWasSetUp:
            Bird._setUpAnimation()
        SIZE = 25
        self.birdType = pos[0] % 2

        if self.birdType is 0:
            self.animationFlyRight = Bird.CROW_FLY_ANIMATION_RIGHT
            self.animationFlyLeft = Bird.CROW_FLY_ANIMATION_LEFT
            self.animationIdle = Bird.CROW_IDLE_ANIMATION
        else:
            self.animationFlyRight = Bird.PIGEON_FLY_ANIMATION_RIGHT
            self.animationFlyLeft = Bird.PIGEON_FLY_ANIMATION_LEFT
            self.animationIdle = Bird.PIGEON_IDLE_ANIMATION

        self.image = self.animationIdle[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50 + 12
        self.posX = pos[0] * 50.0
        self.posY = pos[1] * 50.0 + 12

        self.alpha = 255
        self.disappeared = False #true after alpha is set to 0
        self._startFlying = None
        self.fliesRight = True
        self._lastAnimationFrame = 0
        self._animationDeltaTime = randrange(10) / 10  # used to make other bird move differently then this one
        self._animationBooster = randrange(80, 120) / 100  # used so each animation will be at a little different speed
        self._animationSpeed = 10 * self._animationBooster

    @staticmethod
    def create(pos):
        obj = Bird(pos)
        Bird.allBirds.append(obj)


    @staticmethod
    def updateAll():
        for i in Bird.allBirds:
            i._update()

    @staticmethod
    def renderAll():
        for i in Bird.allBirds:
            i._render()

    @staticmethod
    def birdsOnMap():
        onMap = 0
        for i in Bird.allBirds:
            if i.disappeared is False:
                onMap += 1

        return onMap

    @staticmethod
    def _setUpAnimation():
        SIZE = 40
        NUMBER_OF_IMAGES = 6

        # Pigeon
        for i in range(NUMBER_OF_IMAGES):
            img = pygame.image.load(f"images/bird2/fly/{i+1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Bird.PIGEON_FLY_ANIMATION_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Bird.PIGEON_FLY_ANIMATION_RIGHT)):
            flippedImage = pygame.transform.flip(Bird.PIGEON_FLY_ANIMATION_RIGHT[i], True, False)
            Bird.PIGEON_FLY_ANIMATION_LEFT.append(flippedImage)

        # Crow
        for i in range(NUMBER_OF_IMAGES):
            img = pygame.image.load(f"images/bird1/fly/{i+1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Bird.CROW_FLY_ANIMATION_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Bird.CROW_FLY_ANIMATION_RIGHT)):
            flippedImage = pygame.transform.flip(Bird.CROW_FLY_ANIMATION_RIGHT[i], True, False)
            Bird.CROW_FLY_ANIMATION_LEFT.append(flippedImage)

        SIZE = 25

        # Pigeon
        for i in range(4):
            img = pygame.image.load(f"images/bird2/idle/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Bird.PIGEON_IDLE_ANIMATION.append(readyImg.convert_alpha())

        for i in range(len(Bird.PIGEON_IDLE_ANIMATION)):
            Bird.PIGEON_IDLE_ANIMATION.append(Bird.PIGEON_IDLE_ANIMATION[i])

        for i in range(len(Bird.PIGEON_IDLE_ANIMATION)):
            flippedImage = pygame.transform.flip(Bird.PIGEON_IDLE_ANIMATION[i], True, False)
            Bird.PIGEON_IDLE_ANIMATION.append(flippedImage)

        # Crow
        for i in range(4):
            img = pygame.image.load(f"images/bird1/idle/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Bird.CROW_IDLE_ANIMATION.append(readyImg.convert_alpha())

        for i in range(len(Bird.CROW_IDLE_ANIMATION)):
            Bird.CROW_IDLE_ANIMATION.append(Bird.CROW_IDLE_ANIMATION[i])

        for i in range(len(Bird.CROW_IDLE_ANIMATION)):
            flippedImage = pygame.transform.flip(Bird.CROW_IDLE_ANIMATION[i], True, False)
            Bird.CROW_IDLE_ANIMATION.append(flippedImage)

        Bird._animationWasSetUp = True

    def _render(self):
        if self.disappeared is False:
            self.image.set_alpha(self.alpha)
            screen.blit(self.image, Camera.Camera.relativePosition(self.rect.topleft))

    def _update(self):
        if self.disappeared is False:
            self._checkScared()
            self._setAlpha()
            self._animate()
            if self._startFlying is not None:
                self._move()

    def _checkScared(self):
        playerCenter = Player.Player.getInstance().rect.center
        birdCenter = self.rect.center
        dist = math.hypot(playerCenter[0] - birdCenter[0], playerCenter[1] - birdCenter[1])
        if dist < 150 and self._startFlying is None:
            self._startFlying = time.time()
            if self.birdType is 0:
                randSound = randrange(2)
                if randSound is 0:
                    Bird.SOUNDS_SCARE_RAVEN1.play()
                else:
                    Bird.SOUNDS_SCARE_RAVEN2.play()
            else:
                randSound = randrange(2)
                if randSound is 0:
                    Bird.SOUNDS_SCARE_PIGEON1.play()
                else:
                    Bird.SOUNDS_SCARE_PIGEON2.play()



            if playerCenter[0] > birdCenter[0]:
                self.fliesRight = False
            else:
                self.fliesRight = True
            if self.birdType is 0:
                self.posY -= 12

    def _setAlpha(self):
        if self._startFlying is not None:
            self.alpha = 255 - (time.time() - self._startFlying) / Bird.DISAPPEARING_TIME * 255
            if self.alpha < 0:
                self.alpha = 0
                self.disappeared = True
                BirdCounter.BirdCounter.catchedBird()


    def _move(self):
        if self.birdType is 0:
            speedX = 1.35
            speedY = 0.5
        else:
            speedX = 1
            speedY = 1.25

        if not self.fliesRight:
            speedX *= -1

        self.posX += speedX * InnerTime.deltaTime / 10
        self.posY -= speedY * InnerTime.deltaTime / 10
        self.rect.center = (self.posX, self.posY)

    def _animate(self):
        if self._startFlying: #flying animation
            currentTime = int((time.time() + self._animationDeltaTime) * self._animationSpeed)

            if currentTime % 6 != self._lastAnimationFrame:
                if self.fliesRight is True:
                    self._lastAnimationFrame = currentTime % len(self.animationFlyRight)
                    self.image = self.animationFlyRight[self._lastAnimationFrame]
                else:
                    self._lastAnimationFrame = currentTime % len(self.animationFlyLeft)
                    self.image = self.animationFlyLeft[self._lastAnimationFrame]
        else: #idle animation
            currentTime = int((time.time() + self._animationDeltaTime) * self._animationSpeed / 2)

            if currentTime % 6 != self._lastAnimationFrame:
                self._lastAnimationFrame = currentTime % len(self.animationIdle)
                self.image = self.animationIdle[self._lastAnimationFrame]


