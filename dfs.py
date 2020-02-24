# -----------------------------------------------------------
# dfs.py 22/01/20
#
# Define and run depth-first search algorithm
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
import constant
from constant import DFS_ALGORITHM
from utils import *
from utils import get_puzzle_info


def main(file_path):
    """
    Read file, retrieve puzzle info, and execute dfs for each puzzle
    :param (string) file_path: relative path to the input file
    :return: void
    """
    with open(file_path) as fp:
        for puzzle_number, puzzle in enumerate(fp):
            max_d, max_l, grid, goal = get_puzzle_info(puzzle)
            execute_dfs(grid, max_d, goal, puzzle_number)


def execute_dfs(grid, max_d, goal, puzzle_number):
    """
    Wrapper for DFS
    :param (ndarray) grid: numpy 2-D array representation of the input board
    :param (int) max_d: maximum depth
    :param (string) goal: serialized goal grid
    :param (int) puzzle_number: line number of the puzzle for which DFS is executed
    :return: void
    """
    print('Execute DFS with max depth {} on grid \n{} '.format(max_d, grid))
    open_list = []
    open_set = set()
    closed_dict = {}
    search_path = []

    s_grid = grid_to_string(grid)
    path_to_root = ['{}   {}'.format(0, s_grid)]

    root = Node(grid, s_grid, 1, 0, 0, path_to_root)
    open_list.append(root)
    open_set.add(s_grid)
    solution_path = dfs(open_list, open_set, closed_dict, search_path, goal, max_d)
    write_results(solution_path, search_path, puzzle_number, DFS_ALGORITHM)
    print('Found no solution' if solution_path == constant.NO_SOLUTION
          else 'Found result in {} moves'.format(len(solution_path) - 1))


def dfs(open_list: List[Node], open_set, closed_dict, search_path, goal, max_d):
    """
    Iterative DFS.
    Each node in the open list carries: grid, level and a solution_path up to this grid
    :param (stack) open_list: stack of yet to be processed grids
    :param (set) open_set: keep track of the configurations in the open_list
    :param (dictionary) closed_dict: visited grid configurations and their depth
    :param (list) search_path: path up to the specific node
    :param (string) goal: goal configuration
    :param (int) max_d: maximum execution depth
    :return (list | string): path up to identified solution. List of paths or 'no solution'
    """
    while len(open_list) > 0:
        node = open_list.pop()

        open_set.remove(node.s_grid)
        closed_dict[node.s_grid] = node.depth
        search_path.append(get_search_move(constant.DFS_ALGORITHM, node))
        if node.s_grid == goal:
            return node.path_from_root
        if node.depth < max_d:
            evaluate_dfs_children(open_list, open_set, closed_dict, node)
    return constant.NO_SOLUTION


# Define input file here
main('input.txt')
