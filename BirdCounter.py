import time

import pygame
import pygame.freetype

import Bird
import GameInfo
import Screen

class BirdCounter:
    IMG = pygame.transform.scale(pygame.image.load("images/gui/bird.png"), (35, 33)).convert_alpha()
    _FONT = pygame.freetype.Font("fonts/timer.ttf", 50)
    color = (255, 255, 255)
    _FONT_BACKGROUND = pygame.Surface((135, 44))

    SOUND = pygame.mixer.Sound("sounds/bird.wav")

    allBirds = 0
    birdsCatched = 0
    lastCatchTime = 0

    @staticmethod
    def render():
        deltaTime = time.time() - BirdCounter.lastCatchTime

        # font size after catching bird
        if deltaTime > 0 and deltaTime < 0.3:
            if deltaTime < 0.15:  # font is growing
                BirdCounter._FONT.size = 50 + deltaTime * 75
            else:  # font is shrinking
                BirdCounter._FONT.size = 61.25 - (deltaTime - 0.15) * 75
        else:
            BirdCounter._FONT.size = 50

        strr = str(BirdCounter.birdsCatched) + "/" + str(BirdCounter.allBirds)

        Screen.screen.blit(BirdCounter._FONT_BACKGROUND, (45, 100))
        Screen.screen.blit(BirdCounter.IMG, (50, 105))

        BirdCounter._FONT.render_to(Screen.screen, (100, 105), strr, BirdCounter.color)


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
            print(stringLen)
            print(surfaceWidth)




