import pygame
import os

from Const import LIVE_PLAYERS, SCORE_POWER_UP_TIME, SPEED_SHOOT, SPEED_SHOOT_POWER
from Entity import Entity




class Player(Entity):
    def __init__(self, x, y, plane_config, player_id=1):
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, "..", "asset", f"{plane_config.asset_name}.png")

        img = pygame.image.load(img_path).convert_alpha()

        # --- ROTACIONAR A NAVE ---
        # rotate(imagem, ângulo): 90 graus gira ela para olhar para CIMA
        img = pygame.transform.rotate(img, 90)

        self.image = pygame.transform.scale(img, (50, 50))
        super().__init__("player", x, y, self.image)

        self.id = player_id  # Salva o ID
        self.score = 0  # Cada player agora tem seu próprio score
        self.speed = plane_config.speed
        self.shoot_delay = plane_config.fire_rate
        self.bullets = []
        self.life = LIVE_PLAYERS #quantidade de vidas po player
        self.last_shot = 0
        self.power_up_active = False
        self.power_up_timer = 0
        self.last_shot_time = 0

    def activate_power_up(self):
        self.power_up_active = True
        # 30 segundos * 60 FPS = 1800 frames
        self.power_up_timer =SCORE_POWER_UP_TIME
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

        # LOGICA DO POWER-UP: Tiros muito mais rápidos (50ms vs 300ms)
        cooldown = 100 if self.power_up_active else self.shoot_delay

        if now - self.last_shot > cooldown:
            from Bullet import Bullet  # Garanta que o arquivo Bullet.py não importe Player de volta

            if self.power_up_active:
                # TIRO DUPLO (Um em cada lado da nave)
                b1 = Bullet(self.x + 5, self.y, -1, SPEED_SHOOT_POWER, "player", self.id)
                b2 = Bullet(self.x + 45, self.y, -1, SPEED_SHOOT_POWER, "player", self.id)
                self.bullets.extend([b1, b2])
            else:
                # TIRO NORMAL (Centralizado)
                bullet = Bullet(self.x + 25, self.y, -1, SPEED_SHOOT, "player", self.id)
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
        self.bullets = [b for b in self.bullets if b.y > -50]
        # Controle do Power-Up
        if self.power_up_active:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.power_up_active = False

    def draw(self, window):
        # Lógica para PISCAR: Desenha a nave apenas em frames pares
        if self.power_up_active:
            if (self.power_up_timer // 5) % 2 == 0:  # Pisca a cada 5 frames
                window.blit(self.image, self.rect)
        else:
            window.blit(self.image, self.rect)