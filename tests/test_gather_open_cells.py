from typing import List, Tuple

import pytest

from bot.minesweeper.game import gather_open_cells


@pytest.mark.parametrize(
    "field, current, expected",
    [
        [
            # Field
            [[0, 1, 1, 1, 0], [1, 2, "*", 1, 0], [1, "*", 2, 1, 0], [1, 1, 1, 1, 1], [0, 0, 1, "*", 1]],
            # Current
            (0, 4),
            # Expected
            [(0, 4), (1, 4), (2, 4), (0, 3), (1, 3), (2, 3), (3, 3), (3, 4)]
        ],
        [
            # Field
            [[0, 1, 1, 1, 0], [1, 2, "*", 1, 0], [1, "*", 2, 1, 0], [1, 1, 1, 1, 1], [0, 0, 1, "*", 1]],
            # Current
            (0, 0),
            # Expected
            [(0, 0), (0, 1), (1, 0), (1, 1)]
        ],
        [
            # Field
            [[0, 1, 1, 1, 0], [1, 2, "*", 1, 0], [1, "*", 2, 1, 0], [1, 1, 1, 1, 1], [0, 0, 1, "*", 1]],
            # Current
            (4, 0),
            # Expected
            [(4, 0), (4, 1), (4, 2), (3, 0), (3, 1), (3, 2)]
        ],
        [
            # Field
            [[0, 0, 1, 1, 1], [0, 0, 1, "*", 1], [0, 0, 2, 2, 2], [0, 0, 1, "*", 2], [0, 0, 1, 2, "*"]],
            # Current
            (0, 0),
            # Expected
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2),
             (4, 0), (4, 1), (4, 2)]
        ],
        [
            # Field
            [[0, 0, 1, "*", 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 0], [0, 1, "*", 2, 1], [0, 1, 1, 2, "*"]],
            # Current
            (0, 0),
            # Expected
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (4, 0), (4, 1)]
        ]
    ]
)
def test_gather_open_cells(field: List[List[int]], current: Tuple[int, int],
                           expected: List[Tuple[int, int]]):
    assert sorted(gather_open_cells(field, current, reset_contextvar=True)) == sorted(expected)
