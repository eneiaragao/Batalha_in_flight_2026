import pygame

class LevelConfig:
    def __init__(self, name, enemy_speed, spawn_rate, bg_layers, music_name):
        self.name = name
        self.enemy_speed = enemy_speed
        self.spawn_rate = spawn_rate
        self.bg_layers = bg_layers  # Lista com os nomes das imagens (ex: ["Level1Bg0", "Level1Bg1"...])
        self.music_name = music_name

LEVELS = [
    LevelConfig("Fase 1", 3, 60, ["Level1Bg0", "Level1Bg1", "Level1Bg2", "Level1Bg3", "Level1Bg4"], "Level1"),
    LevelConfig("Fase 2", 4, 40, ["Level2Bg0", "Level2Bg1", "Level2Bg2", "Level2Bg3"], "Level2"),
    LevelConfig("Fase 3", 5, 30, ["Level3Bg0", "Level3Bg1", "Level3Bg2", "Level3Bg3", "Level43Bg4"], "Level3")
]