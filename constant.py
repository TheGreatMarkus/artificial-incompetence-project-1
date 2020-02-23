# -----------------------------------------------------------
# constant.py 22/01/20
#
# Define constants available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
from typing import List

from numpy.core.records import ndarray

NO_SOLUTION = 'no solution'

SEARCH_FILE = 'search.txt'
SOLUTION_FILE = 'solution.txt'

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
    grid: ndarray = None
    s_grid: str = ''
    depth: int = 0
    hn: float = 0.0
    black_tokens = 0
    path_from_root: list = []

    def __init__(self, grid: ndarray, s_grid: str, depth: int, hn: float, black_tokens: int, path_from_root: List[str]):
        """
        Create Node object
        :param grid: 2D numpy array representation of the state
        :param s_grid: String representation of the state
        :param depth: Depth of the state
        :param hn: h(n) of the state
        :param path_from_root: Path from the root to the state
        """
        self.grid = grid
        self.s_grid = s_grid
        self.depth = depth
        self.hn = hn
        self.black_tokens = black_tokens
        self.path_from_root = path_from_root

    def get_hn(self):
        return self.hn

    def get_gn(self):
        return self.depth

    def get_fn(self):
        return self.hn + self.depth
