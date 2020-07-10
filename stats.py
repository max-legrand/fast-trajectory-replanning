#!/usr/bin/env pipenv run python
import csv
import sys
import time
import os
import timeit
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


def perform_stats(grid_num):
    dirname = os.path.dirname(os.path.realpath(__file__))
    file_name = dirname+f"/grids/grid_{grid_num}.txt"
    grid = list(csv.reader(open(file_name)))
    # Cast items in grid to integer
    grid = [[int(col) for col in row] for row in grid]
    print("===============================================================")
    print(f"GRID {grid_num} == 10 ITERATIONS")
    print("===============================================================")

    searchObject = init_grid(grid)
    animation = "|/-\\"

    # Forward A
    idx = 0
    expanded_cells = 0
    totaltime = 0
    for i in range(0, 10):
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
        start_time = timeit.default_timer()
        searchObject.a_star(grid, True)
        end_time = timeit.default_timer()
        TIME = end_time - start_time
        expanded_cells = expanded_cells + len(searchObject.clset)
        searchObject.fvals = {}
        searchObject.gvals = {}
        searchObject.hvals = {}
        searchObject.clset = []
        searchObject.prev = {}
        totaltime = totaltime + TIME
    avg_val = expanded_cells / 10
    avg_time = totaltime / 10
    print(f"Average Expanded Cells Forward A*: {avg_val}")
    print(f"Time: {avg_time}")

    # Adaptive A
    expanded_cells = 0
    idx = 0
    totaltime = 0
    for i in range(0, 10):
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
        searchObject.a_star(grid, True, True)
        for item in searchObject.clset:
            searchObject.hvals[item] = searchObject.fvals[item] - searchObject.gvals[searchObject.end]
        start_time = timeit.default_timer()
        searchObject.adap_a_star(grid)
        end_time = timeit.default_timer()
        expanded_cells = expanded_cells + len(searchObject.clset)
        searchObject.fvals = {}
        searchObject.gvals = {}
        searchObject.hvals = {}
        searchObject.clset = []
        searchObject.prev = {}
        TIME = end_time - start_time
        totaltime = totaltime + TIME
    avg_val = expanded_cells / 10
    avg_time = totaltime / 10
    print(f"Average Expanded Cells Adaptive A*: {avg_val}")
    print(f"Time: {avg_time}")

    # Forward A High G
    expanded_cells = 0
    idx = 0
    totaltime = 0
    for i in range(0, 10):
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
        start_time = timeit.default_timer()
        searchObject.a_star(grid, True, True)
        end_time = timeit.default_timer()
        expanded_cells = expanded_cells + len(searchObject.clset)
        searchObject.fvals = {}
        searchObject.gvals = {}
        searchObject.hvals = {}
        searchObject.clset = []
        searchObject.prev = {}
        TIME = end_time - start_time
        totaltime = totaltime + TIME
    avg_val = expanded_cells / 10
    avg_time = totaltime / 10
    print(f"Average Expanded Cells Forward A* High G: {avg_val}")
    print(f"Time: {avg_time}")

    # Backwards A
    expanded_cells = 0
    idx = 0
    totaltime = 0
    for i in range(0, 10):
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
        start_time = timeit.default_timer()
        searchObject.a_star(grid, False)
        end_time = timeit.default_timer()
        expanded_cells = expanded_cells + len(searchObject.clset)
        searchObject.fvals = {}
        searchObject.gvals = {}
        searchObject.hvals = {}
        searchObject.clset = []
        searchObject.prev = {}
        TIME = end_time - start_time
        totaltime = totaltime + TIME
    avg_val = expanded_cells / 10
    avg_time = totaltime / 10
    print(f"Average Expanded Cells Backwards A*: {avg_val}")
    print(f"Time: {avg_time}")

    # Backwards A High G
    expanded_cells = 0
    totaltime = 0
    idx = 0
    for i in range(0, 10):
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
        start_time = timeit.default_timer()
        searchObject.a_star(grid, False, True)
        end_time = timeit.default_timer()
        expanded_cells = expanded_cells + len(searchObject.clset)
        searchObject.fvals = {}
        searchObject.gvals = {}
        searchObject.hvals = {}
        searchObject.clset = []
        searchObject.prev = {}
        TIME = end_time - start_time
        totaltime = totaltime + TIME
    avg_val = expanded_cells / 10
    avg_time = totaltime / 10
    print(f"Average Expanded Cells Backwards A* High G: {avg_val}")
    print(f"Time: {avg_time}")


if __name__ == "__main__":
    perform_stats(10)
    perform_stats(25)
    perform_stats(1)
    perform_stats(49)
