import os.path
from enum import Enum

PATH = os.path.abspath('') + '/'


class BuildType(Enum):
    WINDOWS = 0
    WEB = 1
    ANDROID = 2


class GameInfo:
    _sound = 6   # from 0 to 6
    _music = 6   # from 0 to 6

    BUILD_TYPE = BuildType.WINDOWS
    NUMBER_OF_LEVELS = 6
    levelTime = [0.0] * (NUMBER_OF_LEVELS + 1)
    fullScreen = 0      # 0 - False, 1 - True

    HUD_SCALE = 1.5 if BUILD_TYPE is BuildType.ANDROID else 1

    # Times for gold and silver
    # TROPHY_TIMES[3][1] returns time on 3rd level for silver, TROPHY_TIMES[1][0] returns time on first level for gold
    TROPHY_TIMES = [[0, 0], [30, 40], [36, 44], [32, 40], [43, 50], [52, 56], [55, 57]]

    @staticmethod
    def soundUp():
        if GameInfo._sound < 6:
            GameInfo._sound += 1

    @staticmethod
    def soundDown():
        if GameInfo._sound > 0:
            GameInfo._sound -= 1

    @staticmethod
    def musicUp():
        if GameInfo._music < 6:
            GameInfo._music += 1

    @staticmethod
    def musicDown():
        if GameInfo._music > 0:
            GameInfo._music -= 1

    @staticmethod
    def getSound():
        return GameInfo._sound/6

    @staticmethod
    def getMusic():
        return GameInfo._music/6

    @staticmethod
    def load():
        if GameInfo.BUILD_TYPE == BuildType.WEB:
            GameInfo.loadTimeFromWeb()
        else:
            GameInfo.loadTimeTxt()

        GameInfo.loadSettings()

    @staticmethod
    def loadTimeFromWeb():
        GameInfo.levelTime[0] = 1
        if __import__("sys").platform == "emscripten":
            from platform import window
            error = False
            for i in range(GameInfo.NUMBER_OF_LEVELS):
                time = window.localStorage.getItem(f"level{i + 1}")
                if time is None:
                    GameInfo.levelTime[i + 1] = 0
                    error = True
                else:
                    GameInfo.levelTime[i + 1] = float(time)
            if error:
                GameInfo.saveTimeToWeb()

    @staticmethod
    def loadTimeTxt():
        error = False
        GameInfo.levelTime[0] = 1

        fileExists = os.path.exists(f'{PATH}save.txt')
        if not fileExists:
            GameInfo.saveTime()

        with open(f'{PATH}save.txt') as f:
            for i in range(GameInfo.NUMBER_OF_LEVELS):
                try:
                    GameInfo.levelTime[i + 1] = float(f.readline())
                except (ValueError, TypeError,IndexError):
                    GameInfo.levelTime[i + 1] = 0.0
                    error = True
        if error:
            GameInfo.saveTime()

    @staticmethod
    def saveTime():
        if GameInfo.BUILD_TYPE == BuildType.WEB:
            GameInfo.saveTimeToWeb()
        else:
            GameInfo.saveTimeTxt()

    @staticmethod
    def saveTimeToWeb():
        if __import__("sys").platform == "emscripten":
            from platform import window

            for i in range(GameInfo.NUMBER_OF_LEVELS):
                window.localStorage.setItem(f"level{i + 1}", GameInfo.levelTime[i+1])

    @staticmethod
    def saveTimeTxt():
        with open(f'{PATH}save.txt', 'w') as f:
            for i in range(GameInfo.NUMBER_OF_LEVELS):
                f.write(f"{GameInfo.levelTime[i+1]}\n")

    @staticmethod
    def loadSettings():
        try:
            with open(f'{PATH}game_settings.txt') as f:
                GameInfo._sound = int(f.readline())
                GameInfo._music = int(f.readline())
                GameInfo.fullScreen = int(f.readline())
        except Exception:
            GameInfo._sound = 6
            GameInfo._music = 6
            GameInfo.fullScreen = 0
            GameInfo.saveSettings()

    @staticmethod
    def saveSettings():
        with open(f'{PATH}game_settings.txt', 'w') as f:
            f.write(f"{GameInfo._sound}\n{GameInfo._music}\n{GameInfo.fullScreen}")

    @staticmethod
    def strLevelTime(levelNr):
        strr = ""
        time = GameInfo.levelTime[levelNr]

        seconds = int(time)
        minutes = seconds // 60
        ms = int(time * 1000 % 1000)

        seconds = seconds % 60
        if minutes <= 9:
            strr += '0'

        strr += str(minutes)
        strr += ':'

        if seconds <= 9:
            strr += '0'
        strr += str(seconds)
        strr += '.'

        if ms <= 99:
            strr += '0'
            if ms <= 9:
                strr += '0'

        strr += str(ms)

        return strr

    '''0 - none, 1 - bronze, 2 - silver, 3 - gold'''
    @staticmethod
    def getTrophee(level, time=-1):
        if time == -1:
            time = GameInfo.levelTime[level]

        if time > 60 or time == 0:
            return 0

        if time <= GameInfo.TROPHY_TIMES[level][0]:
            return 3
        elif time <= GameInfo.TROPHY_TIMES[level][1]:
            return 2
        else:
            return 1
