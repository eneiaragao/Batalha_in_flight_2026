import pygame
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

            if self.state == GameState.MENU:
                new_state = self.menu.run()
                self.menu.draw()

                if new_state == GameState.PLAYING:
                    self.state = GameState.SELECTION
                elif new_state in [GameState.COOP, GameState.VS]:
                    self.state = new_state
                    self.level = Level(self.window, self.state, [PLANES[0], PLANES[1]])
                elif new_state == GameState.SCORE:
                    self.state = GameState.SCORE
                elif new_state == GameState.EXIT:
                    self.running = False

            elif self.state in [GameState.PLAYING, GameState.COOP, GameState.VS]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                if self.level:
                    self.level.update()
                    self.level.draw()

                    # --- VERIFICAÇÃO DE FIM DE JOGO ---
                    if self.level.is_game_over() or self.level.is_victory():
                        lista_players = self.level.mediator.players

                        # 1. Define o nome para o Ranking
                        if self.state == GameState.COOP:
                            name = "Equipe"
                        elif self.state == GameState.VS:
                            p1 = lista_players[0]
                            p2 = lista_players[1]
                            name = "P1 Vencedor" if p1.score > p2.score else "P2 Vencedor"
                        else:
                            name = "Player 1"

                        # 2. Pega o score processado (Média no Coop / Maior no VS)
                        score_final = self.level.get_final_score()

                        # 3. Executa o salvamento
                        print(f"DEBUG: Salvando {name} com score {score_final}")
                        self.database.insert_score(name, score_final)

                        # --- MODIFICAÇÃO DE SEGURANÇA ---
                        # Removemos o level e mudamos o estado ANTES do delay
                        # Isso impede que o loop rode novamente e salve duplicado
                        self.level = None
                        self.state = GameState.MENU

                        pygame.time.delay(1000)

            elif self.state == GameState.SCORE:
                new_state = self.score_screen.run()
                self.score_screen.draw()
                if new_state == GameState.MENU:
                    self.state = GameState.MENU

            elif self.state == GameState.SELECTION:
                new_state, plane = self.selection_screen.run()
                self.selection_screen.draw()

                if new_state == GameState.PLAYING:
                    self.selected_plane = plane
                    self.level = Level(self.window, GameState.PLAYING, [self.selected_plane])
                    self.state = GameState.PLAYING
                elif new_state == GameState.MENU:
                    self.state = GameState.MENU

            pygame.display.flip()
        pygame.quit()