from Game import Game

game = Game()
while Game.isRunning:
    game.update()
    game.render()
    game.delay()

game.exit()
