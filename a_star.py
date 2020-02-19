# -----------------------------------------------------------
# dfs.py 22/01/20
#
# Define and run a* search algorithm
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
from utils import get_puzzle_info, get_configuration


def main(file_path):
    """
    Read file, retrive puzzle info, and execute a* for each puzzle
    :param (string) file_path: relative path the input fule
    :return: void
    """
    with open(file_path) as puzzle_file:
        for puzzle_number, puzzle in enumerate(puzzle_file):
            max_d, max_l, grid, goal = get_puzzle_info(puzzle)


def execute_a_star(grid, goal, max_l, puzzle_number):
    """
    Wrapper function for A*
    :param (ndarray) grid: numpy 2D array representation of the input board.
    :param (string) goal: goal configuration
    :param (int) max_l: maximum search path length
    :param (int) puzzle_number: line number of the puzzle
    :return: void
    """
    print("Executing A* Algorithm with max search length of {} on grid\n{}".format(max_l, grid))
    print("TODO")
