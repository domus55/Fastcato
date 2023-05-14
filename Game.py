from Player import *
from Screen import *
from Camera import *
import InnerTimer


class Game:
    isRunning = True
    keyPressed = None

    def __init__(self):
        self._maxFps = 60
        self._clock = clock = pygame.time.Clock()
        LevelManager.LevelManager.Initialize()

    def update(self):
        InnerTimer.Timer.update()
        screenUpdate()
        LevelManager.LevelManager.player.update(Game.keyPressed)
        Camera.update(LevelManager.LevelManager.player) #must be after player update


    def render(self):
        screen.fill((0, 0, 0))
        LevelManager.LevelManager.player.render()
        ObstacleManager.ObstacleManager.renderAll()
        Block.Block.renderAll()
        screenRender()


    def delay(self):
        self._clock.tick(self._maxFps)


    def exit(self):
        pygame.quit()
