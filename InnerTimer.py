import datetime

class Timer:
    _prevTime = None

    # Time in ms from previous frame, it's used to update objects
    deltaTime = 0

    @staticmethod
    def update():
        if Timer._prevTime is None:
            Timer._prevTime = datetime.datetime.now()
        Timer.deltaTime = ((datetime.datetime.now() - Timer._prevTime).microseconds) / 1000
        Timer._prevTime = datetime.datetime.now()


    _framesThisSecond = 0
    _lastSecond = 0

    @staticmethod
    def showFps():
        if Timer._lastSecond == datetime.datetime.now().second:
            Timer._framesThisSecond += 1
        else:
            Timer._lastSecond = datetime.datetime.now().second
            if Timer._framesThisSecond is not 0:
                print(f"FPS: {Timer._framesThisSecond}")
            Timer._framesThisSecond = 0
