from random import randrange

import pygame

from src import game_info
from src.project_common import PATH

MUSIC_ENDED = pygame.USEREVENT + 1


class Music:
    @staticmethod
    def start(first_music: bool = False):
        if first_music:
            pygame.mixer.music.load(f"{PATH}sounds/music/Anita music.mp3")
        else:
            NUMBER_OF_MUSICS = 5
            music = randrange(NUMBER_OF_MUSICS) + 1
            pygame.mixer.music.load(f"{PATH}sounds/music/{music}.wav")

        pygame.mixer.music.set_endevent(MUSIC_ENDED)
        Music.adjust_volume()
        pygame.mixer.music.play(fade_ms=5000)

    @staticmethod
    def adjust_volume():
        pygame.mixer.music.set_volume(game_info.GameInfo.getMusic())
