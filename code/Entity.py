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
        pass

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))