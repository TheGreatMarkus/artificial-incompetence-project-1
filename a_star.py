# -----------------------------------------------------------
# dfs.py 22/01/20
#
# Define and run a* search algorithm
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
import sys
import time
from heapq import heappush, heappop
from typing import List, Tuple, Set

import numpy as np
from numpy.core.multiarray import ndarray

import constant
from constant import NO_SOLUTION, ZERO_HEURISTIC, COUNT_HEURISTIC, DIV_BY_5_HEURISTIC, \
    NO_DOUBLE_PRESS_HEURISTIC, Node, A_STAR_ALGORITHM
from heuristic import get_heuristic
from utils import get_puzzle_info, grid_to_string, write_results, get_search_move, evaluate_a_star_children, \
    get_white_token_score, prepare_performance_file, gather_performance


def main(file_path):
    """
    Read file, retrieve puzzle info, and execute a* for each puzzle
    :param (string) file_path: relative path the input file
    :return: void
    """
    heuristics = [ZERO_HEURISTIC, COUNT_HEURISTIC, DIV_BY_5_HEURISTIC, NO_DOUBLE_PRESS_HEURISTIC]
    if len(sys.argv) < 2 or sys.argv[1] not in heuristics:
        print('Invalid heuristic. Accepted heuristics are: {}'.format(heuristics))
        sys.exit()

    heuristic = sys.argv[1]
    prepare_performance_file(A_STAR_ALGORITHM, heuristic)
    with open(file_path) as puzzle_file:
        for puzzle_number, puzzle in enumerate(puzzle_file):
            max_d, max_l, grid, goal = get_puzzle_info(puzzle)
            execute_a_star(grid, goal, max_l, puzzle_number, heuristic)


def execute_a_star(grid: ndarray,
                   goal: str,
                   max_l: int,
                   puzzle_number: int,
                   heuristic_algorithm: str):
    """
    Wrapper function to run A*
    :param grid: numpy 2D array representation of the input board.
    :param goal: goal grid string
    :param max_l: maximum search path length
    :param puzzle_number: line number of the puzzle
    :param heuristic_algorithm: Heuristic algorithm to be used for this run
    :return: void
    """
    print("Executing A* Algorithm with heuristic {} and max search length of {} on the grid\n{}".format(
        heuristic_algorithm, max_l, grid))
    # Initialize necessary data structures
    open_list: List[Tuple[float, int, Node]] = []
    open_set = set()
    closed_set = set()
    search_path: List[str] = []

    # initialize root node information
    s_grid = grid_to_string(grid)
    path = ['{}   {}'.format(0, s_grid)]
    num_black_tokens = s_grid.count('1')
    hn = get_heuristic(heuristic_algorithm, num_black_tokens, 0)
    root_node = Node(grid, s_grid, 1, path, hn, num_black_tokens, [])

    heappush(open_list, (root_node.get_fn(), get_white_token_score(s_grid), root_node))
    open_set.add(s_grid)

    start_time = time.time()
    solution_path = a_star(open_list, open_set, closed_set, search_path, goal, max_l, heuristic_algorithm)
    end_time = time.time()
    write_results(solution_path, search_path, puzzle_number, A_STAR_ALGORITHM)
    gather_performance(puzzle_number, np.size(grid, 0), len(solution_path), len(search_path),
                       start_time, end_time, A_STAR_ALGORITHM, heuristic_algorithm)
    print('Found no solution' if solution_path == constant.NO_SOLUTION
          else 'Found solution in {} moves'.format(len(solution_path) - 1))


def a_star(open_list: List[Tuple[float, int, Node]],
           open_set: Set[str],
           closed_set: Set[str],
           search_path: List[str],
           goal_s_grid,
           max_l,
           heuristic) -> List[str]:
    """
    Runs the A* search algorithm
    :param open_list: Priority Queue containing all discovered nodes
    :param open_set: Set containing all grid strings of all discovered nodes from open_list
    :param closed_set: Set containing all visited grid strings
    :param search_path: Search path string
    :param goal_s_grid: Goal grid string
    :param max_l: maximum search path length
    :param heuristic: Heuristic algorithm to be used for this run
    :return: Solution path if available, else returns a string indicating failure to find a solution
    """
    while len(open_list) > 0:
        # Pop node from priority queue
        node_tuple = heappop(open_list)
        node = node_tuple[2]
        # Update data structures
        open_set.remove(node.s_grid)
        closed_set.add(node.s_grid)
        search_path.append(get_search_move(A_STAR_ALGORITHM, node))

        if node.s_grid == goal_s_grid:
            print('Search path length: {}'.format(len(search_path)))
            print('Open list size: {}'.format(len(open_list)))
            return node.path_from_root
        if len(search_path) < max_l:
            evaluate_a_star_children(open_list, open_set, closed_set, node, heuristic)
    return NO_SOLUTION


main('input.txt')
