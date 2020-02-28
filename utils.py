# -----------------------------------------------------------
# utils.py 22/01/20
#
# Define set of utility functions available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
import copy
import os
from heapq import heappush
from typing import Dict, Tuple, Union

import numpy as np

from constant import *
from heuristic import get_heuristic


def flip_token(grid: np.ndarray, r: int, c: int) -> int:
    """
    Flip current token and 4 adjacent cells. Up, Down, Left, Right
    :param grid: numpy 2-D array
    :param r: row index
    :param c: column index
    :return: difference in number of black pegs after flip
    """
    dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    n = len(grid)
    count_flipped = 0
    grid[r][c] = 1 - grid[r][c]
    count_flipped += -1 if grid[r][c] == 0 else 1
    for i in range(4):
        nxt_row = r + dirs[i][0]
        nxt_col = c + dirs[i][1]
        if 0 <= nxt_row < n and 0 <= nxt_col < n:
            grid[nxt_row][nxt_col] = 1 - grid[nxt_row][nxt_col]
            count_flipped += -1 if grid[nxt_row][nxt_col] == 0 else 1
    return count_flipped


def grid_to_string(grid: np.ndarray) -> str:
    """
    Get string version of the 2D numpy array
    Example: [[1,1],[0,0]] => '1 1 0 0'
    :param grid: numpy 2-D array
    :return: string representation of string
    """
    return ' '.join(map(str, [value for row in grid for value in row]))


def string_to_grid(s_grid: str, n: int) -> np.ndarray:
    """
    Construct 2-D numpy array from its string representation
    :param s_grid: grid data
    :param n: grid size
    :return: 2-D numpy grid
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
    Return max_d, max_l, ndarray grid and goal string from the puzzle string
    :param puzzle: file line that describes puzzle
    :return: max_d, max_l, grid, goal
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
    :param n: shape of the 2-D grid, filled with zeros
    :return: serialized version of the goal grid
    """
    goal_grid = np.zeros([n, n], dtype=int)
    return grid_to_string(goal_grid)


def get_solution_move(row: int, col: int, s_grid: str) -> str:
    """
    Generate move string to be added to the current node's path
    Example: row = 0, col = 0, config = '1 1 0 0' => 'A1  1 1 0 0'
    :param row: row index
    :param col: column index
    :param s_grid: serialized version of the grid
    :return: solution move
    """
    ascii_of_a = 65
    token = chr(ascii_of_a + row) + str(col + 1)
    return '{}  {}'.format(token, s_grid)


def get_search_move(search_algorithm: str, node: Node) -> str:
    """
    Prepend configuration with required heuristic data
    :param search_algorithm: type of search algorithm
    :param node: Node object
    :return: search move
    """
    hn = node.get_hn() if search_algorithm in [BEST_FIRST_ALGORITHM, A_STAR_ALGORITHM] else 0
    gn = node.get_gn() if search_algorithm == A_STAR_ALGORITHM else 0
    fn = hn + gn
    config = node.s_grid.replace(' ', '')
    return '{} {} {} {}'.format(fn, gn, hn, config)


