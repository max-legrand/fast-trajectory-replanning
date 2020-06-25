#!/usr/bin/env pipenv run python
'''
file:           a_star.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   Peforms A* search
'''

# TODO: Implement Binary heap
# TODO: Use Binary heap instead of list for openList
# TODO: Repeated A*

import random
import importlib
from gen_grid import MAXSIZE
import view_grid
import pygame


def find_in_list(find_list, location):
    """
    Funciton to determine if location value is present in a list of nodes

    Args:
        find_list (array): list to search
        location (tuple): coordinate tuple to search for in list

    Returns:
        node: returns a node if found, None otherwise
    """
    try:
        return next(item for item in find_list if location == item.location)
    except StopIteration:
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


def a_star(grid, start, end):
    """
    Performs A* search

    Args:
        grid (2D array): Array representation of the grid
        start (Tuple): tuple containing x and y coordinates of start position
        end (Tuple): tuple containing x and y coordinates of end position
    """
    openList = []
    closedList = []
    startNode = grid[start[0]][start[1]]
    endNode = grid[end[0]][end[1]]
    path = []
    for counter1 in range(MAXSIZE):
        for counter2 in range(MAXSIZE):
            grid[counter1][counter2].addNeighbors(grid)

    openList.append(startNode)

    while len(openList) > 0:
        for cell in closedList:
            grid[cell.location[0]][cell.location[1]].path = True
        view_grid.view_grid(grid=grid, start=start, end=end)

        smallest_f_index = 0
        for counter in range(len(openList)):
            if openList[counter].f < openList[smallest_f_index].f:
                smallest_f_index = counter

        currentNode = openList[smallest_f_index]
        if currentNode == endNode:
            for i in range(round(currentNode.f)):
                currentNode.closed = False
                currentNode.path = True
                currentNode = currentNode.previous
                path.append(currentNode)
            return path
        openList.pop(smallest_f_index)
        closedList.append(currentNode)

        neighbors = currentNode.neighbors
        for counter in range(len(neighbors)):
            neighbor = neighbors[counter]
            if neighbor not in closedList:
                gval = currentNode.g + 1
                if neighbor in openList:
                    if neighbor.g > gval:
                        neighbor.g = gval
                else:
                    neighbor.g = gval
                    openList.append(neighbor)

            neighbor.h = calc_distance(neighbor.location, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous is None:
                neighbor.previous = currentNode
    currentNode.closed = True


if __name__ == "__main__":

    grid_num = random.randint(1, 50)
    print(f"Using grid {grid_num}")
    full_module_name = "grids." + f"grid_{grid_num}"
    grid_import = importlib.import_module(full_module_name)
    grid = grid_import.grid

    start = (random.randint(0, 100), random.randint(0, 100))
    while grid[start[0]][start[1]].unblocked is False:
        start = (random.randint(0, 100), random.randint(0, 100))

    end = (random.randint(0, 100), random.randint(0, 100))
    while grid[end[0]][end[1]].unblocked is False and end != start:
        end = (random.randint(0, 100), random.randint(0, 100))

    print(f"Starting at: {start[0]}, {start[1]}")
    print(f"Ending at: {end[0]}, {end[1]}")
    print("Calculating path...")

    pygame.init()
    screen = pygame.display.set_mode(view_grid.WINDOW_SIZE)
    pygame.display.set_caption("MAZE")
    path = a_star(grid, start, end)

    # print(path)

    for cell in path:
        grid[cell.location[0]][cell.location[1]].spath = True

    view_grid.view_grid(grid=grid, start=start, end=end)

    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
                break
    pygame.quit()
