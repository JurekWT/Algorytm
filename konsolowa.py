import math
import subprocess
import pandas as pd
import heapq as hp



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

    return 0

def get_neighbors(g, current):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor = current[0] + dx, current[1] + dy
        if ((0 <= neighbor[0] <= 19) and (0 <= neighbor[1] <= 19)) and g.at[neighbor] != 5:
            neighbors.append(neighbor)
    return neighbors


def set_start(x,y):
    start = (x,y)
    return start

def set_end(x,y):
    end = (x,y)
    return end


def heur(g, current, end):
    heurs = g + math.sqrt((current[0] - end[0]) ** 2 + (current[1] - end[1]) ** 2)
    return heurs

def new_grid():
    subprocess.run(["map_generator.exe"])

generate = input("Wygenerować nową siatkę? (t/n): ")
if generate == "t":
    new_grid()


grid = pd.read_csv('grid.txt', sep=' ', header=None)
startLocation = set_start(19, 0)
endLocation = set_end(0, 19)
path = find_route(grid, startLocation, endLocation)

grid = grid.astype(str)
print("Wczytano mapę:")
print(grid.to_string(header=False, index=False, col_space=2))
if path != 0:
    for node in path:
        grid.at[node] = '*'
    print("Znaleziono ścieżkę!")
    print(grid.to_string(header=False, index=False, col_space=2))
else: print('Nie można znaleźć ścieżki!')
