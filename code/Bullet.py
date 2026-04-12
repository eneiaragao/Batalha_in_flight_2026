import pygame
from Entity import Entity

class Bullet(Entity):
    def __init__(self, x, y, direction, speed, owner):
        sprite = pygame.Surface((5, 10))
        sprite.fill((255, 255, 0))

        super().__init__("bullet", x, y, sprite)

        self.direction = direction  # -1 sobe, 1 desce
        self.speed = speed
        self.owner = owner  # "player" ou "enemy"

    def move(self):
        self.y += self.speed * self.direction