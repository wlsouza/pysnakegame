import pygame


from pygame.constants import K_x


class Apple(pygame.sprite.Sprite):
    def __init__(self, screen, color, size, start_pos_x, start_pos_y):
        super().__init__()
        self.screen = screen
        self.color = color
        self.size = size
        self.pos_x = start_pos_x
        self.pos_y = start_pos_y
        self.rect = None

    def update(self):
        self.draw()

    def move(self, position):
        self.pos_x, self.pos_y = position
        self.draw()

    def draw(self):
        self.rect = pygame.draw.rect(
            self.screen, self.color, (self.pos_x, self.pos_y, self.size, self.size)
        )
