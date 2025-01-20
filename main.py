
class Node:
    def __init__(self, coord, parent = None, f_value = None, g_value = None, counter = None):
        self.coord = coord
        self.parent = parent
        self.f_value = f_value
        self.g_value = g_value
        self.counter = counter
    def __str__(self):
        return f'{self.coord}, Parent: {self.parent}, f_value: {self.f_value}, g_value: {self.g_value}, counter: {self.counter}'
    def __lt__(self, other):
        if self.f_value == other.f_value:
            return self.counter < other.counter
        return self.f_value < other.f_value

start = (0,19)
open_list = []
open_list.append(Node(start, f_value = 0, g_value = 0, counter = 0))
open_list.append(Node((3,19), f_value = 13, g_value = 1, counter = 3))
open_list.append(Node((2,19), f_value = 14, g_value = 2, counter = 2))
open_list.append(Node((1,18), f_value = 13, g_value = 2, counter = 1))
open_list.append(Node((1,18), f_value = 13, g_value = 2, counter = 5))
open_list.append(Node((1,18), f_value = 13, g_value = 2, counter = 0))

open_list = sorted(open_list)
for point in open_list:
    print(point)
