import pygame.freetype

import InGameMenu
import InnerTimer
import Screen


class Credits:
    _FONT = pygame.freetype.Font("fonts/timer.ttf", 50)
    _color = (255, 255, 255)
    text = []
    _fade = pygame.Surface((1600, 900))
    y = 9999
    _started = False

    @staticmethod
    def restart():
        Credits._started = False
        Credits.y = 875

    @staticmethod
    def start():
        Credits._started = True
        Credits.text.clear()

        lines = "Creator\nDominik Palenik\n\nI hope you enjoyed\nThank you for playing".splitlines()
        for i, l in enumerate(lines):
            Credits.text.append(pygame.freetype.Font.render(Credits._FONT, l, Credits._color)[0])

    @staticmethod
    def renderText():
        if not Credits._started:
            return

        Credits.y -= InnerTimer.InnerTime.deltaTime/30
        for i, l in enumerate(Credits.text):
            x = 800 - l.get_width() / 2
            Screen.screen.blit(l, (x, Credits.y + 45 * i))

    @staticmethod
    def renderFade():
        if not Credits._started:
            return

        if Credits.y < 350:
            alpha = (350 - Credits.y)
            if alpha > 255:
                alpha = 255

            Credits._fade.set_alpha(alpha)
            Credits._fade.fill((0, 0, 0))
            Screen.screen.blit(Credits._fade, (0, 0))

            if Credits.y < 0 and InGameMenu.InGameMenu.state == InGameMenu.InGameMenu.State.CLOSED:
                InGameMenu.InGameMenu.open()
