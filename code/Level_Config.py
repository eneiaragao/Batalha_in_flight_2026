class LevelConfig:
    def __init__(self, name, enemy_speed, spawn_rate, bg_color):
        self.name = name
        self.enemy_speed = enemy_speed
        self.spawn_rate = spawn_rate
        self.bg_color = bg_color


LEVELS = [
    LevelConfig("Cidade", enemy_speed=3, spawn_rate=60, bg_color=(50, 50, 100)),
    LevelConfig("Deserto", enemy_speed=4, spawn_rate=40, bg_color=(194, 178, 128)),
    LevelConfig("Mar", enemy_speed=5, spawn_rate=25, bg_color=(0, 105, 148)),
]