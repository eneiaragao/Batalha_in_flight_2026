import os
import pygame

from Const import (C_WHITE, C_GRAY, INFO_POS, TITLE_SCORE_POS,
                   FONT_SCORE_SIZE_DEFAULT, FONT_SCORE_SIZE_TITLE,
                   TITLE_SCORE_TXT, TITLE_SCORE_TXT2, SCREEN_WIDTH,
                   SCREEN_HEIGHT, C_ROYAL_BLUE)  # Certifique-se de importar a cor azul aqui
from Game_State import GameState


class ScoreScreen:
    def __init__(self, window, database):
        self.window = window
        self.database = database
        self.font = pygame.font.SysFont(None, FONT_SCORE_SIZE_DEFAULT)
        self.title_font = pygame.font.SysFont(None, FONT_SCORE_SIZE_TITLE)

        # Carregar fundo da tela de score
        # Usei 'ScoreBg.png' assumindo que é o fundo da montanha da imagem 2
        try:
            path_bg = os.path.join(os.path.dirname(__file__), "..", "asset", "ScoreBg.png")
            self.menu_bg = pygame.image.load(path_bg).convert()
            self.menu_bg = pygame.transform.scale(self.menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Erro ao carregar fundo do score: {e}")
            # Fallback caso a imagem não exista
            self.menu_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.menu_bg.fill((20, 20, 20))  # Fundo escuro padrão

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT

            if event.type == pygame.KEYDOWN:
                return GameState.MENU

        return GameState.SCORE

    def draw(self):
        # 1. Desenha a imagem de fundo
        self.window.blit(self.menu_bg, (0, 0))

        # Configurações padronizadas das barras
        largura_barra = 500  # Aumentei um pouco para caber o título maior
        altura_barra = 60
        x_coord = (SCREEN_WIDTH // 2) - (largura_barra // 2)

        # 2. Desenha o Título "TOP SCORES" com fundo azul
        # Posição Y fixa para o título
        rect_titulo = pygame.Rect(x_coord, 30, largura_barra, altura_barra)
        pygame.draw.rect(self.window, C_ROYAL_BLUE, rect_titulo)

        title_surf = self.title_font.render(TITLE_SCORE_TXT, True, C_WHITE)
        title_rect = title_surf.get_rect(center=rect_titulo.center)
        self.window.blit(title_surf, title_rect)

        # 3. Busca e desenha os scores
        scores = self.database.get_top_scores()
        y_coord = 120  # Começa abaixo do título

        for name, score in scores:
            rect_bg = pygame.Rect(x_coord, y_coord, largura_barra, 45)  # Altura menor para a lista
            pygame.draw.rect(self.window, C_ROYAL_BLUE, rect_bg)

            text_surf = self.font.render(f"{name} - {score}", True, C_WHITE)
            text_rect = text_surf.get_rect(center=rect_bg.center)
            self.window.blit(text_surf, text_rect)

            y_coord += 55  # Espaçamento entre as linhas

        # 4. Desenha o rodapé "Pressione qualquer tecla..." com fundo azul
        # rodapé um pouco mais para baixo
        y_rodape = SCREEN_HEIGHT - 80
        rect_info = pygame.Rect(x_coord, y_rodape, largura_barra, 40)
        pygame.draw.rect(self.window, C_ROYAL_BLUE, rect_info)

        info_surf = self.font.render(TITLE_SCORE_TXT2, True, C_WHITE)  # Mudei para C_WHITE para destacar no azul
        info_rect = info_surf.get_rect(center=rect_info.center)
        self.window.blit(info_surf, info_rect)