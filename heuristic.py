# -----------------------------------------------------------
# heuristic.py 22/01/20
#
# Define heuristic functionality available throughout a project
#
# Copyright (c) 2020-2021 Team Artificial Incompetence, COMP 472
# All rights reserved.
# -----------------------------------------------------------
from typing import Set

import constant
from constant import DOUBLE_PRESS


def get_heuristic(heuristic_algorithm: str,
                  parent_black_tokens: int,
                  black_token_diff: int,
                  move_history: Set[str],
                  new_move) -> float:
    """
    Get h(n) for a given Node, given the heuristic algorithm
    :param parent_black_tokens: Number of black token of the parent node
    :param black_token_diff: Difference on black tokens after move
    :param heuristic_algorithm: Algorithm used to calculate heuristic
    :param move_history: List of moves done from the root node
    :param new_move: New move done for this child
    :return: h(n)
    """
    if heuristic_algorithm == constant.ZERO_HEURISTIC:
        return 0.0
    elif heuristic_algorithm == constant.COUNT_HEURISTIC:
        return get_total_count_heuristic(parent_black_tokens, black_token_diff)
    elif heuristic_algorithm == constant.DIV_BY_5_HEURISTIC:
        return get_div_by_5_heuristic(parent_black_tokens, black_token_diff)
    elif heuristic_algorithm == constant.NO_DOUBLE_PRESS_HEURISTIC:
        return get_no_double_press_heuristic(parent_black_tokens, black_token_diff, move_history, new_move)

    return 0


def get_total_count_heuristic(parent_black_tokens: int, black_token_diff: int) -> float:
    """
    Counts the total number of black pegs on the board using differential calculation
    :param parent_black_tokens: Number of black token of the parent node
    :param black_token_diff: Difference on black tokens after move
    :return: heuristic value of the grid
    """
    return parent_black_tokens + black_token_diff


def get_div_by_5_heuristic(parent_black_tokens: int, black_token_diff: int) -> float:
    """
    Counts the total number of black pegs on the board and then divides it by 5
    :param parent_black_tokens: Number of black token of the parent node
    :param black_token_diff: Difference on black tokens after move
    :return: heuristic value of the grid
    """
    return get_total_count_heuristic(parent_black_tokens, black_token_diff) / 5


def get_no_double_press_heuristic(parent_black_tokens: int,
                                  black_token_diff: int,
                                  move_history: Set[str],
                                  new_move: str) -> float:
    if new_move not in move_history:
        return get_div_by_5_heuristic(parent_black_tokens, black_token_diff)

    return DOUBLE_PRESS
