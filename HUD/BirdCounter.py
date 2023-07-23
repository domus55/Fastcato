import time
import pygame

import Bird
import GameInfo
import LevelManager
import Screen
from ProjectCommon import loadImage, PATH


class BirdCounter:
    IMG = loadImage(f"{PATH}images/gui/bird.png", (35, 33))

    color = (255, 255, 255)
    _FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", 50)
    _FONT_BACKGROUND = pygame.Surface((135, 44))

    SOUND = pygame.mixer.Sound(f"{PATH}sounds/bird.wav")

    allBirds = 0
    birdsCatched = 0
    lastCatchTime = 0

    @staticmethod
    def render():
        if LevelManager.LevelManager.currentLevel == 7:  # Don't display on last level
            return
        deltaTime = time.time() - BirdCounter.lastCatchTime

        # font size after catching bird
        if deltaTime > 0 and deltaTime < 0.3:
            if deltaTime < 0.15:  # font is growing
                fontSize = 50 + deltaTime * 75
            else:  # font is shrinking
                fontSize = 61.25 - (deltaTime - 0.15) * 75

            BirdCounter._FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(fontSize))
        else:
            if BirdCounter._FONT.size("a") != (22, 73):
                BirdCounter._FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", 50)

        strr = str(BirdCounter.birdsCatched) + "/" + str(BirdCounter.allBirds)

        Screen.screen.blit(BirdCounter._FONT_BACKGROUND, (45, 100))
        Screen.screen.blit(BirdCounter.IMG, (50, 105))

        surface = BirdCounter._FONT.render(strr, False, BirdCounter.color)
        Screen.screen.blit(surface, (100, 81))


    #use after placing all birds on the map
    @staticmethod
    def restart():
        BirdCounter.allBirds = len(Bird.Bird.allBirds)
        BirdCounter.birdsCatched = 0
        BirdCounter.SOUND.set_volume(GameInfo.GameInfo.getSound())
        BirdCounter._setFontBackgroundWidth()

    @staticmethod
    def catchedBird():
        BirdCounter.birdsCatched += 1
        BirdCounter.lastCatchTime = time.time()
        BirdCounter.SOUND.play()
        BirdCounter._setFontBackgroundWidth()

    @staticmethod
    def _setFontBackgroundWidth():
            stringLen = len(str(BirdCounter.birdsCatched)) + len(str(BirdCounter.allBirds))
            surfaceWidth = 99 + stringLen * 21
            BirdCounter._FONT_BACKGROUND = pygame.Surface((surfaceWidth, 44))
            BirdCounter._FONT_BACKGROUND.set_alpha(100)




