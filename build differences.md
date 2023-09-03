# Building
Currently, there are 3 types of build: windows, web and android.
To change version go to `GameInfo.py` and change `GameInfo.BUILD_TYPE`

## Windows
**Windows** build is made using the Pyinstaller library and it is a full version of the game.

**diff**:<br>
* none

**build**:<br>
* `pyinstaller main.py --windowed --onefile --icon=images/gameIcon.ico --name "Fastcato"`

![image](https://github.com/domus55/Python-Game/blob/main/images/github/windows.png)

## Web
**Web** is made using the pygbag library and has simplified graphic.

**diff**: <br>
* no multi layer level background,
* no trees render,
* no background refresh in main menu,
* there is no sound 3 seconds after using dash
* times are saved in localStorage instead of txt file.

**testing**:
1. `cd ..`
2. `pygbag [game_folder_name]`
3. `in browser open http://localhost:8000 or http://localhost:8000/#debug for log messages`

**build**:
1. `cd ..`
2. `pygbag [game_folder_name]`
3. `build will be in [game_folder_name]/build/web`

![image](https://github.com/domus55/Python-Game/blob/main/images/github/web.png)

## Android
**Android** is made using buildozer library and also has simplified graphic
**diff**:
* no multi layer level background,
* no trees render.

**testing**:
* `buildozer -v android debug deploy run logcat`
* `buildozer -v android debug deploy run logcat >> output.txt`

**build**:
1. `buildozer -v android release`
2. `cd bin`
3. `change *.aab file name to Fastcato.aab`
4. `jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 -storepass [password] -keystore fastcato.keystore Fastcato.aab fastcato`

![image](https://github.com/domus55/Python-Game/blob/main/images/github/android.png)