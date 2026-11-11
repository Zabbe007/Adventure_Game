# Adventure Game

A text-based, choose-your-own-adventure game with a purple-themed Tkinter GUI. You wake up in a dark forest and every choice you make shapes whether you escape or meet a grisly end.

## Features

- Branching story with multiple endings (some good, some... not)
- Simple GUI with a main menu and a scrolling game window
- Save and load support, one save file per player
- Random chance in combat: attacks succeed 60% of the time
- Typewriter-style text for atmosphere

## Requirements

- Python 3.x
- Tkinter (included with most Python installs; on some Linux systems install `python3-tk`)

No other packages are needed.

## Files

| File | Purpose |
| --- | --- |
| `adventure_GUI.py` | The GUI and the program entry point. Run this one. |
| `adventure_game.py` | The game logic, story, and save/load system. |

Keep both files in the same folder.

## How to Run

```bash
python adventure_GUI.py
```

From the menu window, choose:

- **Start New Game** to begin a fresh adventure
- **Load Game** to continue from a saved file
- **Exit** to quit

## How to Play

1. Enter a name when prompted (letters only, or leave it blank to play as "Player").
2. Read the story text, then type the number of your choice and press **Enter**.
3. Every choice menu includes an option to exit the game.

## Saving and Loading

The game saves automatically after every choice. Saves are written to the folder you run the game from as `save_<name>.json` and record your name, choices, and outcomes.

To load a save, pick **Load Game**, then enter the number of the save you want (or `0` to go back to the menu).

## Notes

- Game text is sent to the GUI by redirecting `stdout`, and your input is passed back to the game through a queue. This keeps the game logic separate from the window.
- Loading a save currently shows a recap of your last few choices and returns to the main menu rather than resuming mid-story.
  
- <img width="998" height="829" alt="adventure_game" src="https://github.com/user-attachments/assets/20b088ff-83d3-48b9-81f0-f6e68feb1f9b" />
