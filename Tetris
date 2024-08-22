import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# Configuración de colores
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
colors = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Configuración de la cuadrícula
block_size = 30
cols = screen_width // block_size
rows = screen_height // block_size

# Formas de los Tetrominos
shapes = [
    [[1, 1, 1, 1]],          # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],        # O
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 0], [0, 1, 1]],  # S
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Clase para manejar las piezas
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(colors)
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

def create_grid(locked_positions={}):
    grid = [[black for _ in range(cols)] for _ in range(rows)]

    for y in range(rows):
        for x in range(cols):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    shape_format = piece.image()

    # Convertir la forma a una lista de listas si no lo es
    if isinstance(shape_format[0], int):
        shape_format = [shape_format]

    for y, line in enumerate(shape_format):
        for x, block in enumerate(line):
            if block == 1:
                positions.append((piece.x + x, piece.y + y))

    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(cols) if grid[y][x] == black] for y in range(rows)]
    accepted_positions = [x for sub in accepted_positions for x in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    shape = Piece(5, 0, random.choice(shapes))
    return shape

def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    label = font.render(text, 1, color)

    surface.blit(label, (screen_width / 2 - (label.get_width() / 2), screen_height / 2 - (label.get_height() / 2)))

def draw_grid(surface, grid):
    for y in range(rows):
        for x in range(cols):
            pygame.draw.rect(surface, grid[y][x], (x * block_size, y * block_size, block_size, block_size))
            pygame.draw.line(surface, gray, (0, y * block_size), (screen_width, y * block_size))
            pygame.draw.line(surface, gray, (x * block_size, 0), (x * block_size, screen_height))

def clear_rows(grid, locked):
    increment = 0
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        if black not in row:
            increment += 1
            for x in range(cols):
                if (x, y) in locked:
                    del locked[(x, y)]
            for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
                x, y = key
                if y < y:
                    new_key = (x, y + 1)
                    locked[new_key] = locked.pop(key)
    return increment

def draw_next_shape(piece, surface):
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render("Next Shape", 1, white)

    sx = screen_width + 50
    sy = screen_height / 2 - 100
    shape_format = piece.image()

    # Convertir la forma a una lista de listas si no lo es
    if isinstance(shape_format[0], int):
        shape_format = [shape_format]

    for y, line in enumerate(shape_format):
        for x, block in enumerate(line):
            if block == 1:
                pygame.draw.rect(surface, piece.color, (sx + x * block_size, sy + y * block_size, block_size, block_size))

    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, grid, score=0):
    surface.fill(black)

    font = pygame.font.Font(pygame.font.get_default_font(), 60)
    label = font.render("Tetris", 1, white)

    surface.blit(label, (screen_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render(f"Score: {score}", 1, white)

    sx = screen_width + 50
    sy = screen_height / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    draw_grid(surface, grid)

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(screen, grid, score)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("YOU LOST", 40, white, screen)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

    pygame.display.quit()

def main_menu():
    run = True
    while run:
        screen.fill(black)
        draw_text_middle("Press Any Key To Play", 40, white, screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
                run = False
    pygame.quit()

main_menu()
