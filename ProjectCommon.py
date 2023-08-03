import GameInfo
import pygame
import os

PATH = os.path.abspath('.')+'/'


def loadImage(path, size):
    return pygame.transform.scale(pygame.image.load(f"{path}"), size).convert_alpha()


def centerPos(pos):
    x = (800 - pos[0]) * GameInfo.GameInfo.HUD_SCALE + 800
    y = (450 - pos[1]) * GameInfo.GameInfo.HUD_SCALE + 450

    return x, y
