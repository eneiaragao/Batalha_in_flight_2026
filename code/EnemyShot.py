import pygame
import random
from Entity import Entity
from Bullet import Bullet

class Enemy(Entity):
    def __init__(self, x, y):
        sprite = pygame.Surface((40, 40))
        sprite.fill((255, 0, 0))
        super().__init__("enemy", x, y, sprite)

        self.speed = 3
        self.bullets = []

    def move(self):
        self.y += self.speed

    def shoot(self):
        if random.randint(1, 100) < 2:  # chance de atirar
            bullet = Bullet(self.x + 20, self.y, 1, 5, "enemy")
            self.bullets.append(bullet)

    def update(self):
        self.move()
        self.shoot()

        for bullet in self.bullets:
            bullet.update()