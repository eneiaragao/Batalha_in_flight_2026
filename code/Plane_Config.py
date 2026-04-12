

class PlaneConfig:
    def __init__(self, name, speed, fire_rate, color):
        self.name = name
        self.speed = speed
        self.fire_rate = fire_rate
        self.color = color


PLANES = [
    PlaneConfig("Rápido", speed=7, fire_rate=400, color=(0, 255, 0)),
    PlaneConfig("Balanceado", speed=5, fire_rate=300, color=(0, 0, 255)),
    PlaneConfig("Pesado", speed=3, fire_rate=150, color=(255, 0, 0)),
]