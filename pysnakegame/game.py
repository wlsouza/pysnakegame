import os
import pygame
import random
from sprites.snake import Snake
from sprites.apple import Apple


class Game:

    # Define constantes do game
    WIDTH = 600
    HEIGHT = 600
    BLOCK_SIZE = 20
    FPS = 10

    # Define cores
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARKGREEN = (11, 83, 69)
    SKYBLUE = (133, 193, 233)
    STEELBLUE = (46, 134, 193)

    def __init__(self):
        pygame.init()  # Inicia o pygame
        pygame.mixer.init()  # Para iniciar o som
        pygame.display.set_caption("Pysnakegame")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()  # Para sincronizar o FPS
        self.map_positions = self._generate_map_positions()

        # Define fonts
        self.big_font = pygame.font.Font("pysnakegame/fonts/snake_font.ttf", 60)
        self.small_font = pygame.font.Font("pysnakegame/fonts/snake_font.ttf", 18)

        # Define sounds
        self.win_sound = pygame.mixer.Sound("pysnakegame/sounds/win.ogg")
        self.game_over_sound = pygame.mixer.Sound("pysnakegame/sounds/game_over.ogg")
        self.apple_eat_sound = pygame.mixer.Sound("pysnakegame/sounds/apple_eat.ogg")

        # Agrupa todas as sprites juntas para deixar fácil de atualizar.
        self.all_sprites = pygame.sprite.Group()

        # cria a cobra e a maça
        self.snake = Snake(
            screen=self.screen,
            color=self.DARKGREEN,
            body_part_size=self.BLOCK_SIZE,
        )
        self.apple = Apple(
            self.screen,
            self.RED,
            self.BLOCK_SIZE,
            *self._generate_apple_position(),
        )
        self.all_sprites.add(self.snake)
        self.all_sprites.add(self.apple)

    def run(self):
        # Game loop
        self.running = True
        self.game_over = False
        while self.running:

            self.clock.tick(self.FPS)

            # 1 Processa eventos/inputs
            self._check_game_over_events()
            self._check_game_events()

            # 2 Draw/render
            self._draw_grid()
            self._render_score()

            # 3 Update
            self.all_sprites.update()

            # 4 colisões
            self._check_collisions()

            # Atualiza o display
            pygame.display.flip()

        pygame.quit()

    def _check_collisions(self):
        # checando se houve colisão da cabeça da cobra com a maça
        if self.snake.head_rect.colliderect(self.apple.rect):
            self.apple_eat_sound.play()
            self.snake.increase_body()
            if len(self.snake.body) == len(self.map_positions):
                self.win_sound.play()
                self._game_over("You win!!")
            else:
                self.apple.move(self._generate_apple_position())

        # checando se houve colisão da cabeça da cobra com seu corpo.
        if self.snake.head_rect.collidelist(self.snake.body_rects) != -1:
            self.game_over_sound.play()
            self._game_over("Game Over")

        # checando se a cabeça da cobra saiu do mapa (vulgo bateu nas paredes)
        if self.snake.head not in self.map_positions:
            self.game_over_sound.play()
            self._game_over("Game Over")

    def _check_game_events(self):
        for event in pygame.event.get():
            # Escuta teclas pressionadas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.current_direction != "down":
                    self.snake.current_direction = "up"
                elif (
                    event.key == pygame.K_DOWN and self.snake.current_direction != "up"
                ):
                    self.snake.current_direction = "down"
                elif (
                    event.key == pygame.K_LEFT
                    and self.snake.current_direction != "right"
                ):
                    self.snake.current_direction = "left"
                elif (
                    event.key == pygame.K_RIGHT
                    and self.snake.current_direction != "left"
                ):
                    self.snake.current_direction = "right"
                # elif event.key == pygame.K_SPACE: # pause the game
                #     self.snake.current_direction = None
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.QUIT:
                # Escuta se o botão X da janela é clicado
                self.running = False

    def _check_game_over_events(self):
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # sai do jogo
                        self.running = False
                        self.game_over = False
                    elif event.key == pygame.K_SPACE:
                        # recomeça o jogo
                        self.game_over = False
                elif event.type == pygame.QUIT:
                    # Escuta se o botão X da janela é clicado
                    # e sai do jogo
                    self.running = False
                    self.game_over = False

    def _render_score(self):
        score_text = self.small_font.render(
            f"{len(self.snake.body)-1} pontos", True, self.BLACK
        )
        self.screen.blit(score_text, (self.WIDTH - 120, 3))

    def _game_over(self, msg):
        self.game_over = True
        self._fade_screen()
        game_over_text = self.big_font.render(msg, True, self.BLACK)
        continue_text = self.small_font.render("Press SPACE to continue", True, self.BLACK)
        # pegando os rects para alinhar o texto no centro da tela
        game_over_rect = game_over_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2.5))
        continue_rect = continue_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(continue_text, continue_rect)
        self.snake.reset()    

    def _fade_screen(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 100))  # seta cor preta e o alpha em 100
        self.screen.blit(surf, (0, 0))  # desenha a superfície na tela

    def _generate_map_positions(self):
        # Mapeia todas as posições possíveis considerando o tamanho do bloco
        number_x_positions = self.WIDTH // self.BLOCK_SIZE
        number_y_positions = self.HEIGHT // self.BLOCK_SIZE
        map_positions = set()
        for x in range(number_x_positions):
            for y in range(number_y_positions):
                position = (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE)
                map_positions.add(position)
        return map_positions

    def _generate_apple_position(self):
        # Seleciona uma posição aleatória do mapa onde a cobra não esteja
        available_positions = self.map_positions - set(self.snake.body)
        return random.choice(
            list(available_positions)
        )  # Usando apenas available_positions.pop() os valores costumavam repetir

    def _draw_grid(self):
        number_x_positions = self.WIDTH // self.BLOCK_SIZE
        number_y_positions = self.HEIGHT // self.BLOCK_SIZE
        for x in range(number_x_positions):
            for y in range(number_y_positions):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(
                        self.screen,
                        self.SKYBLUE,
                        (
                            x * self.BLOCK_SIZE,
                            y * self.BLOCK_SIZE,
                            self.BLOCK_SIZE,
                            self.BLOCK_SIZE,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        self.STEELBLUE,
                        (
                            x * self.BLOCK_SIZE,
                            y * self.BLOCK_SIZE,
                            self.BLOCK_SIZE,
                            self.BLOCK_SIZE,
                        ),
                    )


if __name__ == "__main__":
    game = Game()
    game.run()
