import pygame
import os
from Entity import Entity


# Removi o import de Bullet do topo para evitar erro circular

class Player(Entity):
    def __init__(self, x, y, plane_config):
        # 1. Carregar a imagem real usando o nome que está no PlaneConfig
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, "..", "asset", f"{plane_config.asset_name}.png")

        try:
            img = pygame.image.load(img_path).convert_alpha()
            sprite = pygame.transform.scale(img, (50, 50))  # Ajuste o tamanho se necessário
        except pygame.error:
            # Caso a imagem falhe, cria um bloco reserva para o jogo não fechar
            sprite = pygame.Surface((50, 50))
            sprite.fill((0, 255, 0))

        super().__init__("player", x, y, sprite)

        self.speed = plane_config.speed
        self.shoot_delay = plane_config.fire_rate
        self.bullets = []
        self.life = 3
        self.last_shot = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < 1190:  # Limite da tela (1240 - 50)
            self.x += self.speed

        # IMPORTANTE: Atualiza o retângulo de colisão e desenho
        self.rect.x = self.x

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            from Bullet import Bullet  # Import local para evitar travamento
            # Usa o Player1Shot.png ou similar se quiser,
            # mas por enquanto vamos manter a lógica da Bullet
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