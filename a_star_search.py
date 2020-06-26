'''
file:           a_star_search.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   Peforms A* search
'''
from binary_heap import BinaryHeap
from constants import PINK, MARGIN, WIDTH, HEIGHT, PURPLE, MAXSIZE
import pygame


def a_star(start, end, screen, grid):

    close_set = set()  # set has better search performance than list
    previous_nodes = {}

    g_vals = {start: 0}
    f_vals = {start: calc_distance(start, end)}

    open_set = BinaryHeap()

    open_set.insert((f_vals[start], start))

    while open_set.size > 0:

        current_node = open_set.delete_min()[1]

        if current_node == end:
            path = []
            while current_node in previous_nodes:
                pygame.draw.rect(screen, PINK, [
                    (MARGIN + WIDTH) * current_node[1] + MARGIN,
                    (MARGIN + HEIGHT) * current_node[0] + MARGIN, WIDTH, HEIGHT
                ])
                pygame.display.flip()
                path.append(current_node)
                current_node = previous_nodes[current_node]
            return path

        close_set.add(current_node)
        neighbors = get_neighbors(current_node, grid)
        for neighbor in neighbors:
            temp_g_val = g_vals[current_node] + 1

            neighbor_g_val = None
            try:
                neighbor_g_val = g_vals[neighbor]
            except Exception as e:
                neighbor_g_val = 0
                e

            if neighbor in close_set and temp_g_val >= neighbor_g_val:
                continue

            if temp_g_val < neighbor_g_val or neighbor not in [item[1] for item in open_set.heap_array]:
                previous_nodes[neighbor] = current_node
                g_vals[neighbor] = temp_g_val
                f_vals[neighbor] = temp_g_val + calc_distance(neighbor, end)
                if (current_node != start and current_node != end):
                    pygame.draw.rect(screen, PURPLE, [
                        (MARGIN + WIDTH) * current_node[1] + MARGIN,
                        (MARGIN + HEIGHT) * current_node[0] + MARGIN, WIDTH, HEIGHT
                    ])
                pygame.display.flip()
                open_set.insert((f_vals[neighbor], neighbor))
    print("Path not found")
    return None


def calc_distance(pos1, pos2):
    """
    Function to calculate the distance between two cells using delta between x and y
    coordinates (since agent cannot move diagonally)

    Args:
        pos1 (tuple): coordinate tuple of first point
        pos2 (tuple): coordinate tuple of second point

    Returns:
        int: total distance between locations
    """
    x_distance = abs(pos1[0] - pos2[0])
    y_distance = abs(pos1[1] - pos2[1])
    return x_distance + y_distance


def get_neighbors(location, grid):
    neighbors = []
    i = location[0]
    j = location[1]
    if i < MAXSIZE-1 and (grid[i + 1][j] == 0 or grid[i + 1][j] == 2 or grid[i + 1][j] == -1):
        neighbors.append((i + 1, j))
    if i > 0 and (grid[i - 1][j] == 0 or grid[i - 1][j] == 2 or grid[i - 1][j] == -1):
        neighbors.append((i - 1, j))
    if j < MAXSIZE-1 and (grid[i][j + 1] == 0 or grid[i][j + 1] == 2 or grid[i][j + 1] == -1):
        neighbors.append((i, j + 1))
    if j > 0 and (grid[i][j - 1] == 0 or grid[i][j - 1] == 2 or grid[i][j - 1] == -1):
        neighbors.append((i, j - 1))
    return neighbors
