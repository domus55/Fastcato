import time
from random import randrange

import pygame.mixer

import Block
import Deadline
import GameInfo
import InGameMenu
import LevelManager
import Camera
import MainMenu
from Obstacles import ObstacleManager
from Screen import *
from InnerTimer import *
from threading import Timer


class Player(pygame.sprite.Sprite):
    _instance = None

    ANIMATION_WALK_RIGHT = []
    ANIMATION_WALK_LEFT = []

    SHADOW_AMOUNT = 4
    IMG_SHADOW_RIGHT = None
    IMG_SHADOW_LEFT = None

    IMG_JUMP_UP_RIGHT = None
    IMG_JUMP_UP_LEFT = None
    IMG_FLYING_RIGHT = None
    IMG_FLYING_LEFT = None
    IMG_FALL_DOWN_RIGHT = None
    IMG_FALL_DOWN_LEFT = None

    ALL_IDLE_ANIMATIONS_RIGHT = []
    ALL_IDLE_ANIMATIONS_LEFT = []

    #sounds
    DASH_SOUND = pygame.mixer.Sound("sounds/dash.wav")
    DASH_READY = pygame.mixer.Sound("sounds/dashReady.wav")

    _animationWasSetUp = False

    def __init__(self):
        super().__init__()
        if not Player._animationWasSetUp:
            Player._setUpAnimation()
        self._prevAnimationFrame = 0
        self.image = Player.ANIMATION_WALK_RIGHT[0]
        self.rect = self.image.get_rect()

        #Movement
        self.collider = self.rect.scale_by(0.5, 0.35)
        self._velocityX = 0
        self._velocityY = 0
        self.speed = 3
        self.canJump = False
        self.startingPosition = (100, 500)

        #Dash
        self._DASH_DELAY = 3 #in seconds
        self._DASH_DISTANCE = 150
        self._DASH_ANIMATION_TIME = 1  # in seconds
        self.last_dash_time = time.time() - self._DASH_DELAY
        self.shadowImagesPos = [pygame.Rect(0, 0, 0, 0)] * Player.SHADOW_AMOUNT
        self._shadowFacingRight = True

        #Animation
        self._prevVelocityX = 0 #it's used for animations
        self._prevVelocityY = 0 #it's used for animations
        self._isFacingRight = True
        self.currentIdleAnimation = None
        self._selectRandomIdleAnimation()

        self.restart()

    @staticmethod
    def getInstance():
        if Player._instance is None:
            Player._instance = Player()
        return Player._instance

    def update(self, keyPressed):
        self._move(keyPressed)
        self._dash(keyPressed)
        self._isOutOfMap()
        self._collisionWithBlock()
        self._collisionWithObstacle()
        self._animate()

    def render(self):
        self.rect.bottomleft = self.collider.bottomleft
        self.rect.centerx -= 28
        screen.blit(self.image, Camera.Camera.relativePosition(self.rect.topleft))

        if time.time() < self.last_dash_time + self._DASH_ANIMATION_TIME:
            for i in range(Player.SHADOW_AMOUNT):
                alpha = self._returnShadowAlpha(i)
                if self._shadowFacingRight:
                    Player.IMG_SHADOW_RIGHT.set_alpha(alpha)
                    screen.blit(Player.IMG_SHADOW_RIGHT, Camera.Camera.relativePosition(self.shadowImagesPos[i].topleft))
                else:
                    Player.IMG_SHADOW_LEFT.set_alpha(alpha)
                    screen.blit(Player.IMG_SHADOW_LEFT, Camera.Camera.relativePosition(self.shadowImagesPos[i].topleft))
        #pygame.draw.rect(screen, (255, 0, 0), self.collider)

    def restart(self):
        self.collider.center = self.startingPosition
        self._velocityY = 0
        self.last_dash_time = time.time() - self._DASH_DELAY
        Player.DASH_SOUND.set_volume(GameInfo.GameInfo.getSound())
        Player.DASH_READY.set_volume(GameInfo.GameInfo.getSound())
        Deadline.Deadline.stop()

    def _move(self, keyPressed):
        self._prevVelocityX = self._velocityX #it's used for animations
        self._prevVelocityY = self._velocityY #it's used for animations
        self._velocityX = 0
        self._velocityY += 0.2 * InnerTime.deltaTime / 10

        if keyPressed[pygame.K_a]:
            self._velocityX -= self.speed
            self._isFacingRight = False
        if keyPressed[pygame.K_d]:
            self._velocityX += self.speed
            self._isFacingRight = True
        if keyPressed[pygame.K_w] and self.canJump:
            self._velocityY = - self.speed * 3
            self.canJump = False

        self.collider.centerx += self._velocityX * InnerTime.deltaTime / 10
        self.collider.centery += self._velocityY * InnerTime.deltaTime / 10

    def _dash(self, keyPressed):
        if keyPressed[pygame.K_LSHIFT] and time.time() > self.last_dash_time + self._DASH_DELAY:
            #print(f"{time.time()}, {self._DASH_DELAY - self.last_dash_time}")

            if self._isFacingRight:
                self._shadowFacingRight = True
                self.collider.centerx += self._DASH_DISTANCE
                for i in range(Player.SHADOW_AMOUNT):
                    self.shadowImagesPos[i] = pygame.Rect((self.rect.topleft), (0, 0))
                    self.shadowImagesPos[i].centerx -= self._DASH_DISTANCE * i/Player.SHADOW_AMOUNT - self._DASH_DISTANCE

            else:
                self._shadowFacingRight = False
                self.collider.centerx -= self._DASH_DISTANCE
                for i in range(Player.SHADOW_AMOUNT):
                    self.shadowImagesPos[i] = pygame.Rect((self.rect.topleft), (0, 0))
                    self.shadowImagesPos[i].centerx += self._DASH_DISTANCE * i/Player.SHADOW_AMOUNT - self._DASH_DISTANCE

            Player.DASH_SOUND.play()
            t = Timer(self._DASH_DELAY, self._dashReadySound)
            t.start()
            self.last_dash_time = time.time()

    def _dashReadySound(self):
        if MainMenu.MainMenu.state is not MainMenu.MainMenu.State.closed:
            return
        else:
            Player.DASH_READY.play()

    def _returnShadowAlpha(self, i):
        alpha = 250 - (i / Player.SHADOW_AMOUNT) * 250
        alpha *= 1 - (time.time() - self.last_dash_time) / self._DASH_ANIMATION_TIME
        return int(alpha)


    def _isOutOfMap(self):
        #Stop on the left wall
        if self.collider.centerx < Camera.Camera.LEFT_WALL:
            self.collider.centerx = Camera.Camera.LEFT_WALL

        #Fell out of the map
        if self.collider.centery > 1000:
            LevelManager.LevelManager.restartLevel()

    def _collisionWithBlock(self):
        self.canJump = False

        for i in Block.Block.allBlocks:
            if self.collider.colliderect(i.rect):
                halfBlockSize = i.rect.size[0] / 2, i.rect.size[1] / 2

                deltaX = i.rect.centerx - (self.collider.centerx )
                deltaY = i.rect.centery - (self.collider.centery )
                intersectX = abs(deltaX) - (halfBlockSize[0] + self.collider.size[0] / 2)
                intersectY = abs(deltaY) - (halfBlockSize[1] + self.collider.size[1] / 2)

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

                self.collider.centerx += changePositionX
                self.collider.centery += changePositionY

                if(changePositionY < 0):
                    self.canJump = True
                    self._velocityY = 0


                if (changePositionY > 0):
                    self._velocityY = 0

    def _collisionWithObstacle(self):
        for i in ObstacleManager.ObstacleManager.allObstacles:
            if self.collider.colliderect(i.hitbox):
                LevelManager.LevelManager.restartLevel()

    @staticmethod
    def _setUpAnimation():
        SIZE = 100
        NUMBER_OF_IMAGES = 4

        #walking
        for i in range(NUMBER_OF_IMAGES):
            img = pygame.image.load(f"images/cat/walk/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (SIZE, SIZE))
            Player.ANIMATION_WALK_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Player.ANIMATION_WALK_RIGHT)):
            flippedImage = pygame.transform.flip(Player.ANIMATION_WALK_RIGHT[i], True, False)
            Player.ANIMATION_WALK_LEFT.append(flippedImage)

        #jumping
        img = pygame.image.load(f"images/cat/jumpUp.png")
        readyImg = pygame.transform.scale(img, (SIZE, SIZE))
        Player.IMG_JUMP_UP_RIGHT = readyImg.convert_alpha()

        flippedImage = pygame.transform.flip(readyImg, True, False)
        Player.IMG_JUMP_UP_LEFT = flippedImage.convert_alpha()

        #flying
        img = pygame.image.load(f"images/cat/flying.png")
        readyImg = pygame.transform.scale(img, (SIZE, SIZE))
        Player.IMG_FLYING_RIGHT = readyImg.convert_alpha()

        flippedImage = pygame.transform.flip(readyImg, True, False)
        Player.IMG_FLYING_LEFT = flippedImage.convert_alpha()

        #falling
        img = pygame.image.load(f"images/cat/fallDown.png")
        readyImg = pygame.transform.scale(img, (SIZE, SIZE))
        Player.IMG_FALL_DOWN_RIGHT = readyImg.convert_alpha()

        flippedImage = pygame.transform.flip(readyImg, True, False)
        Player.IMG_FALL_DOWN_LEFT = flippedImage.convert_alpha()

        #idle animations
        for i in range(6):
            idleAnimationRight = []
            idleAnimationLeft = []
            numOfAnimationFrames = 8

            if i == 4 or i == 5:
                numOfAnimationFrames = 4

            for j in range(numOfAnimationFrames):
                img = pygame.image.load(f"images/cat/idle{i+1}/{j + 1}.png")
                readyImg = pygame.transform.scale(img, (SIZE, SIZE))
                idleAnimationRight.append(readyImg.convert_alpha())

                flippedImage = pygame.transform.flip(readyImg, True, False)
                idleAnimationLeft.append(flippedImage)

            Player.ALL_IDLE_ANIMATIONS_RIGHT.append(idleAnimationRight)
            Player.ALL_IDLE_ANIMATIONS_LEFT.append(idleAnimationLeft)

        #dash
        dashImage = pygame.image.load(f"images/cat/dash.png").convert_alpha()
        dashImage = pygame.transform.scale(dashImage, (SIZE, SIZE))

        Player.IMG_SHADOW_RIGHT = dashImage

        flippedImage = pygame.transform.flip(Player.IMG_SHADOW_RIGHT, True, False)
        Player.IMG_SHADOW_LEFT = flippedImage

        Player._animationWasSetUp = True

    def _animate(self):
        animationSpeed = 1
        animation = Player.ANIMATION_WALK_RIGHT
        stopOnLastFrame = False

        if self._velocityY != 0:
            if abs(self._velocityY) < 2:
                if self._isFacingRight:
                    self.image = Player.IMG_FLYING_RIGHT
                    return
                else:
                    self.image = Player.IMG_FLYING_LEFT
                    return

            elif self._velocityY > 0:
                if self._isFacingRight:
                    self.image = Player.IMG_FALL_DOWN_RIGHT
                    return
                else:
                    self.image = Player.IMG_FALL_DOWN_LEFT
                    return
            else:
                if self._isFacingRight:
                    self.image = Player.IMG_JUMP_UP_RIGHT
                    return
                else:
                    self.image = Player.IMG_JUMP_UP_LEFT
                    return
        else:
            if self._velocityX is 0:
                if self._prevVelocityX is not 0 or (self._prevVelocityY is not 0 and self._velocityY is 0):
                    self._selectRandomIdleAnimation()
                animationSpeed = 3.5
                animation = self.currentIdleAnimation

            elif self._isFacingRight:
                animationSpeed = 12
                animation = Player.ANIMATION_WALK_RIGHT

            else:
                animationSpeed = 12
                animation = Player.ANIMATION_WALK_LEFT

        currentTime = int(time.time() * animationSpeed)

        if currentTime % len(animation) != self._prevAnimationFrame:
            if stopOnLastFrame and self._prevAnimationFrame is len(animation) - 1:
                self._prevAnimationFrame = len(animation) - 1
            else:
                self._prevAnimationFrame = currentTime % len(animation)
            self.image = animation[self._prevAnimationFrame]

    def _selectRandomIdleAnimation(self):
        #Thanks to this if statement there is 90% chance of getting standing animation
        rand = randrange(10)
        if rand is not 1:
            randStandingAnimation = randrange(2)
            if self._isFacingRight:
                self.currentIdleAnimation = self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_RIGHT[randStandingAnimation]
            else:
                self.currentIdleAnimation = self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_LEFT[randStandingAnimation]
            return

        randAnimation = randrange(len(Player.ALL_IDLE_ANIMATIONS_RIGHT))
        if self._isFacingRight:
            self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_RIGHT[randAnimation]
        else:
            self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_LEFT[randAnimation]
