from enum import Enum

import GameInfo
import pygame

import Camera
from HUD import Buttons
from ProjectCommon import PATH, loadImage
from Screen import screen

class Icons:
    #Images
    W_UP = loadImage(f"{PATH}images/gui/icons/w1.png", (42, 40))
    W_DOWN = loadImage(f"{PATH}images/gui/icons/w2.png", (42, 40))
    A_UP = loadImage(f"{PATH}images/gui/icons/a1.png", (42, 40))
    A_DOWN = loadImage(f"{PATH}images/gui/icons/a2.png", (42, 40))
    S_UP = loadImage(f"{PATH}images/gui/icons/s1.png", (42, 40))
    S_DOWN = loadImage(f"{PATH}images/gui/icons/s2.png", (42, 40))
    D_UP = loadImage(f"{PATH}images/gui/icons/d1.png", (42, 40))
    D_DOWN = loadImage(f"{PATH}images/gui/icons/d2.png", (42, 40))
    LSHIFT_UP = loadImage(f"{PATH}images/gui/icons/shift1.png", (93, 40))
    LSHIFT_DOWN = loadImage(f"{PATH}images/gui/icons/shift2.png", (93, 40))
    LSHIFT_ANDROID_UP = loadImage(f"{PATH}images/gui/buttons/dashUp.png", (60, 60))
    LSHIFT_ANDROID_DOWN = loadImage(f"{PATH}images/gui/buttons/dashDown.png", (60, 60))
    DEATH_UP = loadImage(f"{PATH}images/gui/icons/death.png", (40, 40))
    ATTENTION_UP = loadImage(f"{PATH}images/gui/icons/attention.png", (40, 40))
    STAR_UP = loadImage(f"{PATH}images/gui/icons/star.png", (40, 40))
    TIP_UP = loadImage(f"{PATH}images/gui/icons/tip.png", (200, 70))

    class Type(Enum):
        W = 1
        A = 2
        S = 3
        D = 4
        LSHIFT = 5
        LSHIFT_ANDROID = 6
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
        if GameInfo.GameInfo.BUILD_TYPE is GameInfo.BuildType.ANDROID:
            if type.value <= 4:
                return
            if type == Icons.Type.LSHIFT:
                type = Icons.Type.LSHIFT_ANDROID
                pos = pos[0] + 15, pos[1]

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
        if self.type is Icons.Type.LSHIFT_ANDROID:
            if Buttons.Buttons.dash or keyPressed[pygame.K_LSHIFT]:
                self.image = eval("Icons." + str(self.type)[5:] + "_DOWN")
            else:
                self.image = eval("Icons." + str(self.type)[5:] + "_UP")
            return


        if self.type.value > 100:
            return
        if self.type == Icons.Type.LSHIFT:
            typeStr = str(self.type)[5:]
        else:
            typeStr = (str(self.type)[5:]).lower()

        if eval("keyPressed[pygame.K_" + typeStr + "]"):
            self.image = eval("Icons." + str(self.type)[5:] + "_DOWN")
        else:
            self.image = eval("Icons." + str(self.type)[5:] + "_UP")


