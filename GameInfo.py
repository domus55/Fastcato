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
        return GameInfo._sound/6

    @staticmethod
    def getMusic():
        return GameInfo._music/6

    @staticmethod
    def save():
        with open('game_settings.txt', 'w') as f:
            f.write(f"{GameInfo._sound}\n{GameInfo._music}")

    @staticmethod
    def load():
        with open('game_settings.txt') as f:
            try:
                GameInfo._sound = int(f.readline())
                GameInfo._music = int(f.readline())
            except:
                GameInfo._sound = 6
                GameInfo._music = 6
                GameInfo.save()

