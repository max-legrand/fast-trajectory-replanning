#!/usr/bin/env pipenv run python
'''
file:           gen_grid.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   Generates 50 unique grids and outputs files to grids folder
'''

import random
import csv
from constants import MAXSIZE


if __name__ == "__main__":
    # Iterate for 50 grids
    for grid_num in range(0, 50):
        grid = []
        # Init grids to be all empty
        for row in range(MAXSIZE):
            grid.append([])
            for col in range(MAXSIZE):
                grid[row].append(0)
        # Randomly decide to make each space a wall or empty
        for row in range(MAXSIZE):
            for col in range(MAXSIZE):
                if random.random() < 0.7:
                    # Empty space
                    grid[row][col] = 0
                else:
                    # Wall
                    grid[row][col] = 1

        grid[0][0] = 2  # Start space
        grid[MAXSIZE-1][MAXSIZE-1] = -1  # End space

        # Write to text file
        file_name = f"grids/grid_{grid_num}.txt"
        with open(file_name, 'w') as f:
            csv.writer(f, delimiter=',').writerows(grid)
