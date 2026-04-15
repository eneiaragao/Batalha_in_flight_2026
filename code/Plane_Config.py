class PlaneConfig:
    def __init__(self, name, speed, fire_rate, asset_name):
        self.name = name
        self.speed = speed
        self.fire_rate = fire_rate
        self.asset_name = asset_name

#  LISTA DA ESCOLHA DE AVIÃO
PLANES = [
    PlaneConfig("Rápido", speed=7, fire_rate=400, asset_name="Player2"),
    PlaneConfig("Balanceado", speed=6, fire_rate=400, asset_name="Player1"),
]