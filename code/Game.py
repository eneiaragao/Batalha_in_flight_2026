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
                    # Inicia com as duas primeiras naves da lista PLANES
                    self.level = Level(self.window, self.state, [PLANES[0], PLANES[1]])
                elif new_state == GameState.SCORE:
                    self.state = GameState.SCORE
                elif new_state == GameState.EXIT:
                    self.running = False

            # --- ONDE A MÁGICA ACONTECE ---
            elif self.state in [GameState.PLAYING, GameState.COOP, GameState.VS]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                if self.level:
                    self.level.update()
                    self.level.draw()

                    # MUDANÇA AQUI: Verifica morte OU se venceu a última fase
                    if self.level.is_game_over() or self.level.is_victory():

                        # 1. Lógica para definir o nome no ranking
                        if self.state == GameState.COOP:
                            name = "Equipe"
                        elif self.state == GameState.VS:
                            # Verifica quem fez mais pontos para dar o nome
                            p1 = self.level.players[0]
                            p2 = self.level.players[1]
                            name = "P1 Vencedor" if p1.score > p2.score else "P2 Vencedor"
                        else:
                            name = "Player 1"

                        # 2. Pega o score (média no Coop ou maior no VS)
                        score_final = self.level.get_final_score()

                        # 3. SALVAMENTO EFETIVO
                        # DEBUG: Verifique se isso aparece no seu terminal quando você morre
                        print(f"DEBUG: Tentando salvar {name} com score {score_final}")

                        self.database.insert_score(name, score_final)
                        # Pequeno delay antes de voltar ao menu
                        pygame.time.delay(1000)
                        self.state = GameState.MENU

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