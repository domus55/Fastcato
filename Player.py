import time
from random import randrange
import pygame.mixer


from ProjectCommon import PATH
import Block
import GameInfo
import LevelManager
import Camera
import MainMenu
from HUD import Deadline, BirdCounter, Buttons
from Obstacles import ObstacleManager
from Screen import *
from InnerTimer import *
from threading import Timer


class Player(pygame.sprite.Sprite):
    _instance = None

    ANIMATION_WALK_RIGHT = []
    ANIMATION_WALK_LEFT = []
    ANIMATION_MEOW_RIGHT = []

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

    # sounds
    DASH_SOUND = pygame.mixer.Sound(f"{PATH}sounds/dash.wav")
    DASH_READY = pygame.mixer.Sound(f"{PATH}sounds/dashReady.wav")
    SOUND_MEOW1 = pygame.mixer.Sound(f"{PATH}sounds/meow1.wav")
    SOUND_MEOW2 = pygame.mixer.Sound(f"{PATH}sounds/meow2.wav")

    _animationWasSetUp = False

    def __init__(self):
        super().__init__()
        if not Player._animationWasSetUp:
            Player._setUpAnimation()
        self._prevAnimationFrame = 0
        self.image = Player.ANIMATION_WALK_RIGHT[0]
        self.pos = [0.0, 0.0]  # top left

        # Movement
        self.collider = pygame.Rect(0, 0, 50, 35)
        self._velocityX = 0
        self._velocityY = 0
        self.speed = 3
        self.canJump = False
        self.startingPosition = (0, 0)

        # Dash
        self._DASH_DELAY = 3  # in seconds
        self._DASH_DISTANCE = 150
        self._DASH_ANIMATION_TIME = 1  # in seconds
        self.last_dash_time = time.time() - self._DASH_DELAY
        self.shadowImagesPos = [pygame.Rect(0, 0, 0, 0)] * Player.SHADOW_AMOUNT
        self._shadowFacingRight = True

        # Animation
        self.meowStartTime = 0 #used to render lines when cat meows in _lastLevelAnimation
        self._prevVelocityX = 0  # it's used for animations
        self._prevVelocityY = 0  # it's used for animations
        self._isFacingRight = True
        self.currentIdleAnimation = None
        self._selectRandomIdleAnimation()

    @staticmethod
    def getInstance():
        if Player._instance is None:
            Player._instance = Player()
        return Player._instance

    def update(self, keyPressed):
        if (LevelManager.LevelManager.currentLevel == 6 and BirdCounter.BirdCounter.birdsCatched == BirdCounter.BirdCounter.allBirds and GameInfo.GameInfo.levelTime[6] < 60) or \
                LevelManager.LevelManager.currentLevel == 7:
            self._lastLevelAnimation()
        else:
            self._move(keyPressed)
            self.collider.topleft = self.pos
            self._dash(keyPressed)
            self._isOutOfMap()
        self._collisionWithBlock()
        self._collisionWithObstacle()
        self._animate()
        # if Deadline.Deadline.time() > 15:
        #    print(self.pos[0])

    def render(self):
        #self.pos[0] = 1200
        self.collider.topleft = self.pos
        # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(Camera.Camera.relativePosition(self.collider.topleft), self.collider.size))
        screen.blit(self.image, Camera.Camera.relativePosition((self.pos[0] - 25, self.pos[1] - 65)))

        if time.time() < self.last_dash_time + self._DASH_ANIMATION_TIME:
            for i in range(Player.SHADOW_AMOUNT):
                alpha = self._returnShadowAlpha(i)
                if self._shadowFacingRight:
                    Player.IMG_SHADOW_RIGHT.set_alpha(alpha)
                    screen.blit(Player.IMG_SHADOW_RIGHT,
                                Camera.Camera.relativePosition(self.shadowImagesPos[i].topleft))
                else:
                    Player.IMG_SHADOW_LEFT.set_alpha(alpha)
                    screen.blit(Player.IMG_SHADOW_LEFT, Camera.Camera.relativePosition(self.shadowImagesPos[i].topleft))

        if self.meowStartTime > 0:
            self.meowStartTime += InnerTime.deltaTime / 1000
            if self.meowStartTime > 10:
                self.meowStartTime = 0
            if self.meowStartTime < 1:
                screen.blit(self.ANIMATION_MEOW_RIGHT[int(self.meowStartTime * 3)], (1195, 735))

        # pygame.draw.rect(screen, (255, 0, 0), self.collider)

    def restart(self):
        self.collider.center = self.startingPosition
        self.pos = list(self.collider.topleft)
        self.pos[1] += 10
        self._velocityY = 0
        self.last_dash_time = time.time() - self._DASH_DELAY
        Player.DASH_SOUND.set_volume(GameInfo.GameInfo.getSound())
        Player.DASH_READY.set_volume(GameInfo.GameInfo.getSound())
        Player.SOUND_MEOW1.set_volume(GameInfo.GameInfo.getSound())
        Player.SOUND_MEOW2.set_volume(GameInfo.GameInfo.getSound())
        Deadline.Deadline.stop()

    def _move(self, keyPressed):
        self._prevVelocityX = self._velocityX  # it's used for animations
        self._prevVelocityY = self._velocityY  # it's used for animations
        self._velocityX = 0
        self._velocityY += 0.2 * InnerTime.deltaTime / 10

        if keyPressed is not None:
            if keyPressed[pygame.K_a] or Buttons.Buttons.left:
                self._velocityX -= self.speed
                self._isFacingRight = False
            if keyPressed[pygame.K_d] or Buttons.Buttons.right:
                self._velocityX += self.speed
                self._isFacingRight = True
            if (keyPressed[pygame.K_w] or keyPressed[pygame.K_SPACE] or Buttons.Buttons.jump) and self.canJump:
                self._velocityY = - self.speed * 3
                self.canJump = False

        deltaX = self._velocityX * InnerTime.deltaTime / 10.0
        deltaY = self._velocityY * InnerTime.deltaTime / 10.0

        # If user has less than 30FPS then, there is a chance that deltaY will be greater than 25, it can lead to falling out of the map
        # To prevent it in that case I move him only 15px(MAX_DELTA) and check collisions
        # I repeat that until he is in right position
        MAX_DELTA = 15
        while abs(deltaX) > MAX_DELTA or abs(deltaY) > MAX_DELTA:
            if abs(deltaX) > MAX_DELTA:
                changeX = MAX_DELTA if deltaX > 0 else -MAX_DELTA
            else:
                changeX = 0
            deltaX -= changeX
            self.pos[0] += changeX

            if abs(deltaY) > MAX_DELTA:
                changeY = MAX_DELTA if deltaY > 0 else -MAX_DELTA
            else:
                changeY = 0
            deltaY -= changeY
            self.pos[1] += changeY

            self.collider.topleft = self.pos
            self._collisionWithBlock()

        self.pos[0] += deltaX
        self.pos[1] += deltaY

    def _dash(self, keyPressed):
        if keyPressed is None or Deadline.Deadline.time() < 0.25:
            return

        if (keyPressed[pygame.K_LSHIFT] or Buttons.Buttons.dash) and time.time() > self.last_dash_time + self._DASH_DELAY:
            if self._isFacingRight:
                self._shadowFacingRight = True
                self.collider.centerx += self._DASH_DISTANCE
                for i in range(Player.SHADOW_AMOUNT):
                    self.shadowImagesPos[i] = pygame.Rect(self.pos, (0, 0))
                    self.shadowImagesPos[
                        i].centerx -= self._DASH_DISTANCE * i / Player.SHADOW_AMOUNT - self._DASH_DISTANCE
                    self.shadowImagesPos[i].centery -= 70

            else:
                self._shadowFacingRight = False
                self.collider.centerx -= self._DASH_DISTANCE
                for i in range(Player.SHADOW_AMOUNT):
                    self.shadowImagesPos[i] = pygame.Rect(self.pos, (0, 0))
                    self.shadowImagesPos[
                        i].centerx += self._DASH_DISTANCE * i / Player.SHADOW_AMOUNT - self._DASH_DISTANCE
                    self.shadowImagesPos[i].centery -= 70

            # check if after dash is in any blocks
            inBlock = True
            while inBlock:
                inBlock = False
                for i in Block.Block.allBlocks:
                    if self.collider.colliderect(i.rect):
                        inBlock = True

                if inBlock:
                    self.collider.centery -= 1
                    if self._isFacingRight:
                        self.collider.centerx -= 5
                    else:
                        self.collider.centerx += 5

            self.pos = list(self.collider.topleft)
            Player.DASH_SOUND.play()
            if GameInfo.GameInfo.BUILD_TYPE != GameInfo.BuildType.WEB:
                t = Timer(self._DASH_DELAY, self._dashReadySound)
                t.start()
            self.last_dash_time = time.time()

    def _dashReadySound(self):
        if MainMenu.MainMenu.state is not MainMenu.MainMenu.State.CLOSED:
            return
        else:
            Player.DASH_READY.play()

    def _returnShadowAlpha(self, i):
        alpha = 250 - (i / Player.SHADOW_AMOUNT) * 250
        alpha *= 1 - (time.time() - self.last_dash_time) / self._DASH_ANIMATION_TIME
        return int(alpha)

    def _isOutOfMap(self):
        # Stop on the map borders
        PLAYER_WIDTH = 25
        if self.pos[0] < Camera.Camera.borderLeft - PLAYER_WIDTH:
            self.pos[0] = Camera.Camera.borderLeft - PLAYER_WIDTH

        if self.pos[0] > Camera.Camera.borderRight - PLAYER_WIDTH:
            self.pos[0] = Camera.Camera.borderRight - PLAYER_WIDTH

        # Fell out of the map
        if self.pos[1] > 1000:
            self._playMeowSound()
            LevelManager.LevelManager.restartLevel()

    def _collisionWithBlock(self):
        self.canJump = False

        for i in Block.Block.allColliders:
            if self.collider.colliderect(i):
                halfBlockSize = i.size[0] / 2, i.size[1] / 2

                deltaX = i.centerx - self.collider.centerx
                deltaY = i.centery - self.collider.centery
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

                if abs(changePositionX) > 1:
                    self.pos[0] = self.collider.left

                if changePositionY != 0:
                    self.pos[1] = self.collider.top

                if changePositionY < 0:
                    self.canJump = True
                    if self._velocityY >= 0:
                        self._velocityY = 0

                if changePositionY > 0:
                    self._velocityY = 0

    def _collisionWithObstacle(self):
        for i in ObstacleManager.ObstacleManager.allObstacles:
            if self.collider.colliderect(i.hitbox):
                self._playMeowSound()
                LevelManager.LevelManager.restartLevel()

    @staticmethod
    def _setUpAnimation():
        SIZE = 100

        # walking
        for i in range(4):
            img = pygame.image.load(f"{PATH}images/cat/walk/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (SIZE, SIZE))
            Player.ANIMATION_WALK_RIGHT.append(readyImg.convert_alpha())

        for i in range(len(Player.ANIMATION_WALK_RIGHT)):
            flippedImage = pygame.transform.flip(Player.ANIMATION_WALK_RIGHT[i], True, False)
            Player.ANIMATION_WALK_LEFT.append(flippedImage)

        # jumping
        img = pygame.image.load(f"{PATH}images/cat/jumpUp.png")
        readyImg = pygame.transform.scale(img, (SIZE, SIZE))
        Player.IMG_JUMP_UP_RIGHT = readyImg.convert_alpha()

        flippedImage = pygame.transform.flip(readyImg, True, False)
        Player.IMG_JUMP_UP_LEFT = flippedImage.convert_alpha()

        # flying
        img = pygame.image.load(f"{PATH}images/cat/flying.png")
        readyImg = pygame.transform.scale(img, (SIZE, SIZE))
        Player.IMG_FLYING_RIGHT = readyImg.convert_alpha()

        flippedImage = pygame.transform.flip(readyImg, True, False)
        Player.IMG_FLYING_LEFT = flippedImage.convert_alpha()

        # falling
        img = pygame.image.load(f"{PATH}images/cat/fallDown.png")
        readyImg = pygame.transform.scale(img, (SIZE, SIZE))
        Player.IMG_FALL_DOWN_RIGHT = readyImg.convert_alpha()

        flippedImage = pygame.transform.flip(readyImg, True, False)
        Player.IMG_FALL_DOWN_LEFT = flippedImage.convert_alpha()

        # idle animations
        for i in range(6):
            idleAnimationRight = []
            idleAnimationLeft = []
            numOfAnimationFrames = 8

            if i == 4 or i == 5:
                numOfAnimationFrames = 4

            for j in range(numOfAnimationFrames):
                img = pygame.image.load(f"{PATH}images/cat/idle{i + 1}/{j + 1}.png")
                readyImg = pygame.transform.scale(img, (SIZE, SIZE))
                idleAnimationRight.append(readyImg.convert_alpha())

                flippedImage = pygame.transform.flip(readyImg, True, False)
                idleAnimationLeft.append(flippedImage)

            Player.ALL_IDLE_ANIMATIONS_RIGHT.append(idleAnimationRight)
            Player.ALL_IDLE_ANIMATIONS_LEFT.append(idleAnimationLeft)

        # dash
        dashImage = pygame.image.load(f"{PATH}images/cat/dash.png").convert_alpha()
        dashImage = pygame.transform.scale(dashImage, (SIZE, SIZE))

        Player.IMG_SHADOW_RIGHT = dashImage

        flippedImage = pygame.transform.flip(Player.IMG_SHADOW_RIGHT, True, False)
        Player.IMG_SHADOW_LEFT = flippedImage

        # meow
        for i in range(3):
            img = pygame.image.load(f"{PATH}images/cat/meow/{i + 1}.png")
            readyImg = pygame.transform.scale(img, (50, 50))
            Player.ANIMATION_MEOW_RIGHT.append(readyImg.convert_alpha())

        Player._animationWasSetUp = True

    def _animate(self):
        animationSpeed = 1
        animation = Player.ANIMATION_WALK_RIGHT
        stopOnLastFrame = False

        if self._velocityY != 0 and self._prevVelocityY != 0:
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
            if self._velocityX == 0:
                if self._prevVelocityX != 0:
                    self._selectRandomIdleAnimation()
                if self._prevVelocityY != 0 and self._velocityY == 0 and GameInfo.GameInfo.BUILD_TYPE is not GameInfo.BuildType.WEB:
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
        # Thanks to this if statement there is 90% chance of getting standing animation
        rand = randrange(10)
        if rand != 1:
            randStandingAnimation = randrange(2)
            if self._isFacingRight:
                self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_RIGHT[randStandingAnimation]
            else:
                self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_LEFT[randStandingAnimation]
            return

        randAnimation = randrange(len(Player.ALL_IDLE_ANIMATIONS_RIGHT))
        if self._isFacingRight:
            self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_RIGHT[randAnimation]
        else:
            self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_LEFT[randAnimation]

    def _playMeowSound(self):
        SOUND_CHANCE = 50  # percent
        if randrange(1, 100) <= SOUND_CHANCE:
            sound = randrange(2) + 1
            eval("self.SOUND_MEOW" + str(sound) + ".play()")

    def _lastLevelAnimation(self):
        if not hasattr(self, "animationStage"):
            self.animationStage = 1

        debug = False
        self._isFacingRight = True
        self._prevVelocityX = 0
        self._prevVelocityY = 0
        self._velocityX = 0
        speed = self.speed * 0.6
        time = Deadline.Deadline.time()

        if debug:
            time *= 4
            speed *= 4

        if LevelManager.LevelManager.currentLevel == 7:
            if self.pos[0] < 300:  # Go
                self.animationStage = 1
            elif time < 8:  # Wait and see what is happening
                if self.animationStage == 1:
                    self.currentIdleAnimation = Player.ALL_IDLE_ANIMATIONS_RIGHT[1]
                self.animationStage = 2
            elif self.pos[0] < 1200 and self.animationStage <= 3:  # Scare birds and go to small cat
                self.animationStage = 3
            elif time < 16.5:                 # MEOW
                self.animationStage = 4
            elif self.pos[0] > 725:         # Go to the cake
                self.animationStage = 5
            else:                           # Party!
                self.animationStage = 6

            if self.animationStage == 1 or self.animationStage == 3:
                self._velocityX = speed

            if self.animationStage == 4:
                if self.meowStartTime == 0:
                    Player.SOUND_MEOW1.play()
                    self.meowStartTime = 0.05

            if self.animationStage == 5:
                self._isFacingRight = False
                self._velocityX = -speed

        else:
            # go right before on the level before finish level
            self._velocityX = speed

        self._velocityY += 0.2 * InnerTime.deltaTime / 10
        self.pos[0] += self._velocityX * InnerTime.deltaTime / 10.0
        self.pos[1] += self._velocityY * InnerTime.deltaTime / 10.0


