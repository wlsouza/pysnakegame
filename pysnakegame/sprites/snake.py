import pygame


class Snake(pygame.sprite.Sprite):
    def __init__(self, screen, color, body_part_size):
        super().__init__()
        self.screen = screen
        self.color = color
        self.body_part_size = body_part_size
        self.current_direction = None
        self.body = [(0, 0)]
        self.rects = []

    @property
    def head(self):
        return self.body[-1]

    @property
    def tail(self):
        return self.body[0]

    @property
    def head_rect(self):
        return self.rects[-1]

    @property
    def body_rects(self):
        return self.rects[0:-1]

    def update(self):
        self.move()
        self.draw()

    def move(self):
        if self.current_direction:
            # adiciona a parte da frente do corpo (a cabeça)
            pos_x, pos_y = self.head

            if self.current_direction == "up":
                pos_y -= self.body_part_size
            elif self.current_direction == "down":
                pos_y += self.body_part_size
            elif self.current_direction == "left":
                pos_x -= self.body_part_size
            elif self.current_direction == "right":
                pos_x += self.body_part_size
            self.body.append((pos_x, pos_y))

            # remove a primeira parte do corpo da cobra (a cauda)
            self.body.pop(0)

    def increase_body(self):
        # adiciona mais uma parte do corpo na mesma posição que a cauda
        self.body.insert(0,self.tail)

    def reset(self):
        self.body = [(0, 0)]
        self.current_direction = None

    def draw(self):
        self.rects = []
        for body_part in self.body:
            rect = pygame.Rect(
                body_part, (self.body_part_size, self.body_part_size)
            )
            if body_part == self.head:
                self._draw_tong(rect)
            self._draw_body(rect)
            self.rects.append(rect)

    def _draw_body(self, rect):
        pos_x, pos_y = rect.x, rect.y
        pygame.draw.rect(self.screen, self.color, rect)
        pygame.draw.rect(
            self.screen,
            (self.color[2], self.color[1], self.color[0]), # mix color values
            (
                pos_x + (self.body_part_size // 4),
                pos_y + (self.body_part_size // 4),
                self.body_part_size // 2,
                self.body_part_size // 2,
            ),
        )

    def _draw_tong(self, rect):
        pos_x, pos_y = rect.x, rect.y
        if self.current_direction == "up":
            pygame.draw.line(
                self.screen,
                (255, 0, 0),
                (pos_x + self.body_part_size // 2, pos_y),
                (pos_x + self.body_part_size // 2, pos_y - self.body_part_size // 4),
                3,
            )
        elif self.current_direction == "down":
            pygame.draw.line(
                self.screen,
                (255, 0, 0),
                (pos_x + self.body_part_size // 2, pos_y + self.body_part_size),
                (
                    pos_x + self.body_part_size // 2,
                    int(pos_y + self.body_part_size * 1.25),
                ),
                3,
            )
        elif self.current_direction == "left":
            pygame.draw.line(
                self.screen,
                (255, 0, 0),
                (pos_x, pos_y + self.body_part_size // 2),
                (pos_x - self.body_part_size // 4, pos_y + self.body_part_size // 2),
                3,
            )
        elif self.current_direction == "right":
            pygame.draw.line(
                self.screen,
                (255, 0, 0),
                (pos_x + self.body_part_size, pos_y + self.body_part_size // 2),
                (
                    int(pos_x + self.body_part_size * 1.25),
                    pos_y + self.body_part_size // 2,
                ),
                3,
            )
