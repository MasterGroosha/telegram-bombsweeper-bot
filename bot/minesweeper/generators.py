from contextlib import suppress
from typing import List, Tuple
from random import randint


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
    curr_x = x
    curr_y = y
    result = []
    # All possible placements.
    # First letter means vertical (U - Up, C - Center, D - Down)
    # Second letter means horizontal (L - Left, C - Center, R - Right)
    options = {"UL", "UC", "UR", "CL", "CR", "DL", "DC", "DR"}

    # If we are at left side (0, x)
    if curr_x - 1 < 0:
        for i in ("UL", "CL", "DL"):
            options.remove(i)
    # if we are at right side (%size%, x)
    if curr_x + 1 == size:
        for i in ("UR", "CR", "DR"):
            options.remove(i)
    # if we are on top (x, 0)
    if curr_y - 1 < 0:
        for i in ("UL", "UC", "UR"):
            with suppress(KeyError):
                options.remove(i)
    if curr_y + 1 == size:
        for i in ("DL", "DC", "DR"):
            with suppress(KeyError):
                options.remove(i)

    for option in options:
        if option == "UL":
            result.append((curr_x - 1, curr_y - 1))
        elif option == "UC":
            result.append((curr_x, curr_y - 1))
        elif option == "UR":
            result.append((curr_x + 1, curr_y - 1))
        elif option == "CL":
            result.append((curr_x - 1, curr_y))
        elif option == "CR":
            result.append((curr_x + 1, curr_y))
        elif option == "DL":
            result.append((curr_x - 1, curr_y + 1))
        elif option == "DC":
            result.append((curr_x, curr_y + 1))
        elif option == "DR":
            result.append((curr_x + 1, curr_y + 1))
    return result


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
