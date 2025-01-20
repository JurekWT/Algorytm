import math
import pandas as pd
import heapq as hp
import pygame
import sys
import time

##Sekcja z funkcjami PyGame
pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont('Arial', 50)


def draw_grid(win):
    for x in range(0, WIDTH, SQUARE_SIZE):
        for y in range(0, HEIGHT, SQUARE_SIZE):
            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, GREY, rect, 1)


def draw(win, grid, path, start, end, open_list, closed_list, message=None):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE
            if grid.at[(row, col)] == 5:
                color = RED
            elif (row, col) == start:
                color = GREEN
            elif (row, col) == end:
                color = BLUE
            elif closed_list and (row, col) in closed_list:
                color = BLACK
            elif open_list and (row, col) in [i[2] for i in open_list]:
                color = GREY
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    for (row, col) in path:
        pygame.draw.rect(win, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    draw_grid(win)

    if message:
        text = FONT.render(message, True, BLUE)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.update()


def get_clicked_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


## Algorytm A*

def find_route(grid, start, end):
    open_list = []
    closed_list = []
    came_from = {}
    g_value = {start: 0}
    f_value = {start: heur(g_value[start], start, end)}
    hp.heappush(open_list, (0, 0, start))
    counter = 0
    while open_list:
        _, _, current = hp.heappop(open_list)

        if current == end:
            route = []
            while current in came_from:
                route.append(current)
                current = came_from[current]
            route.append(start)
            route.reverse()
            return route

        closed_list.append(current)
        neighbors = get_neighbors(grid, current)

        for neighbor in neighbors:
            if neighbor in closed_list:
                continue

            g_check = g_value[current] + 1
            if neighbor not in g_value or g_check < g_value[neighbor]:
                came_from[neighbor] = current
                g_value[neighbor] = g_value[current] + 1
                f_value[neighbor] = heur(g_value[neighbor], neighbor, end)
                counter += -1
                hp.heappush(open_list, (f_value[neighbor], counter, neighbor))
        yield open_list, closed_list, came_from

    yield None, None, None


def get_neighbors(g, current):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor = current[0] + dx, current[1] + dy
        if ((0 <= neighbor[0] <= 19) and (0 <= neighbor[1] <= 19)) and g.at[neighbor] != 5:
            neighbors.append(neighbor)
    return neighbors


def set_start(x, y):
    start = (x, y)
    return start


def set_end(x, y):
    end = (x, y)
    return end


def heur(g, current, end):
    heurs = g + math.sqrt((current[0] - end[0]) ** 2 + (current[1] - end[1]) ** 2)
    return heurs


grid = pd.read_csv('grid.txt', sep=' ', header=None)
startLocation = set_start(19, 0)
endLocation = set_end(0, 19)
print(find_route(grid, startLocation, endLocation))
path = find_route(grid, startLocation, endLocation)

## Pętla gui

running = True
path_generator = find_route(grid, startLocation, endLocation)
path = []
message = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:  # Lewy klik
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos)
            startLocation = set_start(row, col)
            path_generator = find_route(grid, startLocation, endLocation)
            path = []
            message = None
        if pygame.mouse.get_pressed()[2]:  # Prawy klik
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos)
            endLocation = set_end(row, col)
            path_generator = find_route(grid, startLocation, endLocation)
            path = []
            message = None

    try:
        open_list, closed_list, came_from = next(path_generator)
        if open_list is None:
            message = "Nie można znaleźć ścieżki do celu"
        else:
            path = []
            current = endLocation
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(startLocation)
            path.reverse()
    except StopIteration:
        pass

    draw(WIN, grid, path, startLocation, endLocation, open_list, closed_list, message)
    time.sleep(0.1)
