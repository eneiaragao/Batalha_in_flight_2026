import pygame

from Const import C_WHITE, C_ROYAL_BLUE, C_SKY_BLUE


class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = C_ROYAL_BLUE
        self.hover_color = C_SKY_BLUE
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, self.hover_color, self.rect)
        else:
            pygame.draw.rect(window, self.color, self.rect)

        text_surface = self.font.render(self.text, True, C_WHITE)
        window.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False