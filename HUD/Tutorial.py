import Player
import pygame

import Game
import GameInfo
from HUD import Deadline, Buttons
from Screen import screen


class Tutorial:
    rightPanel = pygame.Surface((400, 900), pygame.SRCALPHA, 32)

    showHint = True

    @staticmethod
    def render():
        # logic part
        if Game.Game.keyPressed is None or GameInfo.GameInfo.BUILD_TYPE is not GameInfo.BuildType.ANDROID or GameInfo.GameInfo.levelTime[1] != 0:
            return

        if Buttons.Buttons.right or Game.Game.keyPressed[pygame.K_d]:
            Tutorial.showHint = False

        # render part
        alpha1 = abs(100 - (Deadline.Deadline.time()) * 25 % 100)
        alpha2 = abs(100 - (Deadline.Deadline.time() + 2) * 25 % 100)
        if Tutorial.showHint or (Player.Player.getInstance().pos[0] < 900 and Deadline.Deadline.time() >= 8):
            if Deadline.Deadline.time() < 4:
                return
            Tutorial._draw_circle_alpha(Tutorial.rightPanel, (1200, 0), (255, 255, 255, alpha1), (200, 450), 5 * abs(100 - alpha1))
            if (Tutorial.showHint and Deadline.Deadline.time() > 6) or (not Tutorial.showHint and Deadline.Deadline.time() >= 10):
                Tutorial._draw_circle_alpha(Tutorial.rightPanel, (1200, 0), (255, 255, 255, alpha2), (200, 450), 5 * abs(100 - alpha2))

    @staticmethod
    def _draw_circle_alpha(panel, panelPos, color, center, radius):
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)
        panel.fill((0, 0, 0, 0))
        panel.blit(shape_surf, target_rect)
        screen.blit(panel, panelPos)
