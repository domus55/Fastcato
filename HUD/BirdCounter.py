import time
import pygame

import Bird
import GameInfo
import LevelManager
import Screen
from ProjectCommon import loadImage, PATH


class BirdCounter:
    SCALE = GameInfo.GameInfo.HUD_SCALE
    IMG = loadImage(f"{PATH}images/gui/bird.png", (35 * SCALE, 33 * SCALE))

    color = (255, 255, 255)
    _FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(50 * SCALE))
    _FONT_BACKGROUND = pygame.Surface((135 * SCALE, 44 * SCALE))

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
                fontSize = (50 + deltaTime * 75) * BirdCounter.SCALE
            else:  # font is shrinking
                fontSize = (61.25 - (deltaTime - 0.15) * 75) * BirdCounter.SCALE

            BirdCounter._FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(fontSize))
        else:
            if BirdCounter._FONT.size("a") != (int(22 * BirdCounter.SCALE), int(73 * BirdCounter.SCALE)):
                BirdCounter._FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(50 * BirdCounter.SCALE))

        strr = str(BirdCounter.birdsCatched) + "/" + str(BirdCounter.allBirds)

        Screen.screen.blit(BirdCounter._FONT_BACKGROUND, (45, 50 + 50 * BirdCounter.SCALE))
        Screen.screen.blit(BirdCounter.IMG, (45 + 5 * BirdCounter.SCALE, 50 + 55 * BirdCounter.SCALE))

        surface = BirdCounter._FONT.render(strr, False, BirdCounter.color)
        Screen.screen.blit(surface, (55 + 45 * BirdCounter.SCALE, 50 + 31 * BirdCounter.SCALE))

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
            surfaceWidth = (99 + stringLen * 21) * BirdCounter.SCALE
            BirdCounter._FONT_BACKGROUND = pygame.Surface((surfaceWidth, 44 * BirdCounter.SCALE))
            BirdCounter._FONT_BACKGROUND.set_alpha(100)




