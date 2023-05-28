class GameInfo:
    _sound = 6   #from 0 - 6
    _music = 6   #from 0 - 6

    NUMBER_OF_LEVELS = 9

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
        GameInfo.loadSettings()
        GameInfo.loadSave()

    @staticmethod
    def loadSave():
        error = False
        GameInfo.levelTime[0] = 1

        with open('save.txt') as f:
            for i in range(GameInfo.NUMBER_OF_LEVELS):
                try:
                    GameInfo.levelTime[i + 1] = float(f.readline())
                except:
                    GameInfo.levelTime[i + 1] = 0.0
                    error = True
        if error:
            GameInfo.saveSave()

    @staticmethod
    def saveSave():
        with open('save.txt', 'w') as f:
            for i in range(GameInfo.NUMBER_OF_LEVELS):
                f.write(f"{GameInfo.levelTime[i+1]}\n")

    @staticmethod
    def saveSettings():
        with open('game_settings.txt', 'w') as f:
            f.write(f"{GameInfo._sound}\n{GameInfo._music}")

    @staticmethod
    def loadSettings():
        with open('game_settings.txt') as f:
            try:
                GameInfo._sound = int(f.readline())
                GameInfo._music = int(f.readline())
            except:
                GameInfo._sound = 6
                GameInfo._music = 6
                GameInfo.saveSettings()

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

