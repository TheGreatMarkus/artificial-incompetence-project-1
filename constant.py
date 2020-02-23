# -----------------------------------------------------------
# constant.py 22/01/20
#
# Define constants available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
from numpy.core.records import ndarray

NO_SOLUTION = 'no solution'
WHITE_TOKEN = '0'

SEARCH_FILE = 'search.txt'
SOLUTION_FILE = 'solution.txt'

DFS_ALGORITHM = 'dfs'
A_STAR_ALGORITHM = 'a_star'
BEST_FIRST_ALGORITHM = 'best_first'

ZERO_HEURISTIC = 'zero_h'
COUNT_HEURISTIC = 'count_h'
DIV_BY_5_HEURISTIC = 'div_5_h'
NO_DOUBLE_PRESS_HEURISTIC = 'no_dbl_press_h'


class Node:
    grid: ndarray = None
    s_grid: str = ''
    depth: int = 0
    hn: int = 0
    path_from_root: list = []

    def __init__(self, grid: ndarray, s_grid: str, depth: int, hn: int, path_from_root: list):
        self.grid = grid
        self.s_grid = s_grid
        self.depth = depth
        self.hn = hn
        self.path_from_root = path_from_root

    def get_hn(self):
        return self.hn

    def get_gn(self):
        return self.depth

    def get_fn(self):
        return self.hn + self.depth
