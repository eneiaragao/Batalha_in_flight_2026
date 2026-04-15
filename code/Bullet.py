import pygame
import os
from Const import C_WHITE, PLAYER_SIZE, SCREEN_WIDTH

class Bullet:
    def __init__(self, x, y, direction, speed, type):
        self.x = x
        self.y = y
        self.direction = direction # Para a direita será 1, para a esquerda será -1
        self.speed = speed
        self.type = type  # "player" ou "enemy"

        base_path = os.path.dirname(__file__)
        img_name = "Player1Shot.png" if self.type == "player" else "Enemy1Shot.png"
        img_path = os.path.join(base_path, "..", "asset", img_name)

        try:
            self.sprite = pygame.image.load(img_path).convert_alpha()
            # Ajustando o tamanho do tiro (geralmente menor que o player)
            self.sprite = pygame.transform.scale(self.sprite, (20, 10))
        except:
            self.sprite = pygame.Surface((10, 5))
            self.sprite.fill(C_WHITE)

        self.rect = self.sprite.get_rect(topleft=(x, y))

    def update(self):
        # Altera o Y para o tiro subir (Player) ou descer (Inimigo)
        self.y += self.direction * self.speed
        self.rect.y = self.y

    def draw(self, window):
        window.blit(self.sprite, self.rect)

    # NOVO MÉTODO: Para evitar o erro de fechar o jogo (AttributeError)
    def handle_collision(self):
        # Aqui você pode adicionar um efeito ou apenas deixar passar
        pass

    def is_off_screen(self):
        """Verifica se o tiro saiu da tela para ser removido"""
        return self.x < 0 or self.x > SCREEN_WIDTH