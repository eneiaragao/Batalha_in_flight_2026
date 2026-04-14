import pygame

from Const import C_WHITE, C_GRAY, INFO_POS, TITLE_SCORE_POS, FONT_SCORE_SIZE_DEFAULT, FONT_SCORE_SIZE_TITLE, \
    TITLE_SCORE_TXT, TITLE_SCORE_TXT2
from Game_State import GameState

class ScoreScreen:
    def __init__(self, window, database):
        self.window = window
        self.database = database
        self.font = pygame.font.SysFont(None, FONT_SCORE_SIZE_DEFAULT)
        self.title_font = pygame.font.SysFont(None, FONT_SCORE_SIZE_TITLE)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT

            if event.type == pygame.KEYDOWN:
                return GameState.MENU

        return GameState.SCORE

    def draw(self):
        self.window.fill((20, 20, 20))

        title = self.title_font.render(TITLE_SCORE_TXT, True, C_WHITE)
        self.window.blit(title, TITLE_SCORE_POS)

        scores = self.database.get_top_scores()

        y = 150
        for name, score in scores:
            text = self.font.render(f"{name} - {score}", True, C_WHITE)
            self.window.blit(text, (300, y))
            y += 50

        info = self.font.render(TITLE_SCORE_TXT2, True, C_GRAY)
        self.window.blit(info, INFO_POS)