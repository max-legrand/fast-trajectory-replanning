#!/usr/bin/env pipenv run python
'''
file:           total_stats.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   Iterates over all grids and generates statistics for runtime
                and cell expansions
'''
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
    """
    Initializes Search object and grid array

    Args:
        grid_obj (2D array): array representing the grid

    Returns:
        Search: initialized search object
    """
    start = (0, 0)
    end = (MAXSIZE-1, MAXSIZE-1)
    grid_obj[start[0]][start[1]] = 2
    grid_obj[end[0]][end[1]] = -1
    obj = Search(start=start, end=end)
    return obj


init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected

cprint(figlet_format('Search Statistics', font='small'),
       'white')


def reset_values(search_object):
    """
    Resets the values of a Search object

    Args:
        search_object (Search): object to reset
    """
    search_object.fvals = {}
    search_object.gvals = {}
    search_object.hvals = {}
    search_object.clset = []
    search_object.prev = {}


def perform_stats(search_type):  # pylint:disable=too-many-statements,too-many-branches
    """
    Performs a specified search for all grids

    Args:
        search_type (String): name of search to performs
    """
    total_valid = 0
    animation = "|/-\\"
    idx = 0
    expanded_cells = 0
    totaltime = 0
    print("===============================================================")

    for grid_num in range(0, 50):
        TIME = 0
        dirname = os.path.dirname(os.path.realpath(__file__))
        file_name = dirname+f"/grids/grid_{grid_num}.txt"
        grid = list(csv.reader(open(file_name)))
        # Cast items in grid to integer
        grid = [[int(col) for col in row] for row in grid]
        path = None
        searchObject = init_grid(grid)
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)

        if search_type == "forward":
            start_time = timeit.default_timer()
            path = searchObject.a_star(grid, True)
            end_time = timeit.default_timer()
            TIME = end_time - start_time

        if search_type == "adaptive":
            searchObject.a_star(grid, True, True)
            for item in searchObject.clset:
                searchObject.hvals[item] = searchObject.fvals[item] - searchObject.gvals[searchObject.end]
            start_time = timeit.default_timer()
            path = searchObject.adap_a_star(grid)
            end_time = timeit.default_timer()
            TIME = end_time - start_time

        if search_type == "forward_high":
            start_time = timeit.default_timer()
            path = searchObject.a_star(grid, True, True)
            end_time = timeit.default_timer()
            TIME = end_time - start_time

        if search_type == "backward":
            start_time = timeit.default_timer()
            path = searchObject.a_star(grid, False)
            end_time = timeit.default_timer()
            TIME = end_time - start_time

        if search_type == "backward_high":
            start_time = timeit.default_timer()
            path = searchObject.a_star(grid, False, True)
            end_time = timeit.default_timer()
            TIME = end_time - start_time

        if path is not None:
            expanded_cells = expanded_cells + len(searchObject.clset)
            total_valid = total_valid + 1
            totaltime = totaltime + TIME
        reset_values(searchObject)

    if search_type == "forward":
        search_string = "Forward A*"
    elif search_type == "adaptive":
        search_string = "Adaptive A*"
    elif search_type == "forward_high":
        search_string = "Forwards A* High G"
    elif search_type == "backward":
        search_string = "Backwards A*"
    elif search_type == "backward_high":
        search_string = "Backwards A* High G"

    avg_val = expanded_cells / total_valid
    avg_time = totaltime / total_valid
    print(f"Average Expanded Cells {search_string}: {avg_val}")
    print(f"Time: {avg_time}")
    print(f"Total valid paths found: {total_valid}")


if __name__ == "__main__":
    perform_stats("forward")
    perform_stats("forward_high")
    perform_stats("adaptive")
    perform_stats("backward")
    perform_stats("backward_high")
