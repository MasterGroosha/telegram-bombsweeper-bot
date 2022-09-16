from itertools import chain
from typing import List, Dict, Callable

import pytest

from bot.minesweeper import game
from tests.test_data.minefields import \
    game_won, one_open_cell, game_in_progress, \
    all_flags_correct_has_hidden_cells, more_flags_than_should


def count_items(rows, count_func: Callable) -> int:
    return sum(1 for _ in filter(count_func, chain(*rows)))


@pytest.mark.parametrize(
    "field, all_free_cells_are_open, untouched_cells_count, all_flags_match_bombs",
    [
        [game_won, True, 3, True],
        [one_open_cell, False, 5*5-1, True],
        [game_in_progress, False, 2, True],
        [all_flags_correct_has_hidden_cells, False, 1, True],
        [more_flags_than_should, False, 0, False],
    ]
)
def test_fields(
        field: List[List[Dict]],
        all_free_cells_are_open: bool,
        untouched_cells_count: int,
        all_flags_match_bombs: bool
):
    assert game.all_free_cells_are_open(field) == all_free_cells_are_open
    assert game.untouched_cells_count(field) == untouched_cells_count
    assert game.all_flags_match_bombs(field) == all_flags_match_bombs
