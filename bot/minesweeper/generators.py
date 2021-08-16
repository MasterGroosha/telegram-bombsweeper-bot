from contextlib import suppress
from typing import List, Tuple
from random import randint


def print_field(field: List[List]):
    for row in field:
        for item in row:
            print(f"{item}\t", end="")
        print()


def generate_square_field(k: int) -> List[List]:
    result = []
    for i in range(k):
        result.append([0 for x in range(k)])
    return result


def generate_valid_coordinates(x: int, y: int, size: int) -> List[Tuple]:
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


def generate_custom(size: int, maxbombs: int):
    field = generate_square_field(size)
    current_count = 0

    while current_count < maxbombs:
        x = randint(0, 4)
        y = randint(0, 4)

        if field[x][y] == "*":
            print("hit!")
            continue
        field[x][y] = "*"
        neigbours = generate_valid_coordinates(x, y, 5)
        for nx, ny in neigbours:
            if field[nx][ny] != "*":
                field[nx][ny] += 1

        current_count += 1

    print_field(field)


if __name__ == '__main__':
    generate_custom(5, 3)