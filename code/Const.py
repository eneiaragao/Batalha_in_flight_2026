# Cores (Padrão RGB)
C_GREEN = (0, 255, 0)
C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)
C_GRAY = (200, 200, 200)
C_BRIGHT_GREEN = (0, 200, 0)
C_ROYAL_BLUE = (100, 100, 255)
C_SKY_BLUE = (150, 150, 255)

#E
# Sons
EXPLOSION_SOUND = "Som_explosao.mp3"  # ARQUIVO EXPLOSÃO
EXPLOSION_VOLUME= 0.6
#F
FONT_SCORE_SIZE_DEFAULT = 40  # Tamanhos de Fonte
FONT_SCORE_SIZE_TITLE = 60  # Tamanhos de Fonte

#I
# Posições de Texto
INFO_POS = (180, 500)

# Dimensões da Tela
SCREEN_WIDTH = 1240
SCREEN_HEIGHT = 650
SPAWN_X_MAX = SCREEN_WIDTH - 50  # 1190 era SCREEN_WIDTH (1240) menos a largura do inimigo (50)  Limites de Spawn (Inimigos)
SCROLL_SPEED = 2  # Configurações do Cenário
SBG_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)  # Configurações do Cenário
SUBTEXT_POS = (300, 350)  # Posições de Texto (X, Y)
SCORE_TO_POWER_UP = 500  # Valor para ativar o Power-Up tiros duplos
SCORE_POWER_UP_TIME=1080
SPEED_SHOOT=15 #VELOCIDADE DO TIRO NORMAL
SPEED_SHOOT_POWER=23 #VELOCIDADE DO TIRO POWER

#P
PLAYER_START_X = 600  # Configurações do Player(posição na tela player1)
PLAYER_START_Y = 500  # Configurações do Player(posição na tela player2)
POINTS_PER_LEVEL = 200   # Regras de Jogo para cada fase
# Tamanhos de Sprites
PLAYER_SIZE = (10, 20)  #  tamanho dO TIRO:

#T
TITLE_SCORE_POS = (250, 50)  # Posições de Títulos
TITLE_SCORE_TXT = "TOP SCORES"  # Conteúdo do Texto
TITLE_SCORE_TXT2 = "Pressione qualquer tecla para voltar"  # Conteúdo do Texto
#v
VICTORY_TEXT_POS = (350, 250)  # Posições de Texto (X, Y)
LIVE_PLAYERS=4


# --- CONFIGURAÇÕES DE BOTÕES DO MENU ---
BTN_WIDTH = 200
BTN_HEIGHT = 50
BTN_X_CENTER = (SCREEN_WIDTH // 2) - (BTN_WIDTH // 2)  # Centralizado dinamicamente

# Cada tupla: (Texto, X, Y, Largura, Altura)
MENU_BUTTONS_CONFIG = [
    ("Player 1", BTN_X_CENTER, 150, BTN_WIDTH, BTN_HEIGHT),
    ("2 Players Coop", BTN_X_CENTER, 220, BTN_WIDTH, BTN_HEIGHT),
    ("2 Players VS", BTN_X_CENTER, 290, BTN_WIDTH, BTN_HEIGHT),
    ("Score", BTN_X_CENTER, 360, BTN_WIDTH, BTN_HEIGHT),
    ("Exit", BTN_X_CENTER, 430, BTN_WIDTH, BTN_HEIGHT),
]
