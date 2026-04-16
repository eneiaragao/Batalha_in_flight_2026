import os
import random
import pygame
from Game_State import GameState
from Const import (
     POINTS_PER_LEVEL, PLAYER_START_X, PLAYER_START_Y,
    SCROLL_SPEED, SBG_SIZE, SPAWN_X_MAX, SCREEN_HEIGHT, EXPLOSION_SOUND, EXPLOSION_VOLUME
)
from Level_Config import LEVELS
# IMPORTAÇÕES DOS NOVOS PADRÕES
from EntityFactory import EntityFactory
from EntityMediator import EntityMediator


class Level:
    def __init__(self, window, mode, plane_configs):
        self.window = window
        self.mode = mode
        self.victory = False
        # 1. Som de Explosão (Mantido aqui para ser passado ao Mediador)
        self.explosion_sfx = self._load_explosion_sound()

        # 2. INICIALIZA O MEDIADOR
        self.mediator = EntityMediator(self.explosion_sfx)
        self.level_index = 0
        self.current_level = LEVELS[self.level_index]
        self.load_level_assets()

        # 3. USA A FACTORY PARA CRIAR OS JOGADORES
        for i, config in enumerate(plane_configs):
            offset = -100 if i == 0 and len(plane_configs) > 1 else (100 if i == 1 else 0)
            # A fábrica entrega o objeto pronto
            player = EntityFactory.get_entity("player", PLAYER_START_X + offset, PLAYER_START_Y, config, i + 1)
            # O Mediador assume a gerência dele
            self.mediator.add_entity(player)
        self.spawn_timer = 0
        self.bg_y = 0
        self.scroll_speed = SCROLL_SPEED

    def _load_explosion_sound(self):
        base_path = os.path.dirname(__file__)
        try:
            if not pygame.mixer.get_init(): pygame.mixer.init()
            path = os.path.join(base_path, "..", "asset", EXPLOSION_SOUND)
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(EXPLOSION_VOLUME)
                return sound
        except:
            pass
        return None

    def load_level_assets(self):
        # --- O SEGREDO ESTÁ AQUI: Limpar a lista anterior ---
        self.bg_images = []

        base_path = os.path.dirname(__file__)

        # Carrega as novas camadas de fundo da fase atual
        for layer_name in self.current_level.bg_layers:
            path = os.path.join(base_path, "..", "asset", f"{layer_name}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                # Redimensiona para o tamanho padrão do cenário
                self.bg_images.append(pygame.transform.scale(img, SBG_SIZE))

        # Atualiza a música para a nova fase
        try:
            music_path = os.path.join(base_path, "..", "asset", f"{self.current_level.music_name}.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")

    def update(self):
        # Atualiza o fundo infinito
        self.bg_y = (self.bg_y + self.scroll_speed) % SCREEN_HEIGHT

        # 4. SPAWN DE INIMIGOS USANDO A FACTORY
        self.spawn_timer += 1
        if self.spawn_timer >= self.current_level.spawn_rate:
            x = random.randint(0, SPAWN_X_MAX)
            # Cria via Fábrica e entrega  ao Mediador
            enemy = EntityFactory.get_entity("enemy", x, -50, self.current_level.enemy_speed)
            self.mediator.add_entity(enemy)
            self.spawn_timer = 0

        # 5. O MEDIADOR ATUALIZA TUDO (Movimento, Tiros e Colisões)
        self.mediator.update()

        # --- NOVA LÓGICA DE POWER-UP (Verifica a cada frame) ---
        for p in self.mediator.players:
            # Se o score for múltiplo de 200 e ele não estiver com power-up ativo
            # Usamos score > 0 para não ativar no início do jogo
            if p.score > 0 and p.score % 200 == 0 and not p.power_up_active:
                p.activate_power_up()
                print(f"DEBUG: Power-up ativado para Player {p.id} (Score: {p.score})")

        # Checa progresso da fase
        self.check_level_progression()
    def check_level_progression(self):
        current_total = sum(p.score for p in self.mediator.players)
        puntos_necessarios = (self.level_index + 1) * POINTS_PER_LEVEL

        if current_total >= puntos_necessarios:
            if self.level_index < len(LEVELS) - 1:
                # Muda de fase normalmente (Fase 1 -> 2 ou 2 -> 3)
                self.level_index += 1
                self.current_level = LEVELS[self.level_index]

                # RECARREGA TUDO: Imagens e Música
                self.load_level_assets()

                # Reseta o timer de spawn para os novos inimigos da fase
                self.spawn_timer = 0
                print(f"DEBUG: Cenário atualizado para Fase {self.level_index + 1}")
            else:
                # Modo infinito na última fase
                # Não altera  o self.victory para True, então o jogo nunca chama o GameState.SCORE
                # até que as vidas (is_game_over) cheguem a zero.
                pass
    def draw(self):
        # Desenha Fundo
        for img in self.bg_images:
            self.window.blit(img, (0, self.bg_y))
            self.window.blit(img, (0, self.bg_y - SCREEN_HEIGHT))

        # 6. O MEDIADOR DESENHA TODAS AS ENTIDADES
        self.mediator.draw(self.window)

        # Desenha a Interface (UI)
        self.draw_ui()

    def draw_ui(self):
        font = pygame.font.SysFont(None, 25)
        # Pega os jogadores direto do mediador
        for i, player in enumerate(self.mediator.players):
            # Mostra P1 e P2 com seus respectivos scores individuais na tela
            color = (255, 255, 255) if player.life > 0 else (150, 150, 150)
            txt = f"Player {player.id} - Score: {player.score} | Vida: {player.life}"
            surf = font.render(txt, True, color)
            self.window.blit(surf, (10, 10 + (i * 30)))

    # Getters úteis para a classe Game
    def is_victory(self):
        return self.victory

    def is_game_over(self):
        return all(p.life <= 0 for p in self.mediator.players)

    def get_final_score(self):
        players = self.mediator.players
        if not players: return 0

        if self.mode == GameState.COOP:
            # MODO COOPERATIVO: Soma os dois e divide por 2 (Média)
            soma = sum(p.score for p in players)
            return soma // 2

        elif self.mode == GameState.VS:
            # MODO COMPETITIVO: Retorna apenas a pontuação do melhor
            return max(p.score for p in players)

        # Modo Single Player
        return players[0].score