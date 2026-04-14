import pygame
import os


class Bullet:
    def __init__(self, x, y, direction, speed, type):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.type = type  # "player" ou "enemy"

        # Carrega a imagem do tiro baseada em quem atirou
        base_path = os.path.dirname(__file__)
        if self.type == "player":
            img_name = "Player1Shot.png"
        else:
            img_name = "Enemy1Shot.png"

        img_path = os.path.join(base_path, "..", "asset", img_name)

        try:
            self.sprite = pygame.image.load(img_path).convert_alpha()
            # Ajusta o tamanho do tiro para ficar proporcional
            self.sprite = pygame.transform.scale(self.sprite, (10, 20))
        except:
            # Fallback caso a imagem falhe
            self.sprite = pygame.Surface((5, 10))
            self.sprite.fill((255, 255, 255))

        self.rect = self.sprite.get_rect(topleft=(x, y))

    def update(self):
        self.y += self.direction * self.speed
        self.rect.y = self.y  # Atualiza a posição da colisão

    def draw(self, window):
        # Mudei de (self.x, self.y) para self.rect
        window.blit(self.sprite, self.rect)