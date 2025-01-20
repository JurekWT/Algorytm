import math
import pandas as pd
import pygame


class Node:
    def __init__(self, coord, parent=None, f_value=None, g_value=None, counter=None):
        self.coord = coord
        self.parent = parent
        self.f_value = f_value
        self.g_value = g_value
        self.counter = counter

    def __lt__(self, other):
        if self.f_value == other.f_value:
            return self.counter < other.counter
        return self.f_value < other.f_value


def algorithm(grid, start, end, win, cell_size):
    open_list = []
    closed_list = []
    counter = 0
    open_list.append(Node(start, f_value=0, g_value=0, counter=counter))

    while open_list:
        open_list.sort()
        current = open_list.pop(0)
        closed_list.append(current)

        # Visualization
        draw_grid(win, grid, cell_size, open_list, closed_list, start, end)

        for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT'):
            g_value = current.g_value + 1
            counter += 1  # Increment counter
            neighbor_coord = get_neighbours(current.coord, direction)

            # Check if the neighbor is within bounds and not a wall
            if not (0 <= neighbor_coord[0] < grid.shape[0] and 0 <= neighbor_coord[1] < grid.shape[1]):
                continue
            if not check_wall(grid, neighbor_coord):
                continue

            neighbor = Node(neighbor_coord, parent=current, g_value=g_value)
            neighbor.f_value = calc_f(neighbor.g_value, neighbor.coord, end)

            if neighbor.coord == end:
                path = []
                while neighbor:
                    path.insert(0, neighbor.coord)
                    neighbor = neighbor.parent
                return path

            if any(neighbor.coord == node.coord for node in closed_list):
                continue
            if any(neighbor.coord == node.coord and neighbor.f_value >= node.f_value for node in open_list):
                continue

            neighbor.counter = counter
            open_list.append(neighbor)

    return None


def get_neighbours(coord, direction):
    x, y = coord
    if direction == 'UP':
        y -= 1
    elif direction == 'DOWN':
        y += 1
    elif direction == 'LEFT':
        x -= 1
    elif direction == 'RIGHT':
        x += 1
    return (x, y)


def check_wall(grid, coord):
    if grid[coord[0], coord[1]] == 5:  # Wall
        return False
    return True


def calc_f(g_value, current, end):
    return g_value + math.sqrt((current[0] - end[0]) ** 2 + (current[1] - end[1]) ** 2)


def draw_grid(win, grid, cell_size, open_list, closed_list, start, end):
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            color = (255, 255, 255)
            if grid[i][j] == 5:  # Wall
                color = (128, 128, 128)
            pygame.draw.rect(win, color, (j * cell_size, i * cell_size, cell_size, cell_size))

    # Draw open list
    for node in open_list:
        pygame.draw.rect(win, (0, 255, 0), (node.coord[1] * cell_size, node.coord[0] * cell_size, cell_size, cell_size))

    # Draw closed list
    for node in closed_list:
        pygame.draw.rect(win, (255, 0, 0), (node.coord[1] * cell_size, node.coord[0] * cell_size, cell_size, cell_size))

    # Draw start and end
    pygame.draw.rect(win, (0, 0, 255), (start[1] * cell_size, start[0] * cell_size, cell_size, cell_size))  # Start
    pygame.draw.rect(win, (255, 255, 0), (end[1] * cell_size, end[0] * cell_size, cell_size, cell_size))  # End

    pygame.display.update()


def visualize(grid, start, end):
    pygame.init()
    width, height = 800, 800
    rows, cols = grid.shape
    cell_size = width // cols

    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("A* Algorithm Visualization")

    clock = pygame.time.Clock()  # Create the clock object to control the frame rate
    run = True
    path = None
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_x // cell_size, mouse_y // cell_size

                if event.button == 1:  # Left-click to set start
                    start = (grid_y, grid_x)
                elif event.button == 3:  # Right-click to set end
                    end = (grid_y, grid_x)

                # Recalculate the path after setting start or end
                path = algorithm(grid, start, end, win, cell_size)

        # Draw grid and path
        draw_grid(win, grid, cell_size, [], [], start, end)
        if path:
            for coord in path:
                pygame.draw.rect(win, (0, 255, 255), (coord[1] * cell_size, coord[0] * cell_size, cell_size, cell_size))
            pygame.display.update()

        clock.tick(20)  # Control the frame rate (20 FPS in this case)

    pygame.quit()


if __name__ == "__main__":
    # Load grid and set start/end points
    grid = pd.read_csv('grid.txt', sep=' ', header=None).values
    start = (19, 0)
    end = (0, 19)

    # Visualize the result
    visualize(grid, start, end)
