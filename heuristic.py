# -----------------------------------------------------------
# heuristic.py 22/01/20
#
# Define heuristic functionality available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
from typing import List

import numpy
from numpy.core.multiarray import ndarray

import constant
from constant import Node


def get_heuristic(heuristic_algorithm: str, grid: numpy.ndarray, path: List[str]):
    """
    Get h(n) for a given Node, given the heuristic algorithm
    :param heuristic_algorithm: Algorithm used to calculate heuristic
    :param grid: 2D numpy array representation of the state
    :param path: Path from root to the given state
    :return: h(n)
    """
    if heuristic_algorithm == constant.ZERO_HEURISTIC:
        return 0
    elif heuristic_algorithm == constant.COUNT_HEURISTIC:
        return get_total_count_heuristic(grid)
    elif heuristic_algorithm == constant.DIV_BY_5_HEURISTIC:
        return get_div_by_5_heuristic(grid)
    elif heuristic_algorithm == constant.NO_DOUBLE_PRESS_HEURISTIC:
        return get_no_double_press_heuristic(grid, path)

    return 0


def get_total_count_heuristic(grid: ndarray):
    """
    Count total number of black pegs on the board.
    :param (ndarray) grid: 2D numpy array
    :return: heuristic value of the grid
    """
    count = 0
    for x, y in numpy.ndindex(grid.shape):
        count += 1 if grid[x, y] == 1 else 0
    return count


def get_div_by_5_heuristic(grid: ndarray):
    """
    Count total number of black pegs on the board and divide by 5.
    :param (ndarray) grid: 2D numpy array
    :return: the value of heuristics
    """
    return get_total_count_heuristic(grid) / 5


# TODO
def get_no_double_press_heuristic(grid: ndarray, path: List[str]):
    pass
