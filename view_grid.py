#!/usr/bin/env pipenv run python
'''
file:           view_grid.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   View grid inside grids folder
'''

import csv
import pygame
import argparse
import timeit
from a_star_search import a_star
from constants import BLACK, WHITE, WINDOW_SIZE, ORANGE, GREEN, MARGIN, HEIGHT, WIDTH, MAXSIZE

time = 0
total_distance = 0
runtime = 0


def clear_screen(grid):
    for row in range(MAXSIZE):
        for col in range(MAXSIZE):
            if grid[row][col] != 1 and grid[row][col] != 2 and grid[row][col] != -1:
                grid[row][col] = 0
                pygame.draw.rect(screen, WHITE, [
                    (MARGIN + WIDTH) * col + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN,
                    WIDTH,
                    HEIGHT
                ])
    pygame.display.flip()
    global time
    global total_distance
    time = 0
    total_distance = 0
    print('Cleared')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='View a grid')
    parser.add_argument('--grid',
                        help='number of grid to view',
                        required=True)

    args = parser.parse_args()
    grid_num = args.grid

    file_name = f"grids/grid_{grid_num}.txt"
    grid = list(csv.reader(open(file_name)))
    grid = [[int(col) for col in row] for row in grid]

    start = (0, 0)
    end = (MAXSIZE-1, MAXSIZE-1)

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("A Star")

    finish = False
    clock_obj = pygame.time.Clock()

    for row in range(MAXSIZE):
        for col in range(MAXSIZE):
            if grid[row][col] == 1:
                color = BLACK
            else:
                color = WHITE

            pygame.draw.rect(screen, color, [
                (MARGIN + WIDTH) * col + MARGIN,
                (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT
            ])

            if grid[row][col] == 2:
                color = GREEN
                pygame.draw.rect(screen, color, [
                    (MARGIN + WIDTH) * col + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT
                ])

            if grid[row][col] == -1:
                color = ORANGE
                pygame.draw.rect(screen, color, [
                    (MARGIN + WIDTH) * col + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT
                ])
    # Draw board
    pygame.display.flip()

    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    clear_screen(grid)

                elif event.key == pygame.K_a:
                    clear_screen(grid)
                    start_time = timeit.default_timer()
                    path = a_star(start, end, screen, grid)
                    end_time = timeit.default_timer()
                    pygame.display.flip()
                    time = end_time - start_time
                    if path is not None:
                        print(f"Forward A*: \nTotal time: {time} seconds\nTotal distance: {len(path)}")
        pygame.display.flip()
    pygame.quit()
