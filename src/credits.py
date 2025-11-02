import pygame

from src import in_game_menu, inner_timer, screen
from src.project_common import PATH


class Credits:
    pygame.font.init()
    _FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", 50)
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

        lines = "I hope you enjoyed\nThank you for playing\n\nCreator\nDominik Palenik".splitlines()
        for i, line in enumerate(lines):
            Credits.text.append(Credits._FONT.render(line, False, Credits._color))

    @staticmethod
    def renderText():
        if not Credits._started:
            return

        Credits.y -= inner_timer.InnerTime.deltaTime / 30
        for i, line in enumerate(Credits.text):
            x = 800 - line.get_width() / 2
            screen.screen.blit(line, (x, Credits.y + 45 * i))

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
            screen.screen.blit(Credits._fade, (0, 0))

            if Credits.y < 0 and in_game_menu.InGameMenu.state == in_game_menu.InGameMenu.State.CLOSED:
                in_game_menu.InGameMenu.open()
