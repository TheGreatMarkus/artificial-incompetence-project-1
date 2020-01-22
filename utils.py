# -----------------------------------------------------------
# uninformed_search.py 22/01/20
#
# Define set of utility functions available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, Comp 472
# All rights reserved.
# -----------------------------------------------------------
import numpy as np
import constant
from heuristic import get_heuristic


def flip(grid, r, c):
    """
    Flip currect token and 4 adjacent cells. Up, Down, Left, Right
    :param (ndarray) grid: numpy 2-D array
    :param (int) r: row number. Index wise
    :param (int) c: column number. Index wise
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
    :param (int) n: grid shape
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
    :param (int) n: shape of the 2-D grid, filled with zeros
    :return (string): serialized version of the goal grid
    """
    goal_grid = np.zeros([n, n], dtype=int)
    return get_configuration(goal_grid)


def get_solution_move(row, col, configuration):
    """
    Prepend configuration with a required token format
    Example: row = 0, col = 0, config = '1 1 0 0' converted 'A1  1 1 0 0'
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
