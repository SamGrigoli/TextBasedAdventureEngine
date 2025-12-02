# TEXT ADVENTURE GAME CREATOR

## Getting Started (Plug and Play)

1. Extract **`TextGameCreator.zip`** somewhere easily accessible.
2. Run **`editor/GameEditor.exe`** to create or edit games.
3. Use **File → New Game** to create a new game.
4. Build your world by adding **rooms**, **items**, **enemies**, and **weapons**.
5. Save your game in the **`data`** folder.

---

## Playing a Game

1. Navigate to the **`engine`** folder in a terminal.
2. Run **`play.bat`** (Windows).
3. Enter the name of the game you want to play.
4. Enjoy!

---

## Folder Structure

```
editor/   → Contains the game editor
data/     → Your saved games go here
engine/   → Contains the game engine
```

---

## How to Build the Project

### Requirements
- `make`
- `g++` (version 17 or higher)
- `python` (version 3 or higher)

---

### Build Instructions

1. Ensure `make` is installed and `g++` is in your PATH.
2. Navigate to the **root directory** of the project.
3. Run:
   ```
   make
   ```
4. This will produce **`textadventure`** along with an example game.
5. *(Optional)* To package the game engine + editor, run:
   ```
   python package.py
   ```
6. Navigate to `TextGameCreator` and run either the **editor** or the **engine**.

---

## Notes / Troubleshooting

- If `.o` files or the `.exe` are not being created, you likely don’t have the correct version of `g++`.
- `make clean` will **not** work unless the `.exe` has already been created.
- **`TextGameCreator.zip`** is a fully-built, self-contained working version of the program.
