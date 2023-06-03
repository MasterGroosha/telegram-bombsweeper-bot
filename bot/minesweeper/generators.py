from itertools import product
from random import sample
from typing import List, Tuple


def generate_square_field(k: int) -> List[List]:
    result = []
    for i in range(k):
        result.append([0] * k)
    return result


def __find_neighbours(x: int, y: int, size: int) -> List[Tuple]:
    """
    Finds neighbours for a cell. Those which fall out of the field are skipped
    :param x: current cell's X coord
    :param y: current cell's Y coord
    :param size: field single dimension size (because field is square)
    :return: list of (x, y) pairs of valid neighbours
    """
    return [
        (x + dx, y + dy) for dx, dy in product([-1, 0, 1], repeat=2)
        if (dx or dy) and 0 <= x + dx < size and 0 <= y + dy < size
    ]


def generate_custom(size: int, bombs: int, predefined: Tuple[int, int]) -> List[List]:
    """
    Generates custom square field with bombs (*).
    If cell contains a bomb, it has "*" value.
    Otherwise, it contains a number of adjacent bomb cells.

    :param size: a single dimension of a field
    :param bombs: bombs count for this field
    :param predefined: coordinates of cell, which MUST be free of bombs
    :return: an array of arrays of cells.
    """
    field = generate_square_field(size)
    freeCells = list(product(range(size), repeat=2))
    freeCells.remove(predefined)
    for x, y in sample(freeCells, bombs):
        field[x][y] = "*"
        for nx, ny in __find_neighbours(x, y, size):
            if field[nx][ny] != "*":
                field[nx][ny] += 1
    return field
