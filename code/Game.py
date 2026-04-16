import pygame
import os
from Game_State import GameState
from Level import Level
from Menu import Menu
from Score_Screen import ScoreScreen
from Selection_Screen import SelectionScreen
from Const import SCREEN_WIDTH, SCREEN_HEIGHT
from Plane_Config import PLANES
from database import Database


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("BATTLE IN FLIGHT 2026")

        self.database = Database()
        self.selection_screen = SelectionScreen(self.window)
        self.score_screen = ScoreScreen(self.window, self.database)
        self.menu = Menu(self.window)

        self.selected_plane = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.level = None

    def run(self):
        while self.running:
            self.clock.tick(60)

            # --- ESTADO: MENU PRINCIPAL ---
            if self.state == GameState.MENU:
                new_state = self.menu.run()
                self.menu.draw()

                if new_state == GameState.PLAYING:
                    self.state = GameState.SELECTION
                    self.selection_screen.mode = GameState.PLAYING
                elif new_state in [GameState.COOP, GameState.VS]:
                    self.state = GameState.SELECTION
                    self.selection_screen.mode = new_state  # COOP ou VS
                elif new_state == GameState.SCORE:
                    self.state = GameState.SCORE
                elif new_state == GameState.EXIT:
                    self.running = False

            # --- ESTADO: DURANTE O JOGO (PLAYING, COOP, VS) ---
            elif self.state in [GameState.PLAYING, GameState.COOP, GameState.VS]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                if self.level:
                    self.level.update()
                    self.level.draw()

                    if self.level.is_game_over() or self.level.is_victory():
                        lista_players = self.level.mediator.players

                        if self.state == GameState.COOP:
                            name = "Equipe Delta"
                        elif self.state == GameState.VS:
                            p1 = lista_players[0]
                            p2 = lista_players[1]
                            name = "P1 Vencedor" if p1.score > p2.score else "P2 Vencedor"
                        else:
                            name = "Player 1"

                        score_final = self.level.get_final_score()
                        self.database.insert_score(name, score_final)

                        self.level = None
                        self.state = GameState.MENU
                        pygame.time.delay(1000)

            # --- ESTADO: RANKING (SCORE) ---
            elif self.state == GameState.SCORE:
                new_state = self.score_screen.run()
                self.score_screen.draw()
                if new_state == GameState.MENU:
                    self.state = GameState.MENU

            # --- ESTADO: TELA DE SELEÇÃO (ONDE AS TECLAS APARECEM) ---
            elif self.state == GameState.SELECTION:
                new_state, plane = self.selection_screen.run()
                self.selection_screen.draw()

                if new_state == GameState.PLAYING:
                    # Lógica para iniciar o jogo baseado no modo escolhido no Menu
                    if self.selection_screen.mode == GameState.PLAYING:
                        # SINGLE PLAYER: Usa apenas o avião que o jogador selecionou
                        self.selected_plane = plane
                        self.level = Level(self.window, GameState.PLAYING, [self.selected_plane])
                        self.state = GameState.PLAYING
                    else:
                        # MULTIPLAYER (COOP/VS): Usa obrigatoriamente os dois aviões da lista PLANES
                        # Isso garante que o Player 1 e Player 2 apareçam com as teclas certas
                        self.level = Level(self.window, self.selection_screen.mode, [PLANES[0], PLANES[1]])
                        self.state = self.selection_screen.mode

                elif new_state == GameState.MENU:
                    self.state = GameState.MENU

            pygame.display.flip()
        pygame.quit()