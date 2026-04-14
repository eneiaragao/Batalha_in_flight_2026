
import pygame
class PlaneConfig:
    def __init__(self, name, speed, fire_rate, asset_name):
        self.name = name
        self.speed = speed
        self.fire_rate = fire_rate
        self.asset_name = asset_name # Nome do arquivo sem extensão ou caminho completo

PLANES = [
    PlaneConfig("Rápido", speed=7, fire_rate=400, asset_name="Player2"),
    PlaneConfig("Balanceado", speed=5, fire_rate=300, asset_name="Player1"),
]

class LevelConfig:
    def __init__(self, name, enemy_speed, spawn_rate, bg_name):
        self.name = name
        self.enemy_speed = enemy_speed
        self.spawn_rate = spawn_rate
        self.bg_name = bg_name # Nome da imagem de fundo (ex: Level1Bg0)

LEVELS = [
    LevelConfig("Fase 1", enemy_speed=3, spawn_rate=60, bg_name="Level1Bg0"),
    LevelConfig("Fase 2", enemy_speed=4, spawn_rate=40, bg_name="Level2Bg0"),
]