import pygame
from Game_State import GameState

class ScoreScreen:
    def __init__(self, window, database):
        self.window = window
        self.database = database
        self.font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 60)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT

            if event.type == pygame.KEYDOWN:
                return GameState.MENU

        return GameState.SCORE

    def draw(self):
        self.window.fill((20, 20, 20))

        title = self.title_font.render("TOP SCORES", True, (255, 255, 255))
        self.window.blit(title, (250, 50))

        scores = self.database.get_top_scores()

        y = 150
        for name, score in scores:
            text = self.font.render(f"{name} - {score}", True, (255, 255, 255))
            self.window.blit(text, (300, y))
            y += 50

        info = self.font.render("Pressione qualquer tecla para voltar", True, (200, 200, 200))
        self.window.blit(info, (180, 500))