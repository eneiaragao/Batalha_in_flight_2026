import os

import pygame
from Button import Button
from Const import C_WHITE, MENU_BUTTONS_CONFIG, SCREEN_WIDTH, SCREEN_HEIGHT, C_ROYAL_BLUE
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
        # Primeiro desenha a imagem de fundo carregada no __init__
        self.window.blit(self.menu_bg, (0, 0))

        title = self.title_font.render("AIR COMBAT", True, C_ROYAL_BLUE )
        self.window.blit(title, (500, 50))

        for button in self.buttons:
            button.draw(self.window)