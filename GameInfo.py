from enum import Enum
import os.path

from ProjectCommon import PATH


class BuildType(Enum):
    WINDOWS = 0
    WEB = 1
    ANDROID = 2

class GameInfo:
    _sound = 6   #from 0 - 6
    _music = 6   #from 0 - 6

    BUILD_TYPE = BuildType.WINDOWS
    NUMBER_OF_LEVELS = 6
    levelTime = [0.0] * (NUMBER_OF_LEVELS + 1)

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
                except:
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
        except Exception:
            GameInfo._sound = 6
            GameInfo._music = 6
            GameInfo.saveSettings()

    @staticmethod
    def saveSettings():
        with open(f'{PATH}game_settings.txt', 'w') as f:
            f.write(f"{GameInfo._sound}\n{GameInfo._music}")

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

