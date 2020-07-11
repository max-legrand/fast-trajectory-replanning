#!/usr/bin/env pipenv run python
'''
file:           sizes.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   Determines the size of a full dictionary, list, 
                and total size of search object
'''
import sys
from math import sqrt

total_cells = input("Enter total cells: ")
total_cells = int(total_cells)

listv = []
dictv = {}

for counter in range(0, total_cells):
    dictv[counter] = 1
    listv.append(counter)

total_size = 56 + sys.getsizeof(listv) + 4*sys.getsizeof(dictv)
grid_len = int(sqrt(total_cells))
mb_size = total_size / (10**6)

print(f"{grid_len}x{grid_len} = {total_cells} cells")
print("Start/End size = 56")
print(f"List size = {sys.getsizeof(listv)}")
print(f"Dict size = {sys.getsizeof(dictv)}")
print(f"Total size = {total_size} = {mb_size}Mb")
