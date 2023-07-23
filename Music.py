from random import randrange
import pygame

from ProjectCommon import PATH
import GameInfo

MUSIC_ENDED = pygame.USEREVENT + 1

class Music:
    @staticmethod
    def start():
        NUMBER_OF_MUSICS = 5
        music = randrange(NUMBER_OF_MUSICS) + 1
        pygame.mixer.music.load(f"{PATH}sounds/music/{music}.wav")
        pygame.mixer.music.set_endevent(MUSIC_ENDED)
        Music.adjustVolume()
        pygame.mixer.music.play(fade_ms=5000)

    @staticmethod
    def adjustVolume():
        pygame.mixer.music.set_volume(GameInfo.GameInfo.getMusic())