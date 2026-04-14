import os
import random
import pygame
from Player import Player
from Enemy import Enemy
from Collision import check_collision
from Level_Config import LEVELS

class Level:
    def __init__(self, window, plane_config):
        self.window = window
        self.player = Player(400, 500, plane_config)

        self.level_index = 0
        self.current_level = LEVELS[self.level_index]

        self.enemies = []
        self.score = 0
        self.spawn_timer = 0

        self.bg_y = 0
        self.scroll_speed = 2  # Velocidade do movimento do fundo

        self.load_level_assets()

    def load_level_assets(self):
        self.bg_images = []
        base_path = os.path.dirname(__file__)

        # 1. Carregar Camadas de Fundo (Montagem de Cenário)
        for layer_name in self.current_level.bg_layers:
            path = os.path.join(base_path, "..", "asset", f"{layer_name}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (1240, 650))
                self.bg_images.append(img)
            except Exception as e:
                print(f"Erro ao carregar camada {layer_name}: {e}")

        # 2. Carregar e Tocar Música do Nível
        try:
            music_path = os.path.join(base_path, "..", "asset", f"{self.current_level.music_name}.mp3")
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao carregar música {self.current_level.music_name}: {e}")

    def load_background(self):

        base_path = os.path.dirname(__file__)
        bg_path = os.path.join(base_path, "..", "asset", f"{self.current_level.bg_name}.png")
        self.bg_image = pygame.image.load(bg_path).convert()
        # Garanta que a imagem cubra a tela toda
        self.bg_image = pygame.transform.scale(self.bg_image, (1240, 650))
    def spawn_enemy(self):
        x = random.randint(0, 1190)
        enemy = Enemy(x, -50, self.current_level.enemy_speed)
        self.enemies.append(enemy)

    def update(self):
        # Faz o fundo "rolar" para baixo
        self.bg_y += self.scroll_speed

        # Se a primeira imagem passar do limite da tela, reseta a posição
        if self.bg_y >= 650:
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
        # sobe de fase a cada 100 pontos
        if self.score >= (self.level_index + 1) * 20: #ajuste para teste
            self.level_index += 1

            if self.level_index < len(LEVELS):
                self.current_level = LEVELS[self.level_index]
                self.load_background()
                print("Nova fase:", self.current_level.name)

    def handle_collisions(self):
        for bullet in self.player.bullets[:]: # o [:] é para evitar erros ao remover itens da lista
            for enemy in self.enemies[:]:
                # check_collision usa o .rect
                if check_collision(bullet.rect, enemy.rect):
                    if enemy in self.enemies: self.enemies.remove(enemy)
                    if bullet in self.player.bullets: self.player.bullets.remove(bullet)
                    self.score += 10
                    break

        for enemy in self.enemies:
            for bullet in enemy.bullets:
                if check_collision(bullet.rect, self.player.rect):
                    enemy.bullets.remove(bullet)
                    self.player.life -= 1

    def draw(self):

        # Desenha duas imagens de fundo para criar o efeito infinito
        # Uma na posição atual e outra logo acima dela
        for img in self.bg_images:
            self.window.blit(img, (0, self.bg_y))
            self.window.blit(img, (0, self.bg_y - 650))

        self.player.draw(self.window)

        for bullet in self.player.bullets:
            bullet.draw(self.window)

        for enemy in self.enemies:
            enemy.draw(self.window)

            for bullet in enemy.bullets:
                bullet.draw(self.window)

        self.draw_ui()


    def draw_ui(self):
        import pygame
        font = pygame.font.SysFont(None, 30)

        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        # Verifique se no seu Player.py o atributo é 'life' ou 'health'
        life_text = font.render(f"Vida: {self.player.life}", True, (255, 255, 255))
        level_text = font.render(f"Fase: {self.current_level.name}", True, (255, 255, 255))

        self.window.blit(score_text, (10, 10))
        self.window.blit(life_text, (10, 40))
        self.window.blit(level_text, (10, 70))


    def is_game_over(self):
        # O jogo acaba se a vida do jogador for menor ou igual a zero
        if self.player.life <= 0:
            return True
        return False


