DUNGEON ESCAPE
=============

A small roguelike made with Pygame Zero.
Collect every coin in the dungeon, avoid the monsters and reach the exit ladder.


LIBRARIES USED
--------------
- Pygame Zero (pgzero)
- math
- random
(pygame itself is not used; only the Rect class is allowed.)


HOW TO RUN
----------
1. Install Pygame Zero:
       pip install pgzero
2. From the project folder, start the game:
       cd src
       python main.py
   or:
       pgzrun src/main.py


CONTROLS
--------
Arrow keys / WASD : move
ESC               : pause / resume
Mouse             : menu buttons


PROJECT STRUCTURE
-----------------
src/main.py       entry point, Pygame Zero hooks and screens
src/settings.py   game-wide constants
src/images/       sprites (pre-scaled 3x for Pygame Zero)
src/sounds/       sound effects (.wav)
src/music/        background music (.ogg)


ASSET CREDITS (all CC0 / public domain)
---------------------------------------
- Sprites: "16x16 DungeonTileset II" by 0x72
  https://0x72.itch.io/dungeontileset-ii
- Sound effects: "The Essential Retro Video Game Sound Effects Collection
  [512 sounds]" by Juhani Junkala
  https://opengameart.org/content/512-sound-effects-8-bit-style
- Music: "Dungeon Ambience" by yd
  https://opengameart.org/content/dungeon-ambience
