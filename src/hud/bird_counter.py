import time

import pygame

from src import bird, game_info, level_manager, screen
from src.project_common import PATH, loadImage


class BirdCounter:
    SCALE = game_info.GameInfo.HUD_SCALE
    IMG = loadImage(f"{PATH}images/gui/bird.png", (35 * SCALE, 33 * SCALE))

    color = (255, 255, 255)
    pygame.font.init()
    _FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(50 * SCALE))
    _FONT_BACKGROUND = pygame.Surface((135 * SCALE, 44 * SCALE))
    pygame.mixer.init()
    SOUND = pygame.mixer.Sound(f"{PATH}sounds/bird.wav")

    all_birds = 0
    birds_caught = 0
    last_catch_time = 0

    @staticmethod
    def render():
        if level_manager.LevelManager.current_level == 7:  # Don't display on last level
            return
        delta_time = time.time() - BirdCounter.last_catch_time

        # font size after catching bird
        if 0 < delta_time < 0.3:
            if delta_time < 0.15:  # font is growing
                font_size = (50 + delta_time * 75) * BirdCounter.SCALE
            else:  # font is shrinking
                font_size = (61.25 - (delta_time - 0.15) * 75) * BirdCounter.SCALE

            BirdCounter._FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(font_size))
        else:
            if BirdCounter._FONT.size("a") != (int(22 * BirdCounter.SCALE), int(73 * BirdCounter.SCALE)):
                BirdCounter._FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(50 * BirdCounter.SCALE))

        strr = str(BirdCounter.birds_caught) + "/" + str(BirdCounter.all_birds)

        screen.screen.blit(BirdCounter._FONT_BACKGROUND, (45, 50 + 50 * BirdCounter.SCALE))
        screen.screen.blit(BirdCounter.IMG, (45 + 5 * BirdCounter.SCALE, 50 + 55 * BirdCounter.SCALE))

        surface = BirdCounter._FONT.render(strr, False, BirdCounter.color)
        screen.screen.blit(surface, (55 + 45 * BirdCounter.SCALE, 50 + 31 * BirdCounter.SCALE))

    # use after placing all birds on the map
    @staticmethod
    def restart():
        BirdCounter.all_birds = len(bird.Bird.all_birds)
        BirdCounter.birds_caught = 0
        BirdCounter.SOUND.set_volume(game_info.GameInfo.getSound())
        BirdCounter._set_font_background_width()

    @staticmethod
    def caught_bird():
        BirdCounter.birds_caught += 1
        BirdCounter.last_catch_time = time.time()
        BirdCounter.SOUND.play()
        BirdCounter._set_font_background_width()
        if BirdCounter.birds_caught >= BirdCounter.all_birds:
            level_manager.LevelManager.finished_level()

    @staticmethod
    def _set_font_background_width():
        string_len = len(str(BirdCounter.birds_caught)) + len(str(BirdCounter.all_birds))
        surface_width = (99 + string_len * 21) * BirdCounter.SCALE
        BirdCounter._FONT_BACKGROUND = pygame.Surface((surface_width, 44 * BirdCounter.SCALE))
        BirdCounter._FONT_BACKGROUND.set_alpha(100)




