import os

import pygame

from Const import C_WHITE, FONT_SCORE_SIZE_DEFAULT, FONT_SCORE_SIZE_TITLE, C_BRIGHT_GREEN, SCREEN_WIDTH
from Game_State import GameState
from Plane_Config import PLANES


class SelectionScreen:
    def __init__(self, window):
        self.window = window
        self.selected = 0
        self.font = pygame.font.SysFont(None, FONT_SCORE_SIZE_DEFAULT)
        self.title_font = pygame.font.SysFont(None, FONT_SCORE_SIZE_TITLE)
        # Pré-carrega as imagens para não travar o draw
        self.plane_images = []
        import os
        base_path = os.path.dirname(__file__)
        for plane in PLANES:
            try:
                path = os.path.join(base_path, "..", "asset", f"{plane.asset_name}.png")
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (100, 100))
                self.plane_images.append(img)
            except:
                self.plane_images.append(None)
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT, None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(PLANES)

                if event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(PLANES)

                if event.key == pygame.K_RETURN:
                    return GameState.PLAYING, PLANES[self.selected]

                if event.key == pygame.K_ESCAPE:
                    return GameState.MENU, None

        return GameState.SELECTION, None

    def draw(self):

        self.window.fill((20, 20, 20))

        # 1. Renderiza o texto
        title = self.title_font.render("ESCOLHA SEU AVIÃO", True, C_WHITE)

        # 2. Obtém o retângulo do texto para calcular o centro
        title_rect = title.get_rect()

        # 3. Define o centro do retângulo como o centro da largura da tela (SCREEN_WIDTH)
        title_rect.centerx = SCREEN_WIDTH // 2
        title_rect.y = 50  # Mantém a altura no topo

        # 4. Desenha usando o retângulo calculado
        self.window.blit(title, title_rect)

        # --- Lógica para Centralizar as Naves ---
        spacing = 150  # Espaço entre o início de cada nave
        total_group_width = len(PLANES) * spacing
        # Calcula onde deve começar o primeiro avião para que o grupo fique no meio
        start_x = (SCREEN_WIDTH // 2) - (total_group_width // 2) + 25

        for i, plane in enumerate(PLANES):
            x = start_x + i * spacing
            y = 250

            base_path = os.path.dirname(__file__)
            img_path = os.path.join(base_path, "..", "asset", f"{plane.asset_name}.png")

            try:
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (100, 100))
                self.window.blit(img, (x - 10, y - 10))
            except:
                pygame.draw.rect(self.window, C_BRIGHT_GREEN, (x, y, 80, 80))

            # Borda de seleção
            if i == self.selected:
                pygame.draw.rect(self.window, C_WHITE, (x - 15, y - 15, 110, 110), 3)

            # Nome do avião (também centralizado embaixo da imagem)
            name_text = self.font.render(plane.name, True, C_WHITE)
            name_rect = name_text.get_rect(centerx=x + 40, y=y + 100)
            self.window.blit(name_text, name_rect)