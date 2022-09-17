from itertools import chain
from typing import List, Dict, Callable

import pytest

from bot.minesweeper import game
from tests.test_data.minefields import \
    game_won, one_open_cell, game_in_progress, \
    all_flags_correct_has_hidden_cells, more_flags_than_should
from bot.minesweeper.states import GameState


def count_items(rows, count_func: Callable) -> int:
    return sum(1 for _ in filter(count_func, chain(*rows)))


@pytest.mark.parametrize(
    "field, game_state",
    [
        [game_won, GameState.VICTORY],
        [one_open_cell, GameState.HAS_HIDDEN_NUMBERS],
        [game_in_progress, GameState.HAS_HIDDEN_NUMBERS],
        [all_flags_correct_has_hidden_cells, GameState.HAS_HIDDEN_NUMBERS],
        [more_flags_than_should, GameState.MORE_FLAGS_THAN_BOMBS],
    ]
)
def test_fields(
        field: List[List[Dict]],
        game_state: int
):
    assert game.analyze_game_field(field) == game_state
