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
from a_star_search import a_star
from constants import BLACK, WHITE, WINDOW_SIZE, ORANGE, GREEN, MARGIN, HEIGHT, WIDTH, MAXSIZE
from focus import focus_app

globals_obj = {}
globals_obj["time"] = 0
globals_obj["total_distance"] = 0
globals_obj["runtime"] = 0
globals_obj["start"] = (0, 0)
globals_obj["end"] = (MAXSIZE-1, MAXSIZE-1)


def clear_screen(grid_obj, global_obj):
    """
    Clear current screen

    Args:
        grid_obj (2D array): grid object
        global_obj (Global): global object
    """
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


def init_grid(grid_obj, rand, globals_object):
    """
    Initialize grid

    Args:
        grid_obj (2D array): 2D array representing grid object
    """
    # Initialize grid GUI
    if rand:
        grid[0][0] = 0 if random.random() < 0.7 else 1
        grid[MAXSIZE-1][MAXSIZE-1] = 0 if random.random() < 0.7 else 1
        globals_object["start"] = (random.randint(0, MAXSIZE-1), random.randint(0, MAXSIZE-1))
        globals_object["end"] = (random.randint(0, MAXSIZE-1), random.randint(0, MAXSIZE-1))
        grid[globals_object["start"][0]][globals_object["start"][1]] = 2
        grid[globals_object["end"][0]][globals_object["end"][1]] = -1
    else:
        globals_object["start"] = (0, 0)
        globals_object["end"] = (MAXSIZE-1, MAXSIZE-1)

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

    init_grid(grid, args.rand, globals_obj)

    while not ISDONE:
        for event in pygame.event.get():
            # If user clicks exit
            if event.type == pygame.QUIT:
                ISDONE = True

            # If user clicks a key
            if event.type == pygame.KEYDOWN:
                # Clear screen on space
                if event.key == pygame.K_SPACE:
                    clear_screen(grid, globals_obj)
                # Perform search on "a"
                elif event.key == pygame.K_a:
                    clear_screen(grid, globals_obj)
                    start_time = timeit.default_timer()
                    path = a_star(globals_obj["start"], globals_obj["end"], screen, grid)
                    end_time = timeit.default_timer()
                    pygame.display.flip()
                    TIME = end_time - start_time
                    if path is not None:
                        print(f"Forward A*: \nRuntime: {TIME} seconds\nPath Length: {len(path)}")
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
                    init_grid(grid, args.rand, globals_obj)

                    if args.mac:
                        focus_app("Python")

                # disable / enable random
                elif event.key == pygame.K_r:
                    args.rand = not args.rand

        pygame.display.flip()
    pygame.quit()
