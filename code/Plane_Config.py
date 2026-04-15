class PlaneConfig:
    def __init__(self, name, speed, fire_rate, asset_name):
        self.name = name
        self.speed = speed
        self.fire_rate = fire_rate
        self.asset_name = asset_name


class LevelConfig:
    def __init__(self, name, enemy_speed, spawn_rate, bg_layers, music_name):
        self.name = name
        self.enemy_speed = enemy_speed
        self.spawn_rate = spawn_rate
        # IMPORTANTE: bg_layers deve ser uma lista para o efeito de fundo infinito/camadas
        self.bg_layers = bg_layers
        self.music_name = music_name


# Configurações das Naves
PLANES = [
    PlaneConfig("Rápido", speed=7, fire_rate=400, asset_name="Player2"),
    PlaneConfig("Balanceado", speed=5, fire_rate=300, asset_name="Player1"),
]

# Configurações das Fases
# Fase 1
LevelConfig(
    name="Fase 1",
    enemy_speed=3,
    spawn_rate=60,
    bg_layers=["Level1Bg0"],  # Se tiver mais camadas, adicione: ["Level1Bg0", "Level1Bg1"]
    music_name="Level1"  # AJUSTADO: Igual ao nome do arquivo na pasta
),

# Fase 2
LevelConfig(
    name="Fase 2",
    enemy_speed=4,
    spawn_rate=45,
    bg_layers=["Level2Bg0"],
    music_name="Level2"  # AJUSTADO: Igual ao nome do arquivo na pasta
),

# Fase 3
LevelConfig(
    name="Fase 3",
    enemy_speed=6,
    spawn_rate=30,
    bg_layers=["Level3Bg0"],
    music_name="Level3"  # AJUSTADO: Igual ao nome do arquivo na pasta
)
