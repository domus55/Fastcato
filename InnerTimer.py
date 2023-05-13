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
