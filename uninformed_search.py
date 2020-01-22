# -----------------------------------------------------------
# uninformed_search.py 22/01/20
#
# Define set of uninformed search algorithms
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, Comp 472
# All rights reserved.
# -----------------------------------------------------------
import copy
import numpy as np
from utils import flip, get_configuration, get_solution_move, get_search_move, write_results
import constant


def execute_dfs(grid, max_d, goal, puzzle_number):
    """
    Wrapper for DFS
    :param (ndarray) grid: numpy 2-D array
    :param (int) max_d: maximum depth
    :param (string) goal: serialized goal grid
    :param (int) puzzle_number: line number of the puzzle for which DFS is executed
    :return: void
    """
    configuration = get_configuration(grid)
    visited = set()
    search_path = []
    solution_path = ['{}   {}'.format(0, configuration)]
    solution_path = dfs(grid, configuration, visited, search_path, solution_path, max_d, goal)
    write_results(solution_path, search_path, puzzle_number)


def dfs(grid, configuration, visited, search_path, solution_path, max_d, goal):
    """
    Maximum depth DFS
    :param (ndarray) grid: numpy 2-D array
    :param (string) configuration: serialized input grid
    :param (set) visited: previously visited configurations
    :param (list) search_path: close list of searched nodes
    :param (list | string) solution_path: path up to identified solution. List of paths or 'no solution'
    :param (int) max_d: maximum depth
    :param (string) goal: serialized goal grid
    :return (list | string): path up to identified solution. List of paths or 'no solution'
    """
    if configuration == goal:
        search_path.append(get_search_move(constant.DFS, configuration))
        return copy.deepcopy(solution_path)
    if max_d == 0 or configuration in visited:
        return constant.NO_SOLUTION

    visited.add(configuration)
    search_path.append(get_search_move(constant.DFS, configuration))
    ans = constant.NO_SOLUTION

    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == 1 and type(ans) is str:
                grid_copy = np.copy(grid)
                flip(grid_copy, row, col)
                grid_copy_configuration = get_configuration(grid_copy)
                solution_path.append(get_solution_move(row, col, grid_copy_configuration))
                ans = dfs(grid_copy, grid_copy_configuration, visited, search_path, solution_path, max_d - 1, goal)
                solution_path.pop()
    return ans
