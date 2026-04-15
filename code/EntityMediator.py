import pygame
from Collision import check_collision


class EntityMediator:
    def __init__(self, explosion_sfx):
        self.players = []
        self.enemies = []
        self.bullets = []  # Centralizamos TODOS os tiros aqui
        self.explosion_sfx = explosion_sfx

    def add_entity(self, entity):
        if entity.name == "player":
            self.players.append(entity)
        elif entity.name == "enemy":
            self.enemies.append(entity)

    def update(self):
        # 1. Atualiza Jogadores e coleta tiros
        for p in self.players:
            if p.life > 0:
                p.update()
                if p.bullets:
                    self.bullets.extend(p.bullets)
                    p.bullets.clear()

        # 2. Atualiza Inimigos e coleta tiros
        for e in self.enemies[:]:
            e.update()
            if e.bullets:
                self.bullets.extend(e.bullets)
                e.bullets.clear()
            if e.y > 700: self.enemies.remove(e)  # Limpeza

        # 3. Atualiza todos os projéteis
        for b in self.bullets[:]:
            b.update()
            if b.y < 0 or b.y > 650: self.bullets.remove(b)

        # 4. Resolve Colisões (Ponto alto do padrão Mediator)
        self.handle_game_logic()

    def handle_game_logic(self):
        for p in self.players:  # Loop do Jogador (P1 ou P2)
            if p.life <= 0: continue

            for b in self.bullets[:]:
                if b.type == "player":
                    for e in self.enemies[:]:
                        if check_collision(b.rect, e.rect):
                            if self.explosion_sfx: self.explosion_sfx.play()

                            for player_pontuacao in self.players:
                                if player_pontuacao.id == b.owner_id:
                                    player_pontuacao.score += 10

                            if e in self.enemies: self.enemies.remove(e)
                            if b in self.bullets: self.bullets.remove(b)
                            break  # Sai do loop de inimigos

                elif b.type == "enemy":
                    if check_collision(b.rect, p.rect):
                        p.life -= 1
                        # Importante: Verificando se a bala ainda está na lista antes de remover
                        if b in self.bullets:
                            self.bullets.remove(b)

    def draw(self, window):
        for p in self.players:
            if p.life > 0: p.draw(window)
        for e in self.enemies: e.draw(window)
        for b in self.bullets: b.draw(window)