def evaluate_dfs_children(open_list: List[Node],
                          open_set: Set[str],
                          closed_dict: Dict[str, int],
                          node: Node):
    """
    Evaluate each child and properly insert them in the open list.
    :param open_list: stack containing all discovered nodes
    :param open_set: Set containing all grid strings of all discovered nodes from open_list
    :param closed_dict: Dictionary containing all visited grid strings
    :param node: Node object
    :return: void
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
            children_nodes[child_s_grid] = Node(child_grid, child_s_grid, node.depth + 1, child_path_from_root)
            children_s_grids.append(child_s_grid)

    children_s_grids.sort(key=lambda s_grid: get_white_token_score(s_grid), reverse=True)
    open_list.extend([children_nodes[child_config] for child_config in children_s_grids])


def evaluate_a_star_children(open_list: List[Tuple[float, int, Node]],
                             open_set: Set[str],
                             closed_set: set,
                             node: Node,
                             heuristic_algorithm: str):
    """
    Evaluate all of a node's children and add them to the open list
    :param open_list: Priority Queue containing all discovered nodes
    :param open_set: Set containing all grid strings of all discovered nodes from open_list
    :param closed_set: Set containing all visited grid strings
    :param node: Node object
    :param heuristic_algorithm: Which heuristic to use
    :return: void
    """
    for row, col in np.ndindex(node.grid.shape):
        child_grid = np.copy(node.grid)
        diff_black_tokens = flip_token(child_grid, row, col)
        child_s_grid: str = grid_to_string(child_grid)
        child_move = '{}:{}'.format(row, col)
        child_hn: float = get_heuristic(heuristic_algorithm, node.black_tokens, diff_black_tokens,
                                        node.move_history, child_move)
        if child_hn != DOUBLE_PRESS and child_s_grid not in open_set and child_s_grid not in closed_set:
            child_path = copy.deepcopy(node.path_from_root)
            child_path.append(get_solution_move(row, col, child_s_grid))
            child_moves = copy.deepcopy(node.move_history)
            child_moves.add(child_move)
            child_depth = node.depth + 1

            child_node = Node(child_grid, child_s_grid, child_depth, child_path, child_hn,
                              node.black_tokens + diff_black_tokens, child_moves)
            # Add child to open set and priority queue
            heappush(open_list, (child_node.get_fn(), get_white_token_score(child_s_grid), child_node))
            open_set.add(child_s_grid)


def evaluate_bfs_children(open_list: List[Tuple[float, int, Node]],
                          open_set: Set[str],
                          closed_set: set,
                          node: Node,
                          heuristic_algorithm: str):
    """
    Evaluate all of a node's children and add them to the open list
    :param open_list: Priority Queue containing all discovered nodes
    :param open_set: Set containing all grid strings of all discovered nodes from open_list
    :param closed_set: Set containing all visited grid strings
    :param node: Node object
    :param heuristic_algorithm: Which heuristic to use
    :return: void
    """
    for row, col in np.ndindex(node.grid.shape):
        child_grid = np.copy(node.grid)
        diff_black_tokens = flip_token(child_grid, row, col)
        child_s_grid: str = grid_to_string(child_grid)
        child_move = '{}:{}'.format(row, col)
        child_hn: float = get_heuristic(heuristic_algorithm, node.black_tokens, diff_black_tokens,
                                        node.move_history, child_move)
        if child_hn != DOUBLE_PRESS and child_s_grid not in open_set and child_s_grid not in closed_set:
            child_path = copy.deepcopy(node.path_from_root)
            child_path.append(get_solution_move(row, col, child_s_grid))
            child_moves = copy.deepcopy(node.move_history)
            child_moves.add(child_move)

            child_node = Node(child_grid, child_s_grid, node.depth, child_path, child_hn,
                              node.black_tokens + diff_black_tokens, child_moves)
            # Add child to open set and priority queue
            heappush(open_list, (child_node.get_hn(), get_white_token_score(child_s_grid), child_node))
            open_set.add(child_s_grid)


def get_white_token_score(s_grid: str) -> int:
    """
    Returns the numerical value of a grid string, considering
    it as the string representation of a binary number
    :param s_grid: The string representation of a grid
    :return: numerical value of string grid
    """
    return int(s_grid.replace(' ', ''), 2)


def write_results(puzzle_number: int, algorithm: str, heuristic: str, solution_path, search_path: List[str]):
    """
    Dump solution_path and search_path to files
    :param solution_path: path up to identified solution. List of paths or 'no solution'
    :param search_path: close list of searched nodes
    :param puzzle_number: line number of the puzzle prepended to the name of the file
    :param algorithm: Algorithm used for the current run
    :param heuristic: Heuristic used to solve puzzle
    :return: void
    """
    filename = SOLUTION_FILE_TEMPLATE.format(heuristic, puzzle_number, algorithm)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as fp:
        if type(solution_path) is str:
            fp.write(solution_path)
        else:
            for path in solution_path:
                fp.write('{}\n'.format(path))
    filename = SEARCH_FILE_TEMPLATE.format(heuristic, puzzle_number, algorithm)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as fp:
        for path in search_path:
            fp.write('{}\n'.format(path))


def gather_performance(puzzle_number: int, grid_size: int, solution_path: Union[str, list], search_path_len: int,
                       start_time: float, end_time: float, algorithm: str, heuristic: str):
    filename = PERFORMANCE_DIR_TEMPLATE.format(algorithm, heuristic)
    with open(filename, 'a') as fp:
        fp.write(PERFORMANCE_FILE_LINE.format(puzzle_number, grid_size,
                                              NO_SOLUTION if solution_path == NO_SOLUTION else len(solution_path),
                                              search_path_len, end_time - start_time))


def prepare_performance_file(algorithm: str, heuristic: str):
    filename = PERFORMANCE_DIR_TEMPLATE.format(algorithm, heuristic)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as fp:
        fp.write(PERFORMANCE_FILE_HEADER.format('Puzzle number', 'Grid size',
                                                'Solution length', 'Search length', 'Time taken (seconds)'))
