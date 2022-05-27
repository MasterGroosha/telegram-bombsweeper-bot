from itertools import product
from random import randint
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
    current_count = 0

    while current_count < bombs:
        x = randint(0, size-1)
        y = randint(0, size-1)

        # Do not place a bomb on another bomb or on predefined place
        if (x == predefined[0] and y == predefined[1]) or field[x][y] == "*":
            continue
        field[x][y] = "*"
        neighbours = __find_neighbours(x, y, size)
        for nx, ny in neighbours:
            if field[nx][ny] != "*":
                field[nx][ny] += 1
        current_count += 1
    return field
