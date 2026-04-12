import pygame
from Entity import Entity
from Bullet import Bullet

class Player(Entity):
    def __init__(self, x, y, plane_config):
        sprite = pygame.Surface((50, 50))
        sprite.fill(plane_config.color)

        super().__init__("player", x, y, sprite)

        self.speed = plane_config.speed
        self.shoot_delay = plane_config.fire_rate
        self.bullets = []
        self.life = 3
        self.last_shot = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
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

        # remove tiros fora da tela
        self.bullets = [b for b in self.bullets if b.y > 0]