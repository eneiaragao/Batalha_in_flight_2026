import pygame
import os
from Entity import Entity




class Player(Entity):
    def __init__(self, x, y, plane_config):
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, "..", "asset", f"{plane_config.asset_name}.png")

        img = pygame.image.load(img_path).convert_alpha()

        # --- ROTACIONAR A NAVE ---
        # rotate(imagem, ângulo): 90 graus gira ela para olhar para CIMA
        img = pygame.transform.rotate(img, 90)

        sprite = pygame.transform.scale(img, (50, 50))
        super().__init__("player", x, y, sprite)

        self.speed = plane_config.speed
        self.shoot_delay = plane_config.fire_rate
        self.bullets = []
        self.life = 3
        self.last_shot = 0

    def move(self):
        keys = pygame.key.get_pressed()

        # Esquerda e Direita
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < 1190:
            self.x += self.speed

        # --- ADICIONAR PARA FRENTE E PARA TRÁS ---
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < 600:
            self.y += self.speed

        # Atualiza a posição do retângulo de colisão
        self.rect.x = self.x
        self.rect.y = self.y  # Não esqueça de atualizar o Y também!
    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            from Bullet import Bullet  # Import local para evitar travamento
            # Usa o Player1Shot.png ou similar ,
            # mas por enquanto manter a lógica da Bullet
            bullet = Bullet(self.x + 20, self.y, -1, 7, "player")
            self.bullets.append(bullet)
            self.last_shot = now

    def update(self):
        self.move()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()

        for bullet in self.bullets:
            bullet.update()

        self.bullets = [b for b in self.bullets if b.y > 0]