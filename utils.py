# -----------------------------------------------------------
# uninformed_search.py 22/01/20
#
# Define set of utility functions available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, Comp 472
# All rights reserved.
# -----------------------------------------------------------
import copy
import numpy as np
import constant
from heuristic import get_heuristic


def flip(grid, r, c):
    """
    Flip current token and 4 adjacent cells. Up, Down, Left, Right
    :param (ndarray) grid: numpy 2-D array
    :param (int) r: row index
    :param (int) c: column index
    :return: void
    """
    dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    n = len(grid)
    grid[r][c] = 1 - grid[r][c]
    for i in range(4):
        nxt_row = r + dirs[i][0]
        nxt_col = c + dirs[i][1]
        if 0 <= nxt_row < n and 0 <= nxt_col < n:
            grid[nxt_row][nxt_col] = 1 - grid[nxt_row][nxt_col]


def get_configuration(grid):
    """
    Get serialized version of the grid.
    Example: [[1,1],[0,0]] => '1 1 0 0'
    :param (ndarray) grid: numpy 2-D array
    :return (string): serialized grid
    """
    return ' '.join(map(str, [value for row in grid for value in row]))


def get_puzzle_info(puzzle):
    """
    Extract n, max_d, max_l and board values from the file line
    :param (string) puzzle: file line that describes puzzle
    :return (int, int, int, string): n, max_d, max_l, board values
    """
    puzzle = puzzle.split(' ')
    return int(puzzle[0]), int(puzzle[1]), int(puzzle[2]), puzzle[3]


def construct_grid(board, n):
    """
    Construct 2-D numpy array of provided shape
    :param (string) board: grid data
    :param (int) n: grid size
    :return (ndarray): 2-D numpy grid
    """
    grid = np.empty([n, n], dtype=int)
    row_num = int(len(board) / n)
    for i in range(row_num):
        start = n * i
        end = start + n
        row = np.array([int(val) for val in list(board[start:end])])
        grid[i] = row
    return grid


def get_goal_state(n):
    """
    Get serialized version of the goal grid
    Example: (n = 3) => '000000000'
    :param (int) n: shape of the 2-D grid, filled with zeros
    :return (string): serialized version of the goal grid
    """
    goal_grid = np.zeros([n, n], dtype=int)
    return get_configuration(goal_grid)


def get_solution_move(row, col, configuration):
    """
    Prepend configuration with a required token format
    Example: row = 0, col = 0, config = '1 1 0 0' => 'A1  1 1 0 0'
    :param (int) row: row number. Index wise
    :param (int) col: column number. Index wise
    :param (string) configuration: serialized version of the grid
    :return (string): solution move
    """
    ascii_of_a = 65
    token = chr(ascii_of_a + row) + str(col + 1)
    return '{}  {}'.format(token, configuration)


def get_search_move(search_algorithm, configuration):
    """
    Prepend configuration with required heuristic data
    :param (string) search_algorithm: type of search algorithm
    :param (string) configuration: serialized version of the grid
    :return (string): search move
    """
    fn, gn, hn = get_heuristic(search_algorithm)
    config = configuration.replace(' ', '')
    return '{} {} {} {}'.format(fn, gn, hn, config)


def evaluate_children(open_list, grid, solution_path, open_set, closed_dict, level):
    """
    Evaluate each child and properly insert them in the open list.
    :param (stack) open_list: stack of yet to be processed grids
    :param (ndarray) grid: Parent 2-D array
    :param (list) solution_path: Path to the parent grid
    :param (set) open_set: keep track of the configurations in the open_list
    :param (dictionary) closed_dict: visited grid configurations and their depth
    :param (int) level: Level of the parent grid
    :return:
    """
    children_config = []
    config_to_grid = {}
    n = len(grid)
    for row in range(n):
        for col in range(n):
            grid_copy = np.copy(grid)
            flip(grid_copy, row, col)
            grid_copy_config = get_configuration(grid_copy)
            if grid_copy_config not in open_set\
                    and (grid_copy_config not in closed_dict or closed_dict[grid_copy_config] > level + 1):
                open_set.add(grid_copy_config)
                solution_move_child = get_solution_move(row, col, grid_copy_config)
                copy_solution_path = copy.deepcopy(solution_path)
                copy_solution_path.append(solution_move_child)
                config_to_grid[grid_copy_config] = \
                    grid_copy, level + 1, copy_solution_path
                children_config.append(grid_copy_config)

    sorted_children = sort_children(children_config)
    open_list.extend([config_to_grid[child_config] for child_config in sorted_children])


def sort_children(children):
    """
    Sort children in descending order of their White Tokens.
    Meaning that the next best choice is at the very end of the returning list.
    Sorting takes into account Scenario 2, provided in a handout.
    Example:
        Input:'1010011', '1010101', '1010110', '1110011', '1111111'
        Output: '1111111', '1110011', '1010110', '1010101', '1010011'
    :param (list) children: Unsorted configuration grids
    :return (list): sorted list of configuration grids in descending order
    """
    sorted_children = []

    while len(children) > 0:
        n = len(children)
        furthest_token_idx = 0
        for j in range(1, n):
            furthest_token, j_token = get_white_tokens(children[furthest_token_idx], children[j])
            if j_token > -1 and furthest_token > -1:
                furthest_token_idx = j if j_token > furthest_token else furthest_token_idx
            else:
                furthest_token_idx = j if j_token == -1 else furthest_token_idx
        sorted_children.append(children[furthest_token_idx])
        children.pop(furthest_token_idx)
    return sorted_children


def get_white_tokens(child_1, child_2):
    """
    Get positions of the first White Tokens for 2 children.
    Cases of the White Tokens being located at the same spots are handled.
    :param (string) child_1: configuration grid
    :param (string) child_2: configuration grid
    :return (int, int) : positions of White Tokens for child_1 and child_2 respectively
    """
    start = 0
    while child_1.find(constant.WHITE_TOKEN, start) == child_2.find(constant.WHITE_TOKEN, start) != -1:
        start = child_2.find(constant.WHITE_TOKEN, start) + 1
    child_1_token = child_1.find(constant.WHITE_TOKEN, start)
    child_2_token = child_2.find(constant.WHITE_TOKEN, start)
    return child_1_token, child_2_token


def write_results(solution_path, search_path, puzzle_number):
    """
    Dump solution_path and search_path to files
    :param (list | string) solution_path: path up to identified solution. List of paths or 'no solution'
    :param (list) search_path: close list of searched nodes
    :param (int) puzzle_number: line number of the puzzle prepended to the name of the file
    :return: void
    """
    with open('{}{}'.format(puzzle_number, constant.DFS_SOLUTION_FILE), 'w') as fp:
        if type(solution_path) is str:
            fp.write(solution_path)
        else:
            for path in solution_path:
                fp.write('{}\n'.format(path))

    with open('{}{}'.format(puzzle_number, constant.DFS_SEARCH_FILE), 'w') as fp:
        for path in search_path:
            fp.write('{}\n'.format(path))
