# -----------------------------------------------------------
# constant.py 22/01/20
#
# Define constants available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
from typing import List, Tuple

from numpy.core.records import ndarray

NO_SOLUTION = 'no solution'
DOUBLE_PRESS = -1

SEARCH_FILE = 'search.txt'
SOLUTION_FILE = 'solution.txt'
PERFORMANCE_DIR_TEMPLATE = 'performance/{}_{}.txt'
PERFORMANCE_FILE_HEADER = '{}\t{}\t{}\t{}\t{}\n'
PERFORMANCE_FILE_LINE = '{}\t{}\t{}\t{}\t{:.10f}\n'

DFS_ALGORITHM = 'dfs'
A_STAR_ALGORITHM = 'astar'
BEST_FIRST_ALGORITHM = 'bfs'

ZERO_HEURISTIC = 'zero_h'
COUNT_HEURISTIC = 'count_h'
DIV_BY_5_HEURISTIC = 'div_5_h'
NO_DOUBLE_PRESS_HEURISTIC = 'no_dbl_press_h'


class Node:
    """
    Node containing the 2D numpy array and string representations of a grid state,
    its depth, h(n) and path from the root node
    """
    # Fields required by all algorithms
    grid: ndarray = None
    s_grid: str = ''
    depth: int = 0
    path_from_root: List[str] = []

    # Fields only required by informed heuristics
    hn: float = 0.0
    black_tokens = 0
    move_history: List[Tuple[int, int]] = []

    def __init__(self,
                 grid: ndarray,
                 s_grid: str,
                 depth: int,
                 path_from_root: List[str],
                 # optional, only for informed search
                 hn: float = 0,
                 black_tokens: int = 0,
                 move_history: List[Tuple[int, int]] = None):
        """
        Generate Node object
        :param grid: 2D numpy array representation of the state
        :param s_grid: String representation of the state
        :param depth: Depth of the state
        :param path_from_root: Path from the root to the state
        :param hn: h(n) of the state
        :param black_tokens: Number of black tokens in the state
        :param move_history: history of (row,col) moves from the root node
        """
        self.grid = grid
        self.s_grid = s_grid
        self.depth = depth
        self.path_from_root = path_from_root
        self.hn = hn
        self.black_tokens = black_tokens
        self.move_history = move_history

    def get_hn(self):
        return self.hn

    def get_gn(self):
        return self.depth

    def get_fn(self):
        return self.hn + self.depth
