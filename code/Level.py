import os
import random
import pygame

# Importação das constantes do seu arquivo Const.py
from Const import (
    C_GREEN, C_BLACK, C_WHITE, SUBTEXT_POS, VICTORY_TEXT_POS,
    POINTS_PER_LEVEL, PLAYER_START_X, PLAYER_START_Y,
    SCROLL_SPEED, SBG_SIZE, SPAWN_X_MAX, SCREEN_HEIGHT, EXPLOSION_SOUND
)
from Player import Player
from Enemy import Enemy
from Collision import check_collision
from Level_Config import LEVELS


class Level:
    def __init__(self, window, plane_config):
        self.window = window
        self.player = Player(PLAYER_START_X, PLAYER_START_Y, plane_config)

        # --- CARREGAMENTO DO SOM DE EXPLOSÃO ---
        base_path = os.path.dirname(__file__)
        self.explosion_sfx = None
        try:
            # Inicializa o mixer caso não tenha sido inicializado no main
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            explosion_path = os.path.join(base_path, "..", "asset", EXPLOSION_SOUND)
            if os.path.exists(explosion_path):
                self.explosion_sfx = pygame.mixer.Sound(explosion_path)
                self.explosion_sfx.set_volume(0.6)  # Volume em 60%
                print("Som de explosão carregado com sucesso.")
            else:
                print(f"AVISO: Arquivo de som {EXPLOSION_SOUND} não encontrado.")
        except Exception as e:
            print(f"Erro ao inicializar som: {e}")

        self.level_index = 0
        self.current_level = LEVELS[self.level_index]

        self.enemies = []
        self.score = 0
        self.spawn_timer = 0

        self.bg_y = 0
        self.scroll_speed = SCROLL_SPEED

        self.load_level_assets()

    def load_level_assets(self):
        self.bg_images = []
        base_path = os.path.dirname(__file__)

        print(f"--- Carregando assets da {self.current_level.name} ---")

        for layer_name in self.current_level.bg_layers:
            filename = f"{layer_name}.png"
            path = os.path.join(base_path, "..", "asset", filename)

            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, SBG_SIZE)
                self.bg_images.append(img)
                print(f"Sucesso: {filename}")
            else:
                print(f"ERRO CRÍTICO: O arquivo {path} NÃO EXISTE!")

        try:
            music_filename = f"{self.current_level.music_name}.mp3"
            music_path = os.path.join(base_path, "..", "asset", music_filename)

            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(500)

            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
            else:
                print(f"Erro: Música {music_filename} não encontrada.")
        except Exception as e:
            print(f"Erro na música: {e}")

    def spawn_enemy(self):
        # Sorteia o X usando a constante e define o Y acima da tela
        x = random.randint(0, SPAWN_X_MAX)
        enemy = Enemy(x, -50, self.current_level.enemy_speed)
        self.enemies.append(enemy)

    def update(self):
        self.bg_y += self.scroll_speed

        if self.bg_y >= SCREEN_HEIGHT:
            self.bg_y = 0

        self.player.update()
        self.spawn_timer += 1

        if self.spawn_timer >= self.current_level.spawn_rate:
            self.spawn_enemy()
            self.spawn_timer = 0

        for enemy in self.enemies:
            enemy.update()

        self.handle_collisions()
        self.check_level_progression()

    def check_level_progression(self):
        if self.score >= (self.level_index + 1) * POINTS_PER_LEVEL:
            self.level_index += 1

            if self.level_index < len(LEVELS):
                self.current_level = LEVELS[self.level_index]
                self.load_level_assets()
                print("Nova fase:", self.current_level.name)
            else:
                print("VITORIA TOTAL!")
                self.show_victory_screen()

    def show_victory_screen(self):
        font = pygame.font.SysFont(None, 80)
        text = font.render("MISSÃO CUMPRIDA!", True, C_GREEN)
        subtext = font.render("Aperte qualquer tecla para sair", True, C_WHITE)

        while True:
            self.window.fill(C_BLACK)
            self.window.blit(text, VICTORY_TEXT_POS)
            self.window.blit(subtext, SUBTEXT_POS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    import sys
                    sys.exit()

    def handle_collisions(self):
        # Colisão: Tiro do Player -> Inimigo
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if check_collision(bullet.rect, enemy.rect):
                    # Toca o som de explosão se ele existir
                    if self.explosion_sfx:
                        self.explosion_sfx.play()

                    if enemy in self.enemies: self.enemies.remove(enemy)
                    if bullet in self.player.bullets: self.player.bullets.remove(bullet)
                    self.score += 10
                    break

        # Colisão: Tiro do Inimigo -> Player
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                if check_collision(bullet.rect, self.player.rect):
                    if bullet in enemy.bullets:
                        enemy.bullets.remove(bullet)
                        self.player.life -= 1

    def draw(self):
        # Fundo infinito
        for img in self.bg_images:
            self.window.blit(img, (0, self.bg_y))
            self.window.blit(img, (0, self.bg_y - SCREEN_HEIGHT))

        self.player.draw(self.window)

        for bullet in self.player.bullets:
            bullet.draw(self.window)

        for enemy in self.enemies:
            enemy.draw(self.window)
            for bullet in enemy.bullets:
                bullet.draw(self.window)

        self.draw_ui()

    def draw_ui(self):
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {self.score}", True, C_WHITE)
        life_text = font.render(f"Vida: {self.player.life}", True, C_WHITE)
        level_text = font.render(f"Fase: {self.current_level.name}", True, C_WHITE)

        self.window.blit(score_text, (10, 10))
        self.window.blit(life_text, (10, 40))
        self.window.blit(level_text, (10, 70))

    def is_game_over(self):
        return self.player.life <= 0