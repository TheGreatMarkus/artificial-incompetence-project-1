# -----------------------------------------------------------
# main.py 22/01/20
#
# Define main entry to the app
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, Comp 472
# All rights reserved.
# -----------------------------------------------------------
from uninformed_search import execute_dfs
from utils import construct_grid, get_puzzle_info, get_goal_state


def search_puzzle(puzzle, puzzle_number):
    """
    Extract input information and execute search algorithms
    :param (string) puzzle: puzzle information
    :param (int) puzzle_number: line number of the puzzle, 0 -> Inf
    :return: void
    """
    n, max_d, max_l, board = get_puzzle_info(puzzle)
    grid = construct_grid(board, n)
    goal = get_goal_state(n)
    execute_dfs(grid, max_d, goal, puzzle_number)


def main(file_path):
    """
    Read file and execute search for each puzzle
    :param (string) file_path: relative path to the input file
    :return: void
    """
    with open(file_path) as fp:
        for puzzle_number, puzzle in enumerate(fp):
            search_puzzle(puzzle, puzzle_number)


# Define input file here
main('input.txt')
