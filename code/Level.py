import os
import random
import pygame
from Game_State import GameState  # Verifique se o nome do arquivo é Game_State ou GameState
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
    # Agora recebemos 'mode' (SINGLE, COOP, VS) e 'plane_configs' (uma lista de naves)
    def __init__(self, window, mode, plane_configs):
        self.window = window
        self.mode = mode
        self.players = []
        self.victory = False  # NOVA FLAG DE VITÓRIA

        # Criar os jogadores baseados na lista recebida
        for i, config in enumerate(plane_configs):
            offset = -100 if i == 0 and len(plane_configs) > 1 else (100 if i == 1 else 0)
            new_player = Player(PLAYER_START_X + offset, PLAYER_START_Y, config, player_id=i + 1)
            self.players.append(new_player)

        # Som de explosão
        base_path = os.path.dirname(__file__)
        self.explosion_sfx = None
        try:
            if not pygame.mixer.get_init(): pygame.mixer.init()
            explosion_path = os.path.join(base_path, "..", "asset", EXPLOSION_SOUND)
            if os.path.exists(explosion_path):
                self.explosion_sfx = pygame.mixer.Sound(explosion_path)
                self.explosion_sfx.set_volume(0.6)
        except Exception as e:
            print(f"Erro som: {e}")

        self.level_index = 0
        self.current_level = LEVELS[self.level_index]
        self.enemies = []
        self.score = 0  # No COOP será a média, no VS será a base do vencedor
        self.spawn_timer = 0
        self.bg_y = 0
        self.scroll_speed = SCROLL_SPEED
        self.load_level_assets()

    def load_level_assets(self):
        self.bg_images = []
        base_path = os.path.dirname(__file__)
        for layer_name in self.current_level.bg_layers:
            path = os.path.join(base_path, "..", "asset", f"{layer_name}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.bg_images.append(pygame.transform.scale(img, SBG_SIZE))

        try:
            music_path = os.path.join(base_path, "..", "asset", f"{self.current_level.music_name}.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
        except:
            pass

    def update(self):
        self.bg_y = (self.bg_y + self.scroll_speed) % SCREEN_HEIGHT

        # Atualiza todos os jogadores vivos
        for player in self.players:
            if player.life > 0:
                player.update()

        self.spawn_timer += 1
        if self.spawn_timer >= self.current_level.spawn_rate:
            x = random.randint(0, SPAWN_X_MAX)
            self.enemies.append(Enemy(x, -50, self.current_level.enemy_speed))
            self.spawn_timer = 0

        # No loop de inimigos:
        for enemy in self.enemies[:]:
            enemy.update()
            # Se o inimigo passou da borda esquerda (X < -50)
            if enemy.x < -50:
                self.enemies.remove(enemy)

        self.handle_collisions()
        self.check_level_progression()

    def handle_collisions(self):
        for player in self.players:
            if player.life <= 0: continue

            # Tiro do Player -> Inimigo
            for bullet in player.bullets[:]:
                for enemy in self.enemies[:]:
                    if check_collision(bullet.rect, enemy.rect):
                        if self.explosion_sfx: self.explosion_sfx.play()

                        # LÓGICA DE SCORE: Adiciona ao score individual do Player
                        player.score += 10

                        if enemy in self.enemies: self.enemies.remove(enemy)
                        if bullet in player.bullets: player.bullets.remove(bullet)
                        break

            # Inimigo -> Player
            for enemy in self.enemies:
                for bullet in enemy.bullets[:]:
                    if check_collision(bullet.rect, player.rect):
                        bullet.handle_collision()  # Assume que bullet tem esse método ou remova da lista
                        if bullet in enemy.bullets: enemy.bullets.remove(bullet)
                        player.life -= 1

    def check_level_progression(self):
        current_total = sum(p.score for p in self.players)
        if current_total >= (self.level_index + 1) * POINTS_PER_LEVEL:
            self.level_index += 1

            if self.level_index < len(LEVELS):
                self.current_level = LEVELS[self.level_index]
                self.load_level_assets()
                print(f"Nova fase: {self.current_level.name}")
            else:
                # ATUALIZADO: Em vez de travar o jogo, avisa que venceu
                self.victory = True
                print("VITÓRIA TOTAL!")

    def is_victory(self):
        return self.victory
    def get_final_score(self):
        # ERRO ANTERIOR: self.mode == "COOP" (String nunca é igual a Enum)
        if self.mode == GameState.COOP:
            return (self.players[0].score + self.players[1].score) // 2
        elif self.mode == GameState.VS:
            return max(p.score for p in self.players)
        return self.players[0].score

    def draw(self):
        for img in self.bg_images:
            self.window.blit(img, (0, self.bg_y))
            self.window.blit(img, (0, self.bg_y - SCREEN_HEIGHT))

        for player in self.players:
            if player.life > 0:
                player.draw(self.window)
                for bullet in player.bullets: bullet.draw(self.window)

        for enemy in self.enemies:
            enemy.draw(self.window)
            for bullet in enemy.bullets: bullet.draw(self.window)

        self.draw_ui()

    def draw_ui(self):
        font = pygame.font.SysFont(None, 25)
        for i, player in enumerate(self.players):
            color = C_WHITE if player.life > 0 else (100, 100, 100)
            txt = f"P{player.id} - Vida: {player.life} | Score: {player.score}"
            surf = font.render(txt, True, color)
            self.window.blit(surf, (10, 10 + (i * 25)))

        lvl_txt = font.render(f"Fase: {self.current_level.name}", True, C_GREEN)
        self.window.blit(lvl_txt, (10, 70))

    def is_game_over(self):
        # No multiplayer, só acaba quando TODOS morrem
        return all(p.life <= 0 for p in self.players)