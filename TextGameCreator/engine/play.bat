@echo off
echo Text Adventure Game Launcher
echo ============================
echo.

:: Check if games directory exists
if not exist "textgame\data\" (
    echo Error: games folder not found!
    echo Please run the editor first to create a game.
    pause
    exit /b 1
)

:: List available games
echo Available games:
echo.
set count=0
for /d %%G in ("textgame\data\*") do (
    set /a count+=1
    echo [!count!] %%~nxG
)

if %count%==0 (
    echo No games found!
    echo Please create a game using the editor first.
    pause
    exit /b 1
)

echo.
set /p gamename="Enter the name of the game you want to play: "

if not exist "textgame\data\%gamename%\" (
    echo Error: Game '%gamename%' not found!
    pause
    exit /b 1
)

:: Run the game
textgame.exe "textgame\data\%gamename%"

pause