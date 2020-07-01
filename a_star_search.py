#!/usr/bin/python
'''
file:           a_star_search.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   Peforms A* search and returns results
'''
from heapq import heappush, heappop
from constants import MAXSIZE

class Search:

    def __init__(self, start, end):
        """
        Constructor for search class

        Args:
            start (tuple): start location for search
            end (tuple): end location for search
        """
        super().__init__()
        self.fvals = {}
        self.start = start
        self.end = end
        self.gvals = {}
        self.hvals = {}
        self.clset = []
        self.prev = {}

    def a_star(self, grid, forwards):
        """
        Perform A* search

        Args:
            grid (2D array): grid object
            forwards (bool): flag for whether to perform forwards search

        Returns:
            list: path taken from start to end
        """

        start = self.start
        end = self.end

        close_set = []
        previous_nodes = {}
        open_set = []

        if forwards:
            g_vals = {start: 0}
            f_vals = {start: calc_distance(start, end)}
            heappush(open_set, (f_vals[start], start))
        else:
            g_vals = {end: 0}
            f_vals = {end: calc_distance(start, end)}
            heappush(open_set, (f_vals[end], end))


        while len(open_set) > 0:

            current_node = heappop(open_set)[1]

            if (current_node == end and forwards) or (current_node == start and not forwards):
                close_set.append(current_node)
                path = []
                while current_node in previous_nodes:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                self.prev = previous_nodes
                return path

            close_set.append(current_node)
            neighbors = get_neighbors(current_node, grid)
            for neighbor in neighbors:

                temp_g_val = g_vals[current_node] + 1

                neighbor_g_val = None
                try:
                    neighbor_g_val = g_vals[neighbor]
                except KeyError as ex:
                    neighbor_g_val = 0
                    ex = str(ex) + "Key not found"

                if ((neighbor not in close_set or temp_g_val < neighbor_g_val) and
                    (temp_g_val < neighbor_g_val or neighbor not in [item[1]
                        for item in open_set])):
                    previous_nodes[neighbor] = current_node
                    g_vals[neighbor] = temp_g_val
                    if forwards:
                        f_vals[neighbor] = temp_g_val + calc_distance(neighbor, end)
                    else:
                        f_vals[neighbor] = temp_g_val + calc_distance(neighbor, start)

                    self.hvals[neighbor] = calc_distance(neighbor, start)
                    self.fvals = f_vals
                    self.gvals = g_vals
                    self.clset = close_set
                    heappush(open_set, (f_vals[neighbor], neighbor))

        print("Path not found")
        return None


    def adap_a_star(self, grid, g_vals, parents, iterations, prev_visited, adaptive=False):  # pylint: disable=too-many-arguments, too-many-branches, too-many-locals
        """
        Performs adaptive A* search

        Args:
            grid (2D array): Grid object
            g_vals (dictionary): key=node, value=g
            parents (dictionary): key=node, value=parent node
            iterations (int): number or iterations
            prev_visited (list): list of previously visited nodes
            adaptive (bool, optional): flag for whether to use adaptive h values. Defaults to False.

        Returns:
            list, list: path taken, list of visted nodes
        """
        start = self.start
        end = self.end

        open_list = []
        complete_closed_list = []
        closed_list = []
        maxdistance = MAXSIZE ** 2
        if start not in g_vals:
            g_vals[start] = 0

        heappush(open_list, (0, start))

        while open_list:
            cell = heappop(open_list)
            previous_cell = cell[1]
            current_cell = cell[1]
            previous_cost = g_vals[current_cell]

            if current_cell == end and iterations > 0:
                while iterations > 0:
                    iterations -= 1
                    complete_closed_list.append(cell)
                    closed_list.append(current_cell)
                    path = build_path(parents, end, start)
                    s_goal = len(path)
                    g_vals[1] = s_goal
                    return self.adap_a_star(grid, g_vals, parents, iterations, closed_list, True)

            elif current_cell == end and iterations == 0:
                complete_closed_list.append(cell)
                path = build_path(parents, end, start)
                return path, closed_list

            if current_cell in closed_list:
                continue

            if adaptive and current_cell not in prev_visited:
                continue

            complete_closed_list.append(cell)
            closed_list.append(current_cell)

            neighbors = get_neighbors(current_cell, grid)
            for neighbor in neighbors:
                if neighbor is not start and neighbor not in closed_list:
                    new_g_score = previous_cost + 1

                    if neighbor in g_vals and g_vals[neighbor] < new_g_score:
                        pass
                    else:
                        g_vals[neighbor] = new_g_score
                        parents[neighbor] = previous_cell

                    if adaptive:
                        h_score = g_vals[1] - g_vals[neighbor]
                    else:
                        h_score = calc_distance(neighbor, end)

                    f_score = h_score * maxdistance - g_vals[neighbor]
                    parents[neighbor] = current_cell
                    heappush(open_list, (f_score, neighbor))

        return "No Path Exists"


def calc_distance(pos1, pos2):
    """
    Function to calculate the distance between two cells using delta between x and y
    coordinates (since agent cannot move diagonally)

    Args:
        pos1 (tuple): coordinate tuple of first point
        pos2 (tuple): coordinate tuple of second point

    Returns:
        int: total distance between locations
    """
    x_distance = abs(pos1[0] - pos2[0])
    y_distance = abs(pos1[1] - pos2[1])
    return x_distance + y_distance


def get_neighbors(location, grid):
    """
    Finds all neighboring cells

    Args:
        location (tuple): row and column of cell to find neighbors of
        grid (2D array): grid object

    Returns:
        array: list of neighbor tuples
    """
    neighbors = []
    i = location[0]
    j = location[1]
    if i < MAXSIZE-1 and (grid[i + 1][j] == 0 or grid[i + 1][j] == 2 or grid[i + 1][j] == -1):
        neighbors.append((i + 1, j))
    if i > 0 and (grid[i - 1][j] == 0 or grid[i - 1][j] == 2 or grid[i - 1][j] == -1):
        neighbors.append((i - 1, j))
    if j < MAXSIZE-1 and (grid[i][j + 1] == 0 or grid[i][j + 1] == 2 or grid[i][j + 1] == -1):
        neighbors.append((i, j + 1))
    if j > 0 and (grid[i][j - 1] == 0 or grid[i][j - 1] == 2 or grid[i][j - 1] == -1):
        neighbors.append((i, j - 1))
    return neighbors


def build_path(parent_nodes, end, start):
    """
    Builds path from list of nodes

    Args:
        parent_nodes (dictionary): key=node, value=parent node
        end (tuple): end location
        start (tuple): start location

    Returns:
        array: path of nodes taken
    """
    current = end
    parent = parent_nodes[current]
    path = [parent]

    while parent is not start:
        temp = parent
        parent = parent_nodes[temp]
        path.append(parent)
    return path
