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

parser = argparse.ArgumentParser(description='View a grid')
parser.add_argument('--grid',
                    help='number of grid to view',
                    required=True)

args = parser.parse_args()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 10
HEIGHT = 10
MARGIN = 5
MAXSIZE = 101
WINDOW_SIZE = [500, 500]

grid_num = args.grid

# Progamatically import grid object from file
full_module_name = "grids." + f"grid_{grid_num}"
grid_import = importlib.import_module(full_module_name)
grid = grid_import.grid

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("MAZE")
done = False

# Draw and update grid
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BLACK)
    for row in range(0, 101):
        for column in range(0, 101):
            color = WHITE
            if grid[row][column]["unblocked"] is False:
                color = BLACK
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    pygame.display.flip()
pygame.quit()
