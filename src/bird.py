import math
import time
from enum import Enum
from random import randrange

import pygame

from src import game_info, player
from src.camera import Camera
from src.hud import bird_counter
from src.inner_timer import InnerTime
from src.project_common import PATH
from src.screen import screen


class BirdType(Enum):
    CROW = 0
    PIGEON = 1


class Bird(pygame.sprite.Sprite):
    all_birds = []
    _DISAPPEARING_TIME = 2.5  # in sec

    _ANIMATION_PIGEON_FLY_RIGHT = []
    _ANIMATION_PIGEON_FLY_LEFT = []
    _ANIMATION_PIGEON_IDLE = []

    _ANIMATION_CROW_FLY_RIGHT = []
    _ANIMATION_CROW_FLY_LEFT = []
    _ANIMATION_CROW_IDLE = []
    _animation_was_set_up = False

    _ICON = pygame.transform.scale(pygame.image.load(f"{PATH}images/gui/icons/attention.png"), (40, 40)).convert_alpha()

    # Sounds
    SOUNDS_SCARE_CROW1 = pygame.mixer.Sound(f"{PATH}sounds/scareBird/crow/1.wav")
    SOUNDS_SCARE_CROW2 = pygame.mixer.Sound(f"{PATH}sounds/scareBird/crow/2.wav")

    SOUNDS_SCARE_PIGEON1 = pygame.mixer.Sound(f"{PATH}sounds/scareBird/pigeon/1.wav")
    SOUNDS_SCARE_PIGEON2 = pygame.mixer.Sound(f"{PATH}sounds/scareBird/pigeon/2.wav")

    def __init__(self, pos, has_icon):
        super().__init__()
        if not Bird._animation_was_set_up:
            Bird._setUpAnimation()

        self.birdType = BirdType(int(pos[0]) % 2)  # 0 = crow, 1 = pigeon
        if self.birdType == BirdType.CROW:
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
        self._hasIcon = has_icon
        self._alpha = 255
        self.disappeared = False  # true after _alpha is set to 0
        self._startFlying = None
        self._fliesRight = True
        self._lastAnimationFrame = 0
        self._animationDeltaTime = randrange(10) / 10  # used to make other bird move differently then this one
        self._animationBooster = randrange(80, 120) / 100  # used so each animation will be at a little different speed
        self._animationSpeed = 10 * self._animationBooster

    @staticmethod
    def create(pos, has_icon=False):
        obj = Bird(pos, has_icon)
        Bird.all_birds.append(obj)
        Bird.SOUNDS_SCARE_CROW1.set_volume(game_info.GameInfo.getSound())
        Bird.SOUNDS_SCARE_CROW2.set_volume(game_info.GameInfo.getSound())
        Bird.SOUNDS_SCARE_PIGEON1.set_volume(game_info.GameInfo.getSound())
        Bird.SOUNDS_SCARE_PIGEON2.set_volume(game_info.GameInfo.getSound())

    @staticmethod
    def updateAll():
        for i in Bird.all_birds:
            i._update()

    @staticmethod
    def renderAll():
        for i in Bird.all_birds:
            i._render()

    @staticmethod
    def birdsOnMap():
        onMap = 0
        for i in Bird.all_birds:
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

        Bird._animation_was_set_up = True

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
        player_center = player.Player.getInstance().collider.center
        bird_center = self.rect.center
        dist = math.hypot(player_center[0] - bird_center[0], player_center[1] - bird_center[1])
        if dist < 150 and self._startFlying is None:
            self._startFlying = time.time()
            if self.birdType == BirdType.CROW:
                rand_sound = randrange(2)
                if rand_sound == 0:
                    Bird.SOUNDS_SCARE_CROW1.play()
                else:
                    Bird.SOUNDS_SCARE_CROW2.play()
            else:
                rand_sound = randrange(2)
                if rand_sound == 0:
                    Bird.SOUNDS_SCARE_PIGEON1.play()
                else:
                    Bird.SOUNDS_SCARE_PIGEON2.play()

            if player_center[0] > bird_center[0]:
                self.__fliesRight = False
            else:
                self.__fliesRight = True
            if self.birdType == BirdType.CROW:
                self.posY -= 12
            bird_counter.BirdCounter.caught_bird()

    def _set_alpha(self):
        if self._startFlying is not None and not self.disappeared:
            self._alpha = 255 - (time.time() - self._startFlying) / Bird._DISAPPEARING_TIME * 255
            if self._alpha < 0:
                self._alpha = 0
                self.disappeared = True

    def _move(self):
        if self.birdType == BirdType.CROW:
            speed_x = 1.35
            speed_y = 0.5
        else:
            speed_x = 1
            speed_y = 1.25

        if not self.__fliesRight:
            speed_x *= -1

        self.posX += speed_x * InnerTime.deltaTime / 10
        self.posY -= speed_y * InnerTime.deltaTime / 10
        self.rect.center = (self.posX, self.posY)

    def _animate(self):
        if self._startFlying:  # flying animation
            current_time = int((time.time() + self._animationDeltaTime) * self._animationSpeed)

            if current_time % 6 != self._lastAnimationFrame:
                if self.__fliesRight is True:
                    self._lastAnimationFrame = current_time % len(self.animationFlyRight)
                    self.image = self.animationFlyRight[self._lastAnimationFrame]
                else:
                    self._lastAnimationFrame = current_time % len(self.animationFlyLeft)
                    self.image = self.animationFlyLeft[self._lastAnimationFrame]
        else:  # idle animation
            current_time = int((time.time() + self._animationDeltaTime) * self._animationSpeed / 2)

            if current_time % 6 != self._lastAnimationFrame:
                self._lastAnimationFrame = current_time % len(self.animationIdle)
                self.image = self.animationIdle[self._lastAnimationFrame]
