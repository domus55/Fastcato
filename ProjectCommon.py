import pygame
import os

PATH = os.path.abspath('.')+'/'


def loadImage(path, size):
    return pygame.transform.scale(pygame.image.load(f"{path}"), size).convert_alpha()
