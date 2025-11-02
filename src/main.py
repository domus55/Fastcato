import asyncio

from src.game import Game


async def main():
    game = Game()
    while Game.isRunning:
        game.update()
        game.render()
        await asyncio.sleep(0)
        game.delay()

    game.exit()

asyncio.run(main())
