import pygame
from Game_State import GameState
from Plane_Config import PLANES


class SelectionScreen:
    def __init__(self, window):
        self.window = window
        self.selected = 0

        self.font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 60)

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
        import os
        self.window.fill((20, 20, 20))

        title = self.title_font.render("ESCOLHA SEU AVIÃO", True, (255, 255, 255))
        self.window.blit(title, (180, 50))

        for i, plane in enumerate(PLANES):
            x = 200 + i * 150
            y = 250

            # 1. Monta o caminho da imagem do avião
            base_path = os.path.dirname(__file__)
            img_path = os.path.join(base_path, "..", "asset", f"{plane.asset_name}.png")

            try:
                # 2. Carrega e redimensiona a imagem para a tela de seleção
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (100, 100))  # Um pouco maior que o quadrado

                # 3. Desenha a imagem na tela
                self.window.blit(img, (x - 10, y - 10))
            except:
                # Caso a imagem falhe, desenha o quadrado verde de segurança
                pygame.draw.rect(self.window, (0, 200, 0), (x, y, 80, 80))

            # 4. Desenha a borda de seleção ao redor da nave selecionada
            if i == self.selected:
                pygame.draw.rect(self.window, (255, 255, 255), (x - 15, y - 15, 110, 110), 3)

            name_text = self.font.render(plane.name, True, (255, 255, 255))
            self.window.blit(name_text, (x, y + 100))