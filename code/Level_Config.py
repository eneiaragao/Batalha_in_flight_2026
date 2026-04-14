import pygame

class LevelConfig:
    def __init__(self, name, enemy_speed, spawn_rate, bg_name):
        self.name = name
        self.enemy_speed = enemy_speed
        self.spawn_rate = spawn_rate
        self.bg_name = bg_name # Agora usamos o nome do arquivo PNG

# Aqui você usa os nomes EXATOS dos arquivos que estão na sua pasta asset
LEVELS = [
    LevelConfig("Fase 1", enemy_speed=3, spawn_rate=60, bg_name="Level1Bg0"),
    LevelConfig("Fase 2", enemy_speed=4, spawn_rate=40, bg_name="Level2Bg0"),
    LevelConfig("Fase 3", enemy_speed=5, spawn_rate=25, bg_name="Level4Bg0"),
]