#!/usr/bin/env pipenv run python
'''
file:           view_grid.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   View grid inside grids folder and perform searches
'''

import csv
import argparse
import timeit
import random
import pygame
from mods.a_star_search import Search
from mods.constants_vals import BLACK, WHITE, PURPLE, PINK, WINDOW_SIZE, ORANGE, GREEN, MARGIN, HEIGHT, WIDTH, MAXSIZE
from mods.focus import focus_app

globals_obj = {}
globals_obj["time"] = 0
globals_obj["total_distance"] = 0


def clear_screen(grid_obj, global_obj, searchObj):
    """
    Clear current screen

    Args:
        grid_obj (2D array): grid object
        global_obj (Global): global object
        searchObj (Search): search object
    """
    searchObj.fvals = {}
    searchObj.gvals = {}
    searchObj.hvals = {}
    searchObj.clset = []
    searchObj.prev = {}
    for row in range(MAXSIZE):
        for cols in range(MAXSIZE):
            if grid_obj[row][cols] != 1 and grid_obj[row][cols] != 2 and grid_obj[row][cols] != -1:
                grid_obj[row][cols] = 0
                pygame.draw.rect(screen, WHITE, [
                    (MARGIN + WIDTH) * cols + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN,
                    WIDTH,
                    HEIGHT
                ])
    pygame.display.flip()

    global_obj["time"] = 0
    global_obj["total_distance"] = 0
    print('Cleared screens')
    return searchObj


