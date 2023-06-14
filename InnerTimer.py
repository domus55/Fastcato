import datetime


class InnerTime:
    _prevTime = None

    # Time in ms from previous frame, it's used to update objects
    deltaTime = 0

    @staticmethod
    def update():
        if InnerTime._prevTime is None:
            InnerTime._prevTime = datetime.datetime.now()
        InnerTime.deltaTime = (datetime.datetime.now() - InnerTime._prevTime).microseconds / 1000
        if InnerTime.deltaTime > 125:
            InnerTime.deltaTime = 0
        InnerTime._prevTime = datetime.datetime.now()


    _framesThisSecond = 0
    _lastSecond = 0

    @staticmethod
    def showFps():
        if InnerTime._lastSecond == datetime.datetime.now().second:
            InnerTime._framesThisSecond += 1
        else:
            InnerTime._lastSecond = datetime.datetime.now().second
            if InnerTime._framesThisSecond is not 0:
                print(f"FPS: {InnerTime._framesThisSecond}")
            InnerTime._framesThisSecond = 0
