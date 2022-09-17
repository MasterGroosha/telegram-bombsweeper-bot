from itertools import chain
from typing import List, Dict, Callable

import pytest

from bot.minesweeper import game
from bot.minesweeper.states import GameState
from tests.test_data import minefields


def count_items(rows, count_func: Callable) -> int:
    return sum(1 for _ in filter(count_func, chain(*rows)))


@pytest.mark.parametrize(
    "field, game_state",
    [
        [minefields.game_won, GameState.VICTORY],
        [minefields.one_open_cell, GameState.HAS_HIDDEN_NUMBERS],
        [minefields.game_in_progress, GameState.HAS_HIDDEN_NUMBERS],
        [minefields.all_flags_correct_has_hidden_cells, GameState.HAS_HIDDEN_NUMBERS],
        [minefields.more_flags_than_should, GameState.MORE_FLAGS_THAN_BOMBS],
    ]
)
def test_fields(
        field: List[List[Dict]],
        game_state: int
):
    assert game.analyze_game_field(field) == game_state