def init_grid(grid_obj, rand):
    """
    Initialize grid

    Args:
        grid_obj (2D array): 2D array representing grid object
        rand (bool): flag for randomizing start and end

    Return:
        Search: returns a search object with proper start and end points
    """
    # Initialize grid GUI
    if rand:
        grid_obj[0][0] = 0 if random.random() < 0.7 else 1
        grid_obj[MAXSIZE-1][MAXSIZE-1] = 0 if random.random() < 0.7 else 1
        start = (random.randint(0, MAXSIZE-1), random.randint(0, MAXSIZE-1))
        end = (random.randint(0, MAXSIZE-1), random.randint(0, MAXSIZE-1))

    else:
        start = (0, 0)
        end = (MAXSIZE-1, MAXSIZE-1)

    grid_obj[start[0]][start[1]] = 2
    grid_obj[end[0]][end[1]] = -1

    for row in range(MAXSIZE):
        for col in range(MAXSIZE):
            if grid_obj[row][col] == 1:
                color = BLACK
            else:
                color = WHITE
            # Draw cells with proper colors
            pygame.draw.rect(screen, color, [
                (MARGIN + WIDTH) * col + MARGIN,
                (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT
            ])

            if grid_obj[row][col] == 2:
                color = GREEN
                pygame.draw.rect(screen, color, [
                    (MARGIN + WIDTH) * col + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT
                ])

            if grid_obj[row][col] == -1:
                color = ORANGE
                pygame.draw.rect(screen, color, [
                    (MARGIN + WIDTH) * col + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT
                ])
    # Draw board
    pygame.display.flip()
    obj = Search(start=start, end=end)
    return obj


def draw_path(type_search, pathlist, searchobj, close_set=None):
    """
    Draw path with pygame

    Args:
        type_search (String): Type of search
        pathlist (list): list of nodes to color
        searchobj (Search): object containing start and end (sometimes close_list)
        close_set (list, optional): Provided closed list to color. Defaults to None.
    """
    if path is not None:
        if close_set is not None:
            searchobj.clset = close_set

        print(f"{type_search}: \nRuntime: {TIME} seconds\nPath Length: {len(path)}")
        print(f"Expanded: {len(searchObject.clset)}")

        for cell_item in searchobj.clset:
            if cell_item not in (searchobj.start, searchobj.end):
                pygame.draw.rect(screen, PURPLE, [
                    (MARGIN + WIDTH) * cell_item[1] + MARGIN,
                    (MARGIN + HEIGHT) * cell_item[0] + MARGIN, WIDTH, HEIGHT
                ])
        for cell_item in pathlist:
            if cell_item not in (searchobj.start, searchobj.end):
                pygame.draw.rect(screen, PINK, [
                    (MARGIN + WIDTH) * cell_item[1] + MARGIN,
                    (MARGIN + HEIGHT) * cell_item[0] + MARGIN, WIDTH, HEIGHT
                ])
    pygame.display.flip()


if __name__ == "__main__":
    # Get grid number from command line
    parser = argparse.ArgumentParser(description='View a grid')
    parser.add_argument('--grid',
                        help='number of grid to view',
                        required=True)
    parser.add_argument('--mac', action='store_true', help="Flag if using Mac OS and VsCode")
    parser.add_argument('--rand', action='store_true', help="Flag for randomizing start and end")

    args = parser.parse_args()
    grid_num = args.grid

    # Import grid from file
    file_name = f"grids/grid_{grid_num}.txt"
    grid = list(csv.reader(open(file_name)))
    # Cast items in grid to integer
    grid = [[int(col) for col in row] for row in grid]

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("A Star")

    ISDONE = False
    clock_obj = pygame.time.Clock()

    searchObject = init_grid(grid, args.rand)

    while not ISDONE:
        for event in pygame.event.get():
            # If user clicks exit
            if event.type == pygame.QUIT:
                ISDONE = True

            # If user clicks a key
            if event.type == pygame.KEYDOWN:

                # Clear screen on space
                if event.key == pygame.K_SPACE:
                    searchObject = clear_screen(grid, globals_obj, searchObject)

                # Perform forward search on "f"
                elif event.key == pygame.K_f:
                    searchObject = clear_screen(grid, globals_obj, searchObject)
                    start_time = timeit.default_timer()
                    path = searchObject.a_star(grid, True)
                    end_time = timeit.default_timer()
                    TIME = end_time - start_time
                    draw_path("Forward A*", path, searchObject)

                # Perform backwards search on "b"
                elif event.key == pygame.K_b:
                    searchObject = clear_screen(grid, globals_obj, searchObject)
                    start_time = timeit.default_timer()
                    path = searchObject.a_star(grid, False)
                    end_time = timeit.default_timer()
                    TIME = end_time - start_time
                    draw_path("Backwards A*", path, searchObject)

                # Perform adaptive search on "a"
                elif event.key == pygame.K_a:
                    searchObject = clear_screen(grid, globals_obj, searchObject)
                    # Load F-Values
                    path = searchObject.a_star(grid, True)
                    for item in searchObject.clset:
                        searchObject.hvals[item] = searchObject.fvals[item] - searchObject.gvals[searchObject.end]
                    start_time = timeit.default_timer()
                    # path, closed_list = searchObject.adap_a_star(grid, searchObject.gvals, {}, 2, None)
                    path, closed_list = searchObject.adap_a_star(grid)
                    end_time = timeit.default_timer()
                    TIME = end_time - start_time
                    draw_path("Adaptive A*", path, searchObject)

                # Perform backwards search -- high g on "r""
                elif event.key == pygame.K_r:
                    searchObject = clear_screen(grid, globals_obj, searchObject)
                    start_time = timeit.default_timer()
                    path = searchObject.a_star(grid, False, True)
                    end_time = timeit.default_timer()
                    TIME = end_time - start_time
                    draw_path("Backwards A* High G", path, searchObject)

                # Perform forwards search -- high g on "e"
                elif event.key == pygame.K_e:
                    searchObject = clear_screen(grid, globals_obj, searchObject)
                    # Load F-Values
                    start_time = timeit.default_timer()
                    path = searchObject.a_star(grid, True, True)
                    end_time = timeit.default_timer()
                    TIME = end_time - start_time
                    draw_path("Forwards A* High G", path, searchObject)

                # Change grid
                elif event.key == pygame.K_c:
                    if args.mac:
                        focus_app("Electron")

                    grid_num = input("Enter grid number: ")
                    # Import grid from file
                    file_name = f"grids/grid_{grid_num}.txt"
                    grid = list(csv.reader(open(file_name)))
                    # Cast items in grid to integer
                    grid = [[int(col) for col in row] for row in grid]
                    searchObject = init_grid(grid, args.rand)

                    if args.mac:
                        focus_app("Python")

                # disable / enable random
                elif event.key == pygame.K_r:
                    args.rand = not args.rand

        pygame.display.flip()
    pygame.quit()
