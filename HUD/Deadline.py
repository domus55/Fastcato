import time
import pygame

import GameInfo
import LevelManager
import Screen


class Deadline:
    _startTime = time.time()
    isRunning = False
    timeOut = False

    # Font
    _FONT = pygame.font.Font("fonts/timer.ttf", 50)
    _color = (255, 255, 255)
    _FONT_BACKGROUND = pygame.Surface((165, 44))
    _FONT_BACKGROUND.set_alpha(100)

    SOUND_TIMER = pygame.mixer.Sound("sounds/timer.wav")


    @staticmethod
    def update(keyPressed):
        Deadline._checkStart(keyPressed)

    @staticmethod
    def _checkStart(keyPressed):
        if keyPressed is None or LevelManager.LevelManager.currentLevel == 7:
            return

        if not Deadline.isRunning:
            if keyPressed[pygame.K_w] or keyPressed[pygame.K_a] or keyPressed[pygame.K_s] or keyPressed[pygame.K_d] or keyPressed[pygame.K_LSHIFT]:
                Deadline._start()

    @staticmethod
    def _start():
        Deadline.SOUND_TIMER.set_volume(GameInfo.GameInfo.getSound())
        Deadline._startTime = time.time()
        Deadline.isRunning = True
        Deadline.timeOut = False
        Deadline._color = (255, 255, 255)

    @staticmethod
    def time():
        return time.time() - Deadline._startTime

    @staticmethod
    def stop():
        Deadline.isRunning = False
        Deadline._color = (255, 255, 255)

    @staticmethod
    def restart():
        Deadline._startTime = time.time()

    @staticmethod
    def render():
        if LevelManager.LevelManager.currentLevel == 7:  # Don't display on last level
            return
        strr = ""
        deltaTime = time.time() - Deadline._startTime
        if not Deadline.isRunning:
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

        # set font _color
        if minutes == 0:
            if seconds >= 50 and seconds < 55:
                a = 255 - (deltaTime - 50) * 51
                Deadline._color = (255, 255, a)
            elif seconds >= 55:
                a = (deltaTime - 55) * 51
                Deadline._color = (255, 255 - a, 0)

        if minutes >= 1 and not Deadline.timeOut:
            Deadline._color = (255, 0, 0)
            if Deadline.timeOut is False:
                Deadline.SOUND_TIMER.play()
            Deadline.timeOut = True

        #font size after 60 seconds
        if deltaTime > 60 and deltaTime < 60.3:
            if deltaTime < 60.15: #font is growing
                fontSize = 50 + (deltaTime - 60) * 75
            else: #font is shrinking
                fontSize = 61.25 - (deltaTime - 60.15) * 75

            Deadline._FONT = pygame.font.Font("fonts/timer.ttf", int(fontSize))
        else:
            if Deadline._FONT.size("a") != (22, 73):
                Deadline._FONT = pygame.font.Font("fonts/timer.ttf", 50)

        Screen.screen.blit(Deadline._FONT_BACKGROUND, (45, 45))

        surface = Deadline._FONT.render(strr, False, Deadline._color)
        Screen.screen.blit(surface, (50, 26))

    @staticmethod
    def strTime():
        strr = ""
        time = Deadline.time()

        seconds = int(time)
        minutes = seconds // 60
        ms = int(time * 1000 % 1000)

        seconds = seconds % 60
        if minutes <= 9:
            strr += '0'

        strr += str(minutes)
        strr += ':'

        if seconds <= 9:
            strr += '0'
        strr += str(seconds)
        strr += '.'

        if ms <= 99:
            strr += '0'
            if ms <= 9:
                strr += '0'

        strr += str(ms)

        return strr
