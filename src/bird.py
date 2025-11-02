import math
import time
from random import randrange
import pygame

from src.hud import bird_counter
from src.camera import Camera
from src import game_info
from src import player
from src.inner_timer import InnerTime
from src.project_common import \
    PATH
from src.screen import screen


class Bird(pygame.sprite.Sprite):
    allBirds = []
    _DISAPPEARING_TIME = 2.5  # in sec

    _ANIMATION_PIGEON_FLY_RIGHT = []
    _ANIMATION_PIGEON_FLY_LEFT = []
    _ANIMATION_PIGEON_IDLE = []

    _ANIMATION_CROW_FLY_RIGHT = []
    _ANIMATION_CROW_FLY_LEFT = []
    _ANIMATION_CROW_IDLE = []
    _animationWasSetUp = False

    _ICON = pygame.transform.scale(pygame.image.load(f"{PATH}images/gui/icons/attention.png"), (40, 40)).convert_alpha()

    # Sounds
    SOUNDS_SCARE_RAVEN1 = pygame.mixer.Sound(f"{PATH}sounds/scareBird/raven/1.wav")
    SOUNDS_SCARE_RAVEN2 = pygame.mixer.Sound(f"{PATH}sounds/scareBird/raven/2.wav")

    SOUNDS_SCARE_PIGEON1 = pygame.mixer.Sound(f"{PATH}sounds/scareBird/pigeon/1.wav")
    SOUNDS_SCARE_PIGEON2 = pygame.mixer.Sound(f"{PATH}sounds/scareBird/pigeon/2.wav")

    def __init__(self, pos, hasIcon):
        super().__init__()
        if not Bird._animationWasSetUp:
            Bird._setUpAnimation()

        self.birdType = int(pos[0]) % 2  # 0 = raven, 1 = pigeon
        if self.birdType == 0:
            self.animationFlyRight = Bird._ANIMATION_CROW_FLY_RIGHT
            self.animationFlyLeft = Bird._ANIMATION_CROW_FLY_LEFT
            self.animationIdle = Bird._ANIMATION_CROW_IDLE
        else:
            self.animationFlyRight = Bird._ANIMATION_PIGEON_FLY_RIGHT
            self.animationFlyLeft = Bird._ANIMATION_PIGEON_FLY_LEFT
            self.animationIdle = Bird._ANIMATION_PIGEON_IDLE

        self.image = self.animationIdle[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50 + 12
        self.posX = pos[0] * 50.0
        self.posY = pos[1] * 50.0 + 12
        self._hasIcon = hasIcon
        self._alpha = 255
        self.disappeared = False  # true after _alpha is set to 0
        self._startFlying = None
        self._fliesRight = True
        self._lastAnimationFrame = 0
        self._animationDeltaTime = randrange(10) / 10  # used to make other bird move differently then this one
        self._animationBooster = randrange(80, 120) / 100  # used so each animation will be at a little different speed
        self._animationSpeed = 10 * self._animationBooster

    @staticmethod
    def create(pos, hasIcon = False):
        obj = Bird(pos, hasIcon)
        Bird.allBirds.append(obj)
        Bird.SOUNDS_SCARE_RAVEN1.set_volume(game_info.GameInfo.getSound())
        Bird.SOUNDS_SCARE_RAVEN2.set_volume(game_info.GameInfo.getSound())
        Bird.SOUNDS_SCARE_PIGEON1.set_volume(game_info.GameInfo.getSound())
        Bird.SOUNDS_SCARE_PIGEON2.set_volume(game_info.GameInfo.getSound())

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
            img = pygame.image.load(f"{PATH}images/bird2/fly/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Bird._ANIMATION_PIGEON_FLY_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Bird._ANIMATION_PIGEON_FLY_RIGHT)):
            flippedImage = pygame.transform.flip(Bird._ANIMATION_PIGEON_FLY_RIGHT[i], True, False)
            Bird._ANIMATION_PIGEON_FLY_LEFT.append(flippedImage)

        # Crow
        for i in range(NUMBER_OF_IMAGES):
            img = pygame.image.load(f"{PATH}images/bird1/fly/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Bird._ANIMATION_CROW_FLY_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Bird._ANIMATION_CROW_FLY_RIGHT)):
            flippedImage = pygame.transform.flip(Bird._ANIMATION_CROW_FLY_RIGHT[i], True, False)
            Bird._ANIMATION_CROW_FLY_LEFT.append(flippedImage)

        SIZE = 25

        # Pigeon
        for i in range(4):
            img = pygame.image.load(f"{PATH}images/bird2/idle/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Bird._ANIMATION_PIGEON_IDLE.append(readyImg.convert_alpha())

        for i in range(len(Bird._ANIMATION_PIGEON_IDLE)):
            Bird._ANIMATION_PIGEON_IDLE.append(Bird._ANIMATION_PIGEON_IDLE[i])

        for i in range(len(Bird._ANIMATION_PIGEON_IDLE)):
            flippedImage = pygame.transform.flip(Bird._ANIMATION_PIGEON_IDLE[i], True, False)
            Bird._ANIMATION_PIGEON_IDLE.append(flippedImage)

        # Crow
        for i in range(4):
            img = pygame.image.load(f"{PATH}images/bird1/idle/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (SIZE * 1.4, SIZE))
            Bird._ANIMATION_CROW_IDLE.append(readyImg.convert_alpha())

        for i in range(len(Bird._ANIMATION_CROW_IDLE)):
            Bird._ANIMATION_CROW_IDLE.append(Bird._ANIMATION_CROW_IDLE[i])

        for i in range(len(Bird._ANIMATION_CROW_IDLE)):
            flippedImage = pygame.transform.flip(Bird._ANIMATION_CROW_IDLE[i], True, False)
            Bird._ANIMATION_CROW_IDLE.append(flippedImage)

        Bird._animationWasSetUp = True

    def _render(self):
        if self.disappeared is False and Camera.isOnScreen(self.rect):
            self.image.set_alpha(self._alpha)
            screen.blit(self.image, Camera.relativePosition(self.rect.topleft))

            if self._hasIcon and self._alpha >= 45:
                Bird._ICON.set_alpha(self._alpha - 45)
                iconPosX, iconPosY = self.rect.topleft
                iconPosY -= 50
                screen.blit(Bird._ICON, Camera.relativePosition((iconPosX, iconPosY)))

    def _update(self):
        if self.disappeared is False:
            self._checkScared()
            self._set_alpha()
            self._animate()
            if self._startFlying is not None:
                self._move()

    def _checkScared(self):
        playerCenter = player.Player.getInstance().collider.center
        birdCenter = self.rect.center
        dist = math.hypot(playerCenter[0] - birdCenter[0], playerCenter[1] - birdCenter[1])
        if dist < 150 and self._startFlying is None:
            self._startFlying = time.time()
            if self.birdType == 0:
                randSound = randrange(2)
                if randSound == 0:
                    Bird.SOUNDS_SCARE_RAVEN1.play()
                else:
                    Bird.SOUNDS_SCARE_RAVEN2.play()
            else:
                randSound = randrange(2)
                if randSound == 0:
                    Bird.SOUNDS_SCARE_PIGEON1.play()
                else:
                    Bird.SOUNDS_SCARE_PIGEON2.play()

            if playerCenter[0] > birdCenter[0]:
                self.__fliesRight = False
            else:
                self.__fliesRight = True
            if self.birdType == 0:
                self.posY -= 12

    def _set_alpha(self):
        if self._startFlying is not None:
            self._alpha = 255 - (time.time() - self._startFlying) / Bird._DISAPPEARING_TIME * 255
            if self._alpha < 0:
                self._alpha = 0
                self.disappeared = True
                bird_counter.BirdCounter.catchedBird()

    def _move(self):
        if self.birdType == 0:
            speedX = 1.35
            speedY = 0.5
        else:
            speedX = 1
            speedY = 1.25

        if not self.__fliesRight:
            speedX *= -1

        self.posX += speedX * InnerTime.deltaTime / 10
        self.posY -= speedY * InnerTime.deltaTime / 10
        self.rect.center = (self.posX, self.posY)

    def _animate(self):
        if self._startFlying:  # flying animation
            currentTime = int((time.time() + self._animationDeltaTime) * self._animationSpeed)

            if currentTime % 6 != self._lastAnimationFrame:
                if self.__fliesRight is True:
                    self._lastAnimationFrame = currentTime % len(self.animationFlyRight)
                    self.image = self.animationFlyRight[self._lastAnimationFrame]
                else:
                    self._lastAnimationFrame = currentTime % len(self.animationFlyLeft)
                    self.image = self.animationFlyLeft[self._lastAnimationFrame]
        else:  # idle animation
            currentTime = int((time.time() + self._animationDeltaTime) * self._animationSpeed / 2)

            if currentTime % 6 != self._lastAnimationFrame:
                self._lastAnimationFrame = currentTime % len(self.animationIdle)
                self.image = self.animationIdle[self._lastAnimationFrame]
