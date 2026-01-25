import os.path
from enum import Enum

import pygame

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
    level_time = [0.0] * (NUMBER_OF_LEVELS + 1)
    fullScreen = 0      # 0 - False, 1 - True

    HUD_SCALE = 1.5 if BUILD_TYPE is BuildType.ANDROID else 1

    # Times for gold and silver
    # TROPHY_TIMES[3][1] returns time on 3rd level for silver, TROPHY_TIMES[1][0] returns time on first level for gold
    TROPHY_TIMES = [[0, 0], [30, 40], [34, 40], [31, 35], [43, 47], [51, 55], [55, 57]]
                            #1           2           3       4       5           6
    @staticmethod
    def sound_up():
        if GameInfo._sound < 6:
            GameInfo._sound += 1

    @staticmethod
    def sound_down():
        if GameInfo._sound > 0:
            GameInfo._sound -= 1

    @staticmethod
    def music_up():
        if GameInfo._music < 6:
            GameInfo._music += 1

    @staticmethod
    def music_down():
        if GameInfo._music > 0:
            GameInfo._music -= 1

    @staticmethod
    def get_sound():
        return GameInfo._sound/6

    @staticmethod
    def get_music():
        return GameInfo._music/6

    @staticmethod
    def load():
        if GameInfo.BUILD_TYPE == BuildType.WEB:
            GameInfo.load_time_from_web()
        else:
            GameInfo.load_time_dat()

        GameInfo.load_settings()

    @staticmethod
    def load_time_from_web():
        GameInfo.level_time[0] = 1
        if __import__("sys").platform == "emscripten":
            from platform import window
            error = False
            for i in range(GameInfo.NUMBER_OF_LEVELS):
                time = window.localStorage.getItem(f"level{i + 1}")
                if time is None:
                    GameInfo.level_time[i + 1] = 0
                    error = True
                else:
                    GameInfo.level_time[i + 1] = float(time)
            if error:
                GameInfo.save_time_to_web()

    @staticmethod
    def load_time_dat():
        error = False
        GameInfo.level_time[0] = 1

        fileExists = os.path.exists(f'{PATH}save.dat')
        if not fileExists:
            GameInfo.save_time()

        with open(f'{PATH}save.dat', 'rb') as f:
            for i in range(GameInfo.NUMBER_OF_LEVELS):
                try:
                    line = f.readline().strip()
                    if not line:
                        print("ValueError")
                        raise ValueError

                    original_bytes = bytes.fromhex(line.decode('utf-8'))
                    GameInfo.level_time[i + 1] = float(original_bytes.decode('utf-8'))

                except (ValueError, TypeError, IndexError):
                    print("Error when loading a save!\n")
                    GameInfo.level_time[i + 1] = 0.0
                    error = True
        if error:
            GameInfo.save_time()

    @staticmethod
    def save_time():
        if GameInfo.BUILD_TYPE == BuildType.WEB:
            GameInfo.save_time_to_web()
        else:
            GameInfo.save_time_dat()

    @staticmethod
    def save_time_to_web():
        if __import__("sys").platform == "emscripten":
            from platform import window

            for i in range(GameInfo.NUMBER_OF_LEVELS):
                window.localStorage.setItem(f"level{i + 1}", GameInfo.level_time[i + 1])

    @staticmethod
    def save_time_dat():
        with open(f'{PATH}save.dat', 'wb') as f:
            for i in range(GameInfo.NUMBER_OF_LEVELS):
                s = str(GameInfo.level_time[i + 1])
                b = s.encode("utf-8")
                hx = b.hex()
                f.write(hx.encode("utf-8") + b"\n")

    @staticmethod
    def load_settings():
        try:
            with open(f'{PATH}game_settings.txt') as f:
                GameInfo._sound = int(f.readline())
                GameInfo._music = int(f.readline())
                GameInfo.fullScreen = int(f.readline())
        except Exception:
            GameInfo._sound = 6
            GameInfo._music = 6
            # if player's screen is 1600x900 or bigger play the game in window. Otherwise, use fullscreen
            display_info = pygame.display.get_desktop_sizes()
            if len(display_info) == 0:
                GameInfo.fullScreen = 0
            else:
                main_monitor = display_info[0]
                if main_monitor[0] >= 1600 and main_monitor[1] >= 900:
                    GameInfo.fullScreen = 0
                else:
                    GameInfo.fullScreen = 1
            GameInfo.save_settings()

    @staticmethod
    def save_settings():
        with open(f'{PATH}game_settings.txt', 'w') as f:
            f.write(f"{GameInfo._sound}\n{GameInfo._music}\n{int(GameInfo.fullScreen)}")

    @staticmethod
    def str_level_time(level_nr):
        strr = ""
        time = GameInfo.level_time[level_nr]

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
    def get_trophy(level, time=-1):
        if time == -1:
            time = GameInfo.level_time[level]

        if time > 60 or time == 0:
            return 0

        if time <= GameInfo.TROPHY_TIMES[level][0]:
            return 3
        elif time <= GameInfo.TROPHY_TIMES[level][1]:
            return 2
        else:
            return 1
