import os

import pygame

from Const import C_WHITE, FONT_SCORE_SIZE_DEFAULT, FONT_SCORE_SIZE_TITLE, C_BRIGHT_GREEN, SCREEN_WIDTH, C_GREEN
from Game_State import GameState
from Plane_Config import PLANES


class SelectionScreen:
    def __init__(self, window, mode=GameState.PLAYING):
        self.window = window
        self.mode = mode  # Salva o modo
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
        title_text = "ESCOLHA SEU AVIÃO" if self.mode == GameState.PLAYING else "PREPAREM-SE PARA O COMBATE"
        title = self.title_font.render(title_text, True, C_WHITE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
        self.window.blit(title, title_rect)

        spacing = 300
        start_x = (SCREEN_WIDTH // 2) - (spacing // 2) - 50
        font_instr = pygame.font.SysFont("Arial", 18, bold=True)

        for i, plane in enumerate(PLANES):
            x = start_x + i * spacing
            y = 250

            # Desenha a imagem da nave
            if self.plane_images[i]:
                self.window.blit(self.plane_images[i], (x, y))

            # SÓ MOSTRA A BORDA DE SELEÇÃO NO MODO SINGLE PLAYER
            if self.mode == GameState.PLAYING and i == self.selected:
                pygame.draw.rect(self.window, C_WHITE, (x - 10, y - 10, 120, 120), 3)

            # Nome do avião
            name_text = self.font.render(plane.name, True, C_WHITE)
            self.window.blit(name_text, (x + 10, y + 110))

            # --- LÓGICA DE COMANDOS CORRIGIDA ---
            if self.mode == GameState.PLAYING:
                # Se for Single Player, os comandos são iguais para os dois aviões (Setas/Ctrl)
                comandos = ["CONTROLES", "CTRL = Atirar", "SETAS = (↑ ↓ ← →)"]

            else:
                # Se for COOP ou VS, cada avião mostra seu respectivo dono
                if i == 0:
                    comandos = ["PLAYER 1", "CTRL = Atirar", "SETAS = Mover (↑ ↓ ← →)"]
                else:
                    comandos = ["PLAYER 2", "L = Atirar", "W, A, S, D = Mover"]

            for j, linha in enumerate(comandos,):
                cor = (255, 255, 0) if j == 0 else C_WHITE
                cmd_surf = font_instr.render(linha, True, cor)
                self.window.blit(cmd_surf, (x, y + 150 + (j * 25)))
                # --- FORA DO LOOP (Para desenhar o aviso de iniciar uma única vez) ---
                # Cria a variável de teste aqui
                msg_start = "Aperte ENTER para iniciar o jogo"

                # Renderiza com uma cor chamativa (ex: Verde ou Amarelo)
                start_surf = font_instr.render(msg_start, True, C_GREEN )

                # Centraliza exatamente no meio da largura da tela
                start_rect = start_surf.get_rect(centerx=SCREEN_WIDTH // 2, y=600)
                self.window.blit(start_surf, start_rect)

