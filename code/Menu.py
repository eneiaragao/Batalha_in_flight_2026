import os

import pygame
from Button import Button
from Game_State import GameState

class Menu:
    def __init__(self, window):
        self.window = window
        # Carregar fundo do menu
        path_bg = os.path.join(os.path.dirname(__file__), "..", "asset", "Background.png")
        self.menu_bg = pygame.image.load(path_bg).convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (1240, 650))

        # Tocar música do menu
        path_music = os.path.join(os.path.dirname(__file__), "..", "asset", "Menu.mp3")
        pygame.mixer.music.load(path_music)
        pygame.mixer.music.play(-1)

        self.buttons = [
            Button("Player 1", 300, 150, 200, 50),
            Button("2 Players Coop", 300, 220, 200, 50),
            Button("2 Players VS", 300, 290, 200, 50),
            Button("Score", 300, 360, 200, 50),
            Button("Exit", 300, 430, 200, 50),
        ]

        self.title_font = pygame.font.SysFont(None, 60)

    def run(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return GameState.EXIT

            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):

                    if i == 0:
                        return GameState.PLAYING
                    elif i == 1:
                        print("Modo Coop")
                    elif i == 2:
                        print("Modo VS")
                    elif i == 3:
                        return GameState.SCORE
                    elif i == 4:
                        return GameState.EXIT

        return GameState.MENU

    def draw(self):
        # Primeiro desenha a imagem de fundo carregada no __init__
        self.window.blit(self.menu_bg, (0, 0))

        # Remova ou comente o window.fill para não cobrir o fundo
        # self.window.fill((30, 30, 30))

        title = self.title_font.render("AIR COMBAT", True, (255, 255, 255))
        self.window.blit(title, (250, 50))

        for button in self.buttons:
            button.draw(self.window)