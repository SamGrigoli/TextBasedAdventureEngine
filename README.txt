TEXT ADVENTURE GAME CREATOR
============================

GETTING STARTED (PLUG AND PLAY):
1. Extract the TextGameCreator.zip somewhere easily accessible 
2. Run "editor/GameEditor.exe" to create or edit games
3. Use File > New Game to create a new game
4. Build your world by adding rooms, items, enemies, and weapons
5. Save your game in the "data" folder

PLAYING A GAME:
1. Navigate to the "engine" folder in a terminal
2. Run "play.bat" (Windows)
3. Enter the name of the game you want to play
4. Enjoy!

FOLDER STRUCTURE:
- editor/ : Contains the game editor
- data/  : Your saved games go here
- engine/ : Contains the game engine

REQUIREMENTS:
- Windows 10 or later (for Windows version)
- No additional software required

HOW TO BUILD PROJECT:
1. Make sure you have "make" installed and g++ (17 or higher) is in your PATH or is easily accessible
2. Make sure you navigate to the root of the projects directory
3. Once in root directory simply run make
4. This should create a file named textgame.exe to run
5. From here you can type in path to the game data folder you would like to play

Things to note when building:
- If all of your .o files or .exe are not being created it is likely that you do not have the correct version of g++.
- If you want to run "make clean" it will not work unless the .exe is already created.
- The folders labled TextGameCreator and TextGameCreator.zip are full builds of the program that work independently.
   Running these should always work but have nothing to do with the build process.


