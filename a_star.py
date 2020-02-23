# -----------------------------------------------------------
# dfs.py 22/01/20
#
# Define and run a* search algorithm
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
import sys
from heapq import heappush, heappop
from typing import List, Tuple

from numpy.core.multiarray import ndarray

import constant
from constant import NO_SOLUTION, ZERO_HEURISTIC, COUNT_HEURISTIC, DIV_BY_5_HEURISTIC, \
    NO_DOUBLE_PRESS_HEURISTIC, Node, A_STAR_ALGORITHM
from heuristic import get_heuristic
from utils import get_puzzle_info, grid_to_string, write_results, get_search_move, evaluate_dfs_children, \
    evaluate_a_star_children, get_white_token_score


def main(file_path):
    """
    Read file, retrive puzzle info, and execute a* for each puzzle
    :param (string) file_path: relative path the input fule
    :return: void
    """
    heuristic = constant.ZERO_HEURISTIC
    if len(sys.argv) > 1:
        heuristic = sys.argv[1]
        heuristics = [ZERO_HEURISTIC, COUNT_HEURISTIC, DIV_BY_5_HEURISTIC, NO_DOUBLE_PRESS_HEURISTIC]
        if heuristic not in heuristics:
            print('Invalid heuristic. Accepted heuristics are: {}'.format(heuristics))
            sys.exit()

    with open(file_path) as puzzle_file:
        for puzzle_number, puzzle in enumerate(puzzle_file):
            max_d, max_l, grid, goal = get_puzzle_info(puzzle)
            execute_a_star(grid, goal, max_l, puzzle_number, heuristic)


def execute_a_star(grid: ndarray, goal: str, max_l: int, puzzle_number: int, heuristic_algorithm: str):
    """
    Wrapper function for A*
    :param heuristic_algorithm: Heuristic algorithm to be used
    :param (ndarray) grid: numpy 2D array representation of the input board.
    :param (string) goal: goal s_grid
    :param (int) max_l: maximum search path length
    :param (int) puzzle_number: line number of the puzzle
    :return: void
    """
    print("Executing A* Algorithm with max search length of {} on grid\n{}".format(max_l, grid))
    # Initialize necessary data structures
    open_list: List[Tuple[int, int, Node]] = []
    open_set = set()
    closed_set = set()
    search_path: List[str] = []

    # initialize root node information
    s_grid = grid_to_string(grid)
    path = ['{}   {}'.format(0, s_grid)]
    hn = get_heuristic(heuristic_algorithm, grid, path)
    root_node = Node(grid, s_grid, 1, hn, path)

    heappush(open_list, (root_node.get_fn(), get_white_token_score(s_grid), root_node))
    open_set.add(s_grid)

    solution_path = a_star(open_list, open_set, closed_set, search_path, goal, max_l, heuristic_algorithm)
    write_results(solution_path, search_path, puzzle_number, A_STAR_ALGORITHM)
    print('Found no solution' if solution_path == constant.NO_SOLUTION
          else 'Found solution in {} moves'.format(len(solution_path) - 1))


def a_star(open_list: List[Tuple[int, int, Node]], open_set, closed_set: set, search_path, goal, max_l,
           heuristic_algorithm) -> List[str]:
    while len(open_list) > 0:
        node_tuple: Tuple[int, int, Node] = heappop(open_list)
        node = node_tuple[2]

        hn = node.get_hn()
        grid = node.grid
        depth = node.depth
        solution_path = node.path_from_root
        s_grid = node.s_grid

        open_set.remove(s_grid)
        closed_set.add(s_grid)
        search_path.append(get_search_move(A_STAR_ALGORITHM, s_grid, node))
        if s_grid == goal:
            return solution_path
        if len(search_path) < max_l:
            evaluate_a_star_children(open_list, open_set, closed_set, node, heuristic_algorithm)
    return NO_SOLUTION


main('input.txt')
