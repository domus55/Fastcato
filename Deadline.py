import time
import pygame.freetype

import GameInfo
import Screen


class Deadline:
    _startTime = time.time() - 45
    _isRunning = False
    timeOut = False

    # Font
    pygame.freetype.init()
    GAME_FONT = pygame.freetype.Font("fonts/timer.ttf", 50)
    color = (255, 255, 255)
    _FONT_BACKGROUND = pygame.Surface((165, 44))
    _FONT_BACKGROUND.set_alpha(100)

    pygame.mixer.init()
    SOUND_TIMER = pygame.mixer.Sound("sounds/timer.wav")


    @staticmethod
    def update(keyPressed):
        Deadline._checkStart(keyPressed)

    @staticmethod
    def _checkStart(keyPressed):
        if not Deadline._isRunning:
            if keyPressed[pygame.K_w] or keyPressed[pygame.K_a] or keyPressed[pygame.K_s] or keyPressed[pygame.K_d] or keyPressed[pygame.K_LSHIFT]:
                Deadline._start()

    @staticmethod
    def _start():
        Deadline.SOUND_TIMER.set_volume(GameInfo.GameInfo.getSound())
        Deadline._startTime = time.time() - 45
        Deadline._isRunning = True
        Deadline.timeOut = False
        Deadline.color = (255, 255, 255)

    @staticmethod
    def stop():
        Deadline._isRunning = False
        Deadline.color = (255, 255, 255)

    @staticmethod
    def render():
        strr = ""
        deltaTime = time.time() - Deadline._startTime
        if not Deadline._isRunning:
            deltaTime = 0

        seconds = int(deltaTime)
        minutes = seconds//60
        ms = int(deltaTime * 10 % 10)

        seconds = seconds % 60
        if minutes <= 9:
            strr += '0'

        strr += str(minutes)
        strr += ':'

        if seconds <= 9:
            strr += '0'
        strr += str(seconds)
        strr += '.'

        strr += str(ms)

        #set font color
        if seconds >= 50 and seconds < 55:
            a = 255 - (deltaTime - 50) * 51
            Deadline.color = (255, 255, a)
        elif seconds >= 55:
            a = (deltaTime - 55) * 51
            Deadline.color = (255, 255 - a, 0)

        if minutes >= 1 and not Deadline.timeOut:
            Deadline.color = (255, 0, 0)
            if Deadline.timeOut is False:
                Deadline.SOUND_TIMER.play()
            Deadline.timeOut = True

        #font size after 60 seconds
        if deltaTime > 60 and deltaTime < 60.3:
            if deltaTime < 60.15: #font is growing
                Deadline.GAME_FONT.size = 50 + (deltaTime - 60) * 75
            else: #font is shrinking
                Deadline.GAME_FONT.size = 61.25 - (deltaTime - 60.15) * 75

        Screen.screen.blit(Deadline._FONT_BACKGROUND, (45, 45))
        Deadline.GAME_FONT.render_to(Screen.screen, (50, 50), strr, Deadline.color)