import pygame
from database import Database
from Level import Level
from Menu import Menu
from Game_State import GameState
from Score_Screen import ScoreScreen
from Selection_Screen import SelectionScreen


class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Air Combat")

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

                elif new_state == GameState.SCORE:
                    self.state = GameState.SCORE

                elif new_state == GameState.EXIT:
                    self.running = False

            elif self.state == GameState.PLAYING:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                self.level.update()
                self.level.draw()

                if self.level.is_game_over():
                    name = "Player"
                    score = self.level.score
                    self.database.insert_score(name, score)
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
                    self.level = Level(self.window, plane)
                    self.state = GameState.PLAYING

                elif new_state == GameState.MENU:
                    self.state = GameState.MENU

                elif new_state == GameState.EXIT:
                    self.running = False

            # Essencial para a tela deixar de ficar preta:
            pygame.display.flip()

        pygame.quit()