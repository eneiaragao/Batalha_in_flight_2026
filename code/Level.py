import random
from Player import Player
from Enemy import Enemy
from Collision import check_collision
from Level_Config import LEVELS

class Level:
    def __init__(self, window, plane_config):
        self.window = window
        self.player = Player(400, 500, plane_config)

        self.level_index = 0
        self.current_level = LEVELS[self.level_index]

        self.enemies = []
        self.score = 0
        self.spawn_timer = 0

    def spawn_enemy(self):
        x = random.randint(0, 760)
        enemy = Enemy(x, -50, self.current_level.enemy_speed)
        self.enemies.append(enemy)

    def update(self):
        self.player.update()

        self.spawn_timer += 1

        if self.spawn_timer >= self.current_level.spawn_rate:
            self.spawn_enemy()
            self.spawn_timer = 0

        for enemy in self.enemies:
            enemy.update()

        self.handle_collisions()
        self.check_level_progression()

    def check_level_progression(self):
        # sobe de fase a cada 100 pontos
        if self.score >= (self.level_index + 1) * 100:
            self.level_index += 1

            if self.level_index < len(LEVELS):
                self.current_level = LEVELS[self.level_index]
                print("Mudou para fase:", self.current_level.name)

    def handle_collisions(self):
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if check_collision(bullet.rect, enemy.rect):
                    self.enemies.remove(enemy)
                    self.player.bullets.remove(bullet)
                    self.score += 10
                    break

        for enemy in self.enemies:
            for bullet in enemy.bullets:
                if check_collision(bullet.rect, self.player.rect):
                    enemy.bullets.remove(bullet)
                    self.player.life -= 1

    def draw(self):
        self.window.fill(self.current_level.bg_color)

        self.player.draw(self.window)

        for bullet in self.player.bullets:
            bullet.draw(self.window)

        for enemy in self.enemies:
            enemy.draw(self.window)

            for bullet in enemy.bullets:
                bullet.draw(self.window)

        self.draw_ui()

    #def draw_ui(self):
     #   import pygame
      #  font = pygame.font.SysFont(None, 30)

       # score_text = font.render(f"Score: {self.score}", True, (255,255,255))
        #life_text = font.render(f"Vida: {self.player.life}", True, (255,255,255))
        #level_text = font.render(f"Fase: {self.current_level.name}", True, (255,255,255))

        #self.window.blit(score_text, (10, 10))
        #self.window.blit(life_text, (10, 40))
        #self.window.blit(level_text, (10, 70))
    def draw_ui(self):
        import pygame
        font = pygame.font.SysFont(None, 30)

        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        # Verifique se no seu Player.py o atributo é 'life' ou 'health'
        life_text = font.render(f"Vida: {self.player.life}", True, (255, 255, 255))
        level_text = font.render(f"Fase: {self.current_level.name}", True, (255, 255, 255))

        self.window.blit(score_text, (10, 10))
        self.window.blit(life_text, (10, 40))
        self.window.blit(level_text, (10, 70))

    # --- ADICIONE ESTE MÉTODO AQUI ---
    def is_game_over(self):
        # O jogo acaba se a vida do jogador for menor ou igual a zero
        if self.player.life <= 0:
            return True
        return False