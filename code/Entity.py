class Entity:
    def __init__(self, name, x, y, sprite):
        self.name = name
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = sprite.get_rect(topleft=(x, y))

    def update(self):
        self.move()

    def move(self):
        self.y += self.speed
        self.rect.y = self.y  # Atualiza a posição da colisão

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))