#!/usr/bin/env pipenv run python
'''
file:           view_grid.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   View grid inside grids folder
'''

import importlib
import pygame
import argparse
from constants import BLACK, WHITE, WINDOW_SIZE, PINK, ORANGE, GREEN, PURPLE, MARGIN, HEIGHT, WIDTH, MAXSIZE

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("MAZE")


def view_grid(grid, ismain=False, start=None, end=None):
    # Initialize pygame
    done = False

    # Draw and update grid
    while not done:
        if not ismain:
            done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill(BLACK)
        for row in range(0, MAXSIZE):
            for column in range(0, MAXSIZE):
                color = WHITE
                try:
                    if grid[row][column].unblocked is False:
                        color = BLACK
                except Exception as e:
                    e
                try:
                    if grid[row][column].path is True:
                        color = PURPLE
                except Exception as e:
                    e
                try:
                    if grid[row][column].spath is True:
                        color = PINK
                except Exception as e:
                    e
                try:
                    if (row, column) == start:
                        color = GREEN
                except Exception as e:
                    e
                try:
                    if (row, column) == end:
                        color = ORANGE
                except Exception as e:
                    e
                pygame.draw.rect(
                    screen,
                    color,
                    [(MARGIN + WIDTH) * column + MARGIN,
                        (MARGIN + HEIGHT) * row + MARGIN,
                        WIDTH,
                        HEIGHT])
        pygame.display.update()
    if ismain:
        pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='View a grid')
    parser.add_argument('--grid',
                        help='number of grid to view',
                        required=True)

    args = parser.parse_args()
    grid_num = args.grid

    # Progamatically import grid object from file
    full_module_name = "grids." + f"grid_{grid_num}"
    grid_import = importlib.import_module(full_module_name)
    grid = grid_import.grid
    view_grid(grid, True)
