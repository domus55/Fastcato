from enum import IntEnum
import pygame

import Camera
from Screen import screen


class Icons:
    #Images
    W_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/w1.png"), (42, 40)).convert_alpha()
    W_DOWN = pygame.transform.scale(pygame.image.load("images/gui/buttons/w2.png"), (42, 40)).convert_alpha()
    A_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/a1.png"), (42, 40)).convert_alpha()
    A_DOWN = pygame.transform.scale(pygame.image.load("images/gui/buttons/a2.png"), (42, 40)).convert_alpha()
    S_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/s1.png"), (42, 40)).convert_alpha()
    S_DOWN = pygame.transform.scale(pygame.image.load("images/gui/buttons/s2.png"), (42, 40)).convert_alpha()
    D_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/d1.png"), (42, 40)).convert_alpha()
    D_DOWN = pygame.transform.scale(pygame.image.load("images/gui/buttons/d2.png"), (42, 40)).convert_alpha()
    LSHIFT_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/shift1.png"), (93, 40)).convert_alpha()
    LSHIFT_DOWN = pygame.transform.scale(pygame.image.load("images/gui/buttons/shift2.png"), (93, 40)).convert_alpha()
    DEATH_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/death.png"), (40, 40)).convert_alpha()
    ATTENTION_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/attention.png"), (40, 40)).convert_alpha()
    STAR_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/star.png"), (40, 40)).convert_alpha()
    TIP_UP = pygame.transform.scale(pygame.image.load("images/gui/buttons/tip.png"), (200, 70)).convert_alpha()


    class Type(IntEnum):
        W = 1
        A = 2
        S = 3
        D = 4
        LSHIFT = 5
        DEATH = 101
        ATTENTION = 102
        STAR = 103
        TIP = 104

    allButton = []

    def __init__(self, type, pos):
        self.pos = pos
        self.type = type
        self.image = eval("Icons." + str(type)[5:] + "_UP")
        self.image.set_alpha(210)

    @staticmethod
    def add(type, pos):
        obj = Icons(type, pos)
        Icons.allButton.append(obj)

    @staticmethod
    def renderAll():
        for i in Icons.allButton:
            i.render()

    def render(self):
        screen.blit(self.image, Camera.Camera.relativePosition(self.pos))

    @staticmethod
    def buttonDown(keyPressed):
        for i in Icons.allButton:
            i._setButtonImage(keyPressed)

    @staticmethod
    def buttonUp(keyPressed):
        for i in Icons.allButton:
            i._setButtonImage(keyPressed)

    def _setButtonImage(self, keyPressed):
        if int(self.type) > 100:
            return
        if self.type == Icons.Type.LSHIFT:
            typeStr = str(self.type)[5:]
        else:
            typeStr = (str(self.type)[5:]).lower()

        if eval("keyPressed[pygame.K_" + typeStr + "]"):
            self.image = eval("Icons." + str(self.type)[5:] + "_DOWN")
        else:
            self.image = eval("Icons." + str(self.type)[5:] + "_UP")


