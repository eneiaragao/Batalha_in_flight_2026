import pygame
import os

from Const import LIVE_PLAYERS
from Entity import Entity




class Player(Entity):
    def __init__(self, x, y, plane_config, player_id=1):
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, "..", "asset", f"{plane_config.asset_name}.png")

        img = pygame.image.load(img_path).convert_alpha()

        # --- ROTACIONAR A NAVE ---
        # rotate(imagem, ângulo): 90 graus gira ela para olhar para CIMA
        img = pygame.transform.rotate(img, 90)

        sprite = pygame.transform.scale(img, (50, 50))
        super().__init__("player", x, y, sprite)

        self.id = player_id  # Salva o ID
        self.score = 0  # Cada player agora tem seu próprio score
        self.speed = plane_config.speed
        self.shoot_delay = plane_config.fire_rate
        self.bullets = []
        self.life = LIVE_PLAYERS #quantidade de vidas po player
        self.last_shot = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if self.id == 1:
            # TECLAS PLAYER 1 (Setas)
            if keys[pygame.K_LEFT] and self.x > 0:
                self.x -= self.speed
            if keys[pygame.K_RIGHT] and self.x < 1190:
                self.x += self.speed
            if keys[pygame.K_UP] and self.y > 0:
                self.y -= self.speed
            if keys[pygame.K_DOWN] and self.y < 600:
                self.y += self.speed

        elif self.id == 2:
            # TECLAS PLAYER 2 (W, A, S, D)
            if keys[pygame.K_a] and self.x > 0:
                self.x -= self.speed
            if keys[pygame.K_d] and self.x < 1190:
                self.x += self.speed
            if keys[pygame.K_w] and self.y > 0:
                self.y -= self.speed
            if keys[pygame.K_s] and self.y < 600:
                self.y += self.speed

        # Atualiza posição do retângulo de colisão (FORA dos ifs acima)
        self.rect.x = self.x
        self.rect.y = self.y

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            from Bullet import Bullet
            # x + 25 centraliza o tiro no bico da nave (50px de largura)
            # direção -1 faz o tiro SUBIR
            bullet = Bullet(self.x + 25, self.y, -1, 10, "player")
            self.bullets.append(bullet)
            self.last_shot = now

    def update(self):
        self.move()

        keys = pygame.key.get_pressed()

        # TECLA DE TIRO SEPARADA
        if self.id == 1:
            if keys[pygame.K_SPACE]: self.shoot()
        else:
            if keys[pygame.K_l]: self.shoot()  # Player 2 atira no 'L'

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.y > 0]