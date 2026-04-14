import pygame
import random
from Entity import Entity
from Bullet import Bullet
import os

# Isso pega o caminho correto da pasta do seu projeto
base_path = os.path.dirname(__file__)
img_path = os.path.join(base_path, "..", "asset", "Player1.png") # O ".." volta uma pasta


class Enemy(Entity):
    def __init__(self, x, y, speed):
        base_path = os.path.dirname(__file__)
        # Use o caminho dinâmico para evitar erros de pasta
        img_path = os.path.join(base_path, "..", "asset", "Enemy1.png")

        img = pygame.image.load(img_path).convert_alpha()
        sprite = pygame.transform.scale(img, (50, 50))

        super().__init__("enemy", x, y, sprite)
        self.speed = speed
        self.bullets = []
    def move(self):
        self.y += self.speed

    def shoot(self):
        if random.randint(1, 100) < 2:  # chance de atirar
            from Bullet import Bullet  # Import local evita o erro circular
            bullet = Bullet(self.x + 20, self.y, 1, 5, "enemy")
            self.bullets.append(bullet)

    def update(self):
        self.move()
        self.shoot()

        for bullet in self.bullets:
            bullet.update()