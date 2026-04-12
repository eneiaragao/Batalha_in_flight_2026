from enum import Enum

class GameState(Enum):
    MENU = 1
    SELECTION = 2
    PLAYING = 3
    SCORE = 4
    EXIT = 5