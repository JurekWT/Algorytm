import math
import pandas as pd


class Node:
    def __init__(self, coord, parent = None, f_value = None, g_value = None, ftotal = None):
        self.coord = coord
        self.parent = parent
        self.f_value = f_value
        self.g_value = g_value
        self.ftotal = ftotal
    def __str__(self):
        return f'{self.coord}, Parent: {self.parent}, f_value: {self.f_value}, g_value: {self.g_value}'
    def __lt__(self, other):
        if self.f_value == other.f_value:
            return self.ftotal > other.ftotal
        return self.f_value < other.f_value

def algorithm(grid, start, end):
    open_list = []
    closed_list = []
    open_list.append(Node(start, f_value = 0, g_value = 0))
    ftotal = 0

    while open_list:
        open_list = sorted(open_list)
        current = open_list.pop(0)
        closed_list.append(current)


        for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT'):
            g_value = current.g_value + 1
            neighbour = Node(get_neighbours(current.coord, direction), parent = current, g_value= g_value)
            neighbour.f_value = calc_f(neighbour.g_value, neighbour.coord, end)
            ftotal += neighbour.f_value
            neighbour.ftotal = ftotal + calc_f(neighbour.g_value, neighbour.coord, end)
            if neighbour.coord == end:
                path = []
                while neighbour:
                    path.insert(0, neighbour.coord)
                    neighbour = neighbour.parent
                return path

            if neighbour.coord in (node.coord for node in closed_list):
                continue
            if any(neighbour.coord == node.coord and neighbour.f_value >= node.f_value for node in open_list):
                continue
            if (0 <= neighbour.coord[0] < grid.shape[0] and 0 <= neighbour.coord[1] < grid.shape[1]) and check_wall(grid, neighbour.coord):
                open_list.append(neighbour)
    return 0


def get_neighbours(coord, direction):
    x, y = coord
    if direction == 'UP':
        x += -1
    elif direction == 'DOWN':
        x += +1
    elif direction == 'LEFT':
        y += -1
    elif direction == 'RIGHT':
        y += +1
    return (x,y)


def check_wall(grid, coord):
    if grid.at[coord] == 5:
        return False
    else:
        return True

def calc_f(g_value, current, end):
    f = g_value + math.sqrt((current[0] - end[0]) ** 2 + (current[1] - end[1]) ** 2)
    return f

def set_start(x, y):
    start = (x, y)
    return start

def set_end(x, y):
    end = (x, y)
    return end

grid = pd.read_csv('grid.txt', sep=' ', header=None)
start = set_start(19,0)
end = set_end(0,19)
path = algorithm(grid, start, end)

grid = grid.astype(str)
print("Wczytano mapę:")
print(grid.to_string(header=False, index=False, col_space=2))
if path != 0:
    for node in path:
        grid.at[node] = '*'
    print("Znaleziono ścieżkę!")
    print(grid.to_string(header=False, index=False, col_space=2))
else: print('Nie można znaleźć ścieżki!')
