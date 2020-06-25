#!/usr/bin/env pipenv run python
'''
file:           gen_grid.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   Generates 50 unique grids and outputs files to grids folder
'''

import random

# Defined constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 10
HEIGHT = 10
MARGIN = 5
MAXSIZE = 101
BLOCK_PROBABILITY = 0.3


def get_neighbors(x, y):
    """
    Determines positions of all neighboring elements to provided cell

    Args:
        x (int): x coordinate of current cell
        y (int): y coordinate of current cell

    Returns:
        array : array of tuples containing all neighboring cell locations
    """
    neighbors = []
    # Left neighbor
    x2 = x-1
    y2 = y
    if (-1 < x < MAXSIZE and -1 < y < MAXSIZE and (x != x2 or y != y2) and (0 <= x2 < MAXSIZE) and (0 <= y2 < MAXSIZE)):
        neighbors.append((x2, y2))
    # Right neighbor
    x2 = x+1
    y2 = y
    if (-1 < x < MAXSIZE and -1 < y < MAXSIZE and (x != x2 or y != y2) and (0 <= x2 < MAXSIZE) and (0 <= y2 < MAXSIZE)):
        neighbors.append((x2, y2))
    # Bottom neighbor
    x2 = x
    y2 = y-1
    if (-1 < x < MAXSIZE and -1 < y < MAXSIZE and (x != x2 or y != y2) and (0 <= x2 < MAXSIZE) and (0 <= y2 < MAXSIZE)):
        neighbors.append((x2, y2))
    # Top neighbor
    x2 = x
    y2 = y+1
    if (-1 < x < MAXSIZE and -1 < y < MAXSIZE and (x != x2 or y != y2) and (0 <= x2 < MAXSIZE) and (0 <= y2 < MAXSIZE)):
        neighbors.append((x2, y2))
    return neighbors


def find_unvisited():
    """
    Finds all unvisited cells remaining in the grid

    Returns:
        array: an array of tuples where each pair is the location of an unvitisted cell
    """
    unvisited = []
    for row in range(0, MAXSIZE):
        for col in range(0, MAXSIZE):
            if grid[row][col]["visited"] is False:
                unvisited.append((row, col))
    return unvisited


if __name__ == "__main__":
    # Iterate for 50 grids
    for i in range(1, 51):
        print(f"=== Generating Grid {i} ===")
        grid = []

        # Init grid
        for row in range(0, MAXSIZE):
            grid.append([])
            for col in range(0, MAXSIZE):
                grid[row].append({"visited": False, "unblocked": True, "x": row, "y": col})

        start_cell = (random.randint(0, MAXSIZE-1), random.randint(0, MAXSIZE-1))

        stack = []
        grid[start_cell[0]][start_cell[1]]["visited"] = True

        unvisited = find_unvisited()

        # perform maze generation via depth-first search
        while unvisited != []:
            neighbors = get_neighbors(start_cell[0], start_cell[1])
            while True:
                next_cell = random.choice(neighbors)
                if grid[next_cell[0]][next_cell[1]]["visited"] is False:
                    break
                else:
                    neighbors.remove(next_cell)
                    if neighbors == []:
                        next_cell = None
                        break

            if next_cell is None:
                if stack == []:
                    unvisited = find_unvisited()
                    start_cell = random.choice(unvisited)
                else:
                    start_cell = stack.pop()
            else:
                is_blocked = True if random.random() < BLOCK_PROBABILITY else False
                grid[next_cell[0]][next_cell[1]]["visited"] = True
                if is_blocked:
                    grid[next_cell[0]][next_cell[1]]["unblocked"] = False
                else:
                    stack.insert(0, next_cell)

                if stack == []:
                    unvisited = find_unvisited()
                    start_cell = random.choice(unvisited)
                else:
                    start_cell = stack.pop()
            grid[start_cell[0]][start_cell[1]]["visited"] = True
            unvisited = find_unvisited()
        # write grid to file
        filename = f"grids/grid_{i}.py"
        f = open(filename, "w")
        f.write("from node import node\n")
        f.write("grid = [\n")
        for row in grid:
            f.write("[\n")
            for item in row:
                f.write(f"node(location=({item['x']}, {item['y']}), unblocked={item['unblocked']}),\n")
            f.write("],\n")
        f.write("]")
        f.close()
