#!/usr/bin/env pipenv run python
import csv
import sys
import time
import os
from termcolor import cprint
from pyfiglet import figlet_format
from colorama import init
from mods.a_star_search import Search
from mods.constants_vals import MAXSIZE


def init_grid(grid_obj):
    start = (0, 0)
    end = (MAXSIZE-1, MAXSIZE-1)
    grid_obj[start[0]][start[1]] = 2
    grid_obj[end[0]][end[1]] = -1
    obj = Search(start=start, end=end)
    return obj


init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected

cprint(figlet_format('Search Statistics', font='small'),
       'white')
print("===============================================================")
dirname = os.path.dirname(os.path.realpath(__file__))
file_name = dirname+"/grids/grid_10.txt"
grid = list(csv.reader(open(file_name)))
# Cast items in grid to integer
grid = [[int(col) for col in row] for row in grid]

searchObject = init_grid(grid)
animation = "|/-\\"
idx = 0
expanded_cells = 0
for i in range(0, 10):
    print(animation[idx % len(animation)], end="\r")
    idx += 1
    time.sleep(0.1)
    # start_time = timeit.default_timer()
    path = searchObject.a_star(grid, True)
    expanded_cells = expanded_cells + len(searchObject.clset)
    searchObject.fvals = {}
    searchObject.gvals = {}
    searchObject.hvals = {}
    searchObject.clset = []
    searchObject.prev = {}
    # end_time = timeit.default_timer()
    # TIME = end_time - start_time
avg_val = expanded_cells / 10
print(f"Average Expanded Cells Forward A*: {avg_val}")
expanded_cells = 0
idx = 0
for i in range(0, 10):
    print(animation[idx % len(animation)], end="\r")
    idx += 1
    time.sleep(0.1)
    # start_time = timeit.default_timer()
    path = searchObject.adap_a_star(grid)
    expanded_cells = expanded_cells + len(searchObject.clset)
    searchObject.fvals = {}
    searchObject.gvals = {}
    searchObject.hvals = {}
    searchObject.clset = []
    searchObject.prev = {}
    # end_time = timeit.default_timer()
    # TIME = end_time - start_time
avg_val = expanded_cells / 10
print(f"Average Expanded Cells Adaptive A*: {avg_val}")
