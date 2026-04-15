from enum import Enum

class GameState(Enum):
    MENU = 1
    SELECTION = 2
    PLAYING = 3  # Single Player
    COOP = 4     # NOVO: Modo Cooperativo
    VS = 5       # NOVO: Modo Versus
    SCORE = 6    # Ajustado o número
    EXIT = 7     # Ajustado o número