class GameInfo:
    _sound = 6   #from 0 - 6
    _music = 6   #from 0 - 6

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
        return GameInfo._sound

    @staticmethod
    def getMusic():
        return GameInfo._music