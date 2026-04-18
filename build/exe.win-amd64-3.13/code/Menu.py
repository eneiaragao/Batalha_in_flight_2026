import os

import pygame
from Button import Button
from Const import C_WHITE, MENU_BUTTONS_CONFIG, SCREEN_WIDTH, SCREEN_HEIGHT, C_SKY_BLUEP, \
    C_SKY_BLUEP2
from Game_State import GameState

class Menu:
    def __init__(self, window):
        self.window = window
        # Carrega fundo do menu
        path_bg = os.path.join(os.path.dirname(__file__), "..", "asset", "Background.png")
        self.menu_bg = pygame.image.load(path_bg).convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (SCREEN_WIDTH,SCREEN_HEIGHT))

        # Tocar música do menu
        path_music = os.path.join(os.path.dirname(__file__), "..", "asset", "Menu.mp3")
        pygame.mixer.music.load(path_music)
        pygame.mixer.music.play(-1)

        self.buttons = [Button(*config) for config in MENU_BUTTONS_CONFIG]

        self.title_font = pygame.font.SysFont(None, 60)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT

            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):

                    if i == 0:
                        return GameState.PLAYING  # Single
                    elif i == 1:
                        return GameState.COOP  # Modo cooperative
                    elif i == 2:
                        return GameState.VS  # Modo competitivo
                    elif i == 3:
                        return GameState.SCORE
                    elif i == 4:
                        return GameState.EXIT

        return GameState.MENU

    def draw(self):
        # 1. Desenha o fundo
        self.window.blit(self.menu_bg, (0, 0))

        # 2. Configurações da Sombra e Texto
        texto_str = "BATTLE IN FLIGHT 2026"
        posicao_x = 400
        posicao_y = 50
        deslocamento = 3  # Quantidade de pixels que a sombra "foge" do texto

        # 3. Desenha a SOMBRA primeiro
        shadow = self.title_font.render(texto_str, True, C_SKY_BLUEP2)
        self.window.blit(shadow, (posicao_x + deslocamento, posicao_y + deslocamento))

        # 4. Desenha o TEXTO PRINCIPAL por cima
        title = self.title_font.render(texto_str, True, C_SKY_BLUEP)
        self.window.blit(title, (posicao_x, posicao_y))

        for button in self.buttons:
            button.draw(self.window)