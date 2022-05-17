from typing import Dict, List, Tuple, Union, Set

from texttable import Texttable

from bot.minesweeper.generators import generate_custom, generate_square_field
from bot.minesweeper.states import CellMask, ClickMode


def get_fake_newgame_data(size: int, bombs: int) -> Dict:
    """
    Prepares a new game dictionary

    :param size: field size (a field is a size x size square)
    :param bombs: number of bombs to place
    :return: a dictionary with field data for a new game
    """
    result = {"current_mode": ClickMode.CLICK, "size": size, "bombs": bombs, "initial": True}
    field = generate_square_field(size)
    for x in range(size):
        for y in range(size):
            field[x][y] = {"value": field[x][y], "mask": CellMask.HIDDEN, "x": x, "y": y}
    result["cells"] = field
    return result


def get_real_game_data(size: int, bombs: int, predefined: Tuple[int, int]) -> List[List[Dict]]:
    field = generate_custom(size, bombs, predefined)
    for x in range(size):
        for y in range(size):
            field[x][y] = {"value": field[x][y], "mask": CellMask.HIDDEN, "x": x, "y": y}
    return field


def untouched_cells_count(cells: List[List[Dict]]) -> int:
    """
    Counts the number of "untouched" cells: those which status is HIDDEN

    :param cells: array of array of cells dicts
    :return: number of cells with HIDDEN status
    """
    counter = 0
    for row in cells:
        for cell in row:
            if cell["mask"] == CellMask.HIDDEN:
                counter += 1
    return counter


def all_flags_match_bombs(cells: List[List[Dict]]) -> bool:
    """
    Checks whether all flags are placed correctly
    and there are no flags over regular cells (not bombs)

    :param cells: array of array of cells dicts
    :return: True if all flags are placed correctly
    """
    for row in cells:
        for cell in row:
            if cell["mask"] == CellMask.FLAG and cell["value"] != "*":
                return False
    return True


def all_free_cells_are_open(cells: List[List[Dict]]) -> bool:
    """
    Checks whether all non-bombs cells are open

    :param cells: array of array of cells dicts
    :return: True if all non-bombs cells are in OPEN state
    """
    hidden_cells_count = 0
    for row in cells:
        for cell in row:
            if cell["mask"] != CellMask.OPEN and cell["value"] != "*":
                hidden_cells_count += 1
    return hidden_cells_count == 0


class CellsChecker:
    """
    This is a special class to check minefield cells
    """

    ROW = 0     # first item in tuple is row
    COL = 1  # second item in tuple is column

    def __init__(self, cells: List[List[Union[Dict, int]]]):
        self.cells = cells
        self.size = len(cells)
        self.checked_cells: Set[Tuple[int, int]] = set()

    def get_cells_to_open(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        When user clicks on empty (value 0) field, we need to open all adjacent cells
        until there is a non-zero cell in every direction.
        We use depth search to find all cells to open

        This function is called recursively until every non-zero adjacent cell is found

        :param cell: a tuple containing row and column coordinates of cell to check
        :return: list of cells which must be open
        """
        result = [cell]

        # current_cell_value is always a dict except when running tests
        current_cell_value = self.cells[cell[self.ROW]][cell[self.COL]]
        if isinstance(current_cell_value, Dict):
            current_cell_value = current_cell_value["value"]

        if current_cell_value != 0:
            return result

        self.checked_cells.add(cell)

        adjacent_cells = (
            (cell[self.ROW] - 1, cell[self.COL]),      # up
            (cell[self.ROW] + 1, cell[self.COL]),      # down
            (cell[self.ROW], cell[self.COL] - 1),      # left
            (cell[self.ROW], cell[self.COL] + 1),      # right
            (cell[self.ROW] - 1, cell[self.COL] - 1),  # up left
            (cell[self.ROW] - 1, cell[self.COL] + 1),  # up right
            (cell[self.ROW] + 1, cell[self.COL] - 1),  # down left
            (cell[self.ROW] + 1, cell[self.COL] + 1),  # down right
        )

        for row_index, col_index in adjacent_cells:
            if 0 <= row_index < self.size \
                    and 0 <= col_index < self.size \
                    and (row_index, col_index) not in self.checked_cells:
                result += self.get_cells_to_open((row_index, col_index))
        return list(set(result))


def gather_open_cells(
        cells: List[List[Union[Dict, int]]],
        current: Tuple[int, int],
) -> List[Tuple[int, int]]:
    """
    If current cell stores value 0, find the whole block of numbers.
    A search goes in all directions until every direction has non-zero values

    Note: integer arrays are allowed to run tests

    :param cells: array of array of cells dicts
    :param current: (row, column) of the current cell
    :return: after all recursion calls, returns unique list of cells coordinates in block
    """

    checker = CellsChecker(cells)
    return checker.get_cells_to_open(current)


def make_text_table(cells: List[List[Dict]]) -> str:
    """
    Makes a text representation of game field using texttable library

    :param cells: array of array of cells dicts
    :return: a pretty-formatted field
    """
    table = Texttable()
    cells_size = len(cells)
    table.set_cols_width([3] * cells_size)
    table.set_cols_align(["c"] * cells_size)

    data_rows = []
    for cell_row in cells:
        data_single_row = []
        for cell in cell_row:
            cell_mask = cell["mask"]
            if cell_mask == CellMask.OPEN:
                data_single_row.append(cell["value"])
            elif cell_mask == CellMask.HIDDEN:
                if cell["value"] == "*":
                    data_single_row.append("💣")
                else:
                    data_single_row.append("•")
            elif cell_mask == CellMask.FLAG:
                if cell["value"] == "*":
                    data_single_row.append("🚩")
                else:
                    data_single_row.append("🚫")
            elif cell_mask == CellMask.BOMB:
                data_single_row.append("💥")
        data_rows.append(data_single_row)
    table.add_rows(data_rows, header=False)
    return f"<code>{table.draw()}</code>"
