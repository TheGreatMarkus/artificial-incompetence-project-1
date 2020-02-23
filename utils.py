# -----------------------------------------------------------
# utils.py 22/01/20
#
# Define set of utility functions available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
import copy
from heapq import heappush
from typing import List, Set, Tuple

import numpy as np

from constant import A_STAR_ALGORITHM, BEST_FIRST_ALGORITHM, SOLUTION_FILE, SEARCH_FILE, WHITE_TOKEN, Node
from heuristic import get_heuristic


def flip_token(grid: np.ndarray, r: int, c: int) -> int:
    """
    Flip current token and 4 adjacent cells. Up, Down, Left, Right
    :param (ndarray) grid: numpy 2-D array
    :param (int) r: row index
    :param (int) c: column index
    :return: difference in number of black pegs after flip
    """
    dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    n = len(grid)
    count_flipped = 0
    grid[r][c] = 1 - grid[r][c]
    count_flipped += 1 if grid[r][c] == 0 else -1
    for i in range(4):
        nxt_row = r + dirs[i][0]
        nxt_col = c + dirs[i][1]
        if 0 <= nxt_row < n and 0 <= nxt_col < n:
            grid[nxt_row][nxt_col] = 1 - grid[nxt_row][nxt_col]
            count_flipped += 1 if grid[nxt_row][nxt_col] == 0 else -1
    return count_flipped


def grid_to_string(grid: np.ndarray) -> str:
    """
    Get serialized version of the grid.
    Example: [[1,1],[0,0]] => '1 1 0 0'
    :param (ndarray) grid: numpy 2-D array
    :return (string): serialized grid
    """
    return ' '.join(map(str, [value for row in grid for value in row]))


def string_to_grid(s_grid: str, n: int) -> np.ndarray:
    """
    Construct 2-D numpy array of provided shape
    :param (string) s_grid: grid data
    :param (int) n: grid size
    :return (ndarray): 2-D numpy grid
    """
    grid = np.empty([n, n], dtype=int)
    row_num = int(len(s_grid) / n)
    for i in range(row_num):
        start = n * i
        end = start + n
        row = np.array([int(val) for val in list(s_grid[start:end])])
        grid[i] = row
    return grid


def get_puzzle_info(puzzle: str) -> Tuple[int, int, np.ndarray, str]:
    """
    Return max_d, max_l, ndarray grid and goal configuration from the puzzle string
    :param (string) puzzle: file line that describes puzzle
    :return (int, int, ndarray, string): max_d, max_l, grid, goal
    """
    puzzle = puzzle.split(' ')
    n = int(puzzle[0])
    max_d = int(puzzle[1])
    max_l = int(puzzle[2])
    board = puzzle[3]
    grid = string_to_grid(board, n)
    goal = get_goal_state(n)
    return max_d, max_l, grid, goal


def get_goal_state(n: int) -> str:
    """
    Get serialized version of the goal grid
    Example: (n = 3) => '000000000'
    :param (int) n: shape of the 2-D grid, filled with zeros
    :return (string): serialized version of the goal grid
    """
    goal_grid = np.zeros([n, n], dtype=int)
    return grid_to_string(goal_grid)


def get_solution_move(row: int, col: int, s_grid: str):
    """
    Generate move string to be added to the current node's path
    Example: row = 0, col = 0, config = '1 1 0 0' => 'A1  1 1 0 0'
    :param (int) row: row number. Index wise
    :param (int) col: column number. Index wise
    :param (string) s_grid: serialized version of the grid
    :return (string): solution move
    """
    ascii_of_a = 65
    token = chr(ascii_of_a + row) + str(col + 1)
    return '{}  {}'.format(token, s_grid)


def get_search_move(search_algorithm: str, node: Node):
    """
    Prepend configuration with required heuristic data
    :param (string) search_algorithm: type of search algorithm
    :param node:
    :return (string): search move
    """
    hn = node.get_hn() if search_algorithm in [BEST_FIRST_ALGORITHM, A_STAR_ALGORITHM] else 0
    gn = node.get_gn() if search_algorithm == A_STAR_ALGORITHM else 0
    fn = hn + gn
    config = node.s_grid.replace(' ', '')
    return '{} {} {} {}'.format(fn, gn, hn, config)


def evaluate_dfs_children(open_list, open_set, closed_dict, node: Node):
    """
    Evaluate each child and properly insert them in the open list.
    :param node:
    :param (stack) open_list: stack of yet to be processed grids
    :param (set) open_set: keep track of the configurations in the open_list
    :param (dictionary) closed_dict: visited grid configurations and their depth
    :return:
    """
    children_s_grids = []
    children_nodes = {}
    for row, col in np.ndindex(node.grid.shape):
        child_grid = np.copy(node.grid)
        flip_token(child_grid, row, col)
        child_s_grid = grid_to_string(child_grid)
        if child_s_grid not in open_set \
                and (child_s_grid not in closed_dict or closed_dict[child_s_grid] > node.depth + 1):
            open_set.add(child_s_grid)
            child_solution_move = get_solution_move(row, col, child_s_grid)
            child_path_from_root = copy.deepcopy(node.path_from_root)
            child_path_from_root.append(child_solution_move)
            children_nodes[child_s_grid] = Node(child_grid, child_s_grid, node.depth + 1, 0, child_path_from_root)
            children_s_grids.append(child_s_grid)

    children_s_grids.sort(key=lambda s_grid: get_white_token_score(s_grid), reverse=True)
    open_list.extend([children_nodes[child_config] for child_config in children_s_grids])


def evaluate_a_star_children(open_list: List[Tuple[int, int, Node]],
                             open_set: Set[str],
                             closed_set: set,
                             node: Node,
                             heuristic_algorithm: str):
    for row, col in np.ndindex(node.grid.shape):
        child_grid = np.copy(node.grid)
        flip_token(child_grid, row, col)
        child_s_grid: str = grid_to_string(child_grid)
        if child_s_grid not in open_set.union(closed_set):
            child_path = copy.deepcopy(node.path_from_root)
            child_path.append(get_solution_move(row, col, child_s_grid))
            child_hn = get_heuristic(heuristic_algorithm, child_grid, child_path)
            child_depth = node.depth + 1
            child_node = Node(child_grid, child_s_grid, child_depth, child_hn, child_path)

            # Add child to open set and priority queue
            heappush(open_list, (child_node.get_fn(), get_white_token_score(child_s_grid), child_node))
            open_set.add(child_s_grid)
    print('Length of open list {}'.format(len(open_list)))


def get_white_token_score(s_grid: str) -> int:
    return int(s_grid.replace(' ', ''), 2)


def write_results(solution_path, search_path, puzzle_number, algorithm: str):
    """
    Dump solution_path and search_path to files
    :param (list | string) solution_path: path up to identified solution. List of paths or 'no solution'
    :param (list) search_path: close list of searched nodes
    :param (int) puzzle_number: line number of the puzzle prepended to the name of the file
    :return: void
    """
    with open('{}_{}_{}'.format(puzzle_number, algorithm, SOLUTION_FILE), 'w') as fp:
        if type(solution_path) is str:
            fp.write(solution_path)
        else:
            for path in solution_path:
                fp.write('{}\n'.format(path))

    with open('{}_{}_{}'.format(puzzle_number, algorithm, SEARCH_FILE), 'w') as fp:
        for path in search_path:
            fp.write('{}\n'.format(path))
