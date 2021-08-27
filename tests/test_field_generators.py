from typing import List, Tuple

import pytest

from bot.minesweeper import generators


@pytest.mark.parametrize(
    "x, y, size, expected",
    [
        [0, 0, 5, [(1, 0), (1, 1), (0, 1)]],  # Top left corner
        [0, 4, 5, [(0, 3), (1, 3), (1, 4)]],  # Bottom left corner
        [4, 0, 5, [(3, 0), (3, 1), (4, 1)]],  # Top right corner
        [4, 4, 5, [(4, 3), (3, 3), (3, 4)]],  # Bottom right corner,
        [2, 2, 5, [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]],  # Center
        [2, 0, 5, [(1, 0), (3, 0), (1, 1), (2, 1), (3, 1)]],  # Top middle
    ]
)
def test_valid_increments(x: int, y: int, size: int, expected: List[Tuple]):
    assert sorted(generators.__find_neighbours(x, y, size)) == sorted(expected)
