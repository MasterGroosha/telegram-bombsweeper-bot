from itertools import chain
from typing import Dict, List, Tuple, Union, Set

from texttable import Texttable

from bot.minesweeper.generators import generate_custom, generate_square_field
from bot.minesweeper.states import CellMask, ClickMode, GameState


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


def ensure_real_game_field(game_data: Dict, first_click_coords: Tuple[int, int]):
    """
    Ensures that we're operating on a real game field, not an empty one.
    This is because player must not blow themselves up on first click,
    so initial game field is completely empty

    :param game_data: player's current game data
    :param first_click_coords: (x, y) of clicked button
    :return: modifies {game_data} in-place, returns nothing
    """
    # If this is the first click, it's time to generate the real game field
    if game_data["initial"] is True:
        cells = get_real_game_data(
            size=game_data["size"],
            bombs=game_data["bombs"],
            predefined=(first_click_coords[0], first_click_coords[1])
        )
        game_data["cells"] = cells
        game_data["initial"] = False


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

    :param cells: list of list of cells dicts
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


def analyze_game_field(game_field: List[List[Dict]]) -> GameState:
    has_hidden_numbers = False
    has_hidden_cells = False

    for cell in list(chain(*game_field)):
        if cell["mask"] == CellMask.HIDDEN:
            has_hidden_cells = True
            if cell["value"] != "*":
                has_hidden_numbers = True
                break
        else:
            if cell["value"] != "*" and cell["mask"] != CellMask.OPEN:
                has_hidden_numbers = True

    if not has_hidden_cells:
        if not has_hidden_numbers:
            return GameState.VICTORY
        else:
            return GameState.MORE_FLAGS_THAN_BOMBS
    if not has_hidden_numbers:
        return GameState.VICTORY
    return GameState.HAS_HIDDEN_NUMBERS


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


def update_game_field(cells: List[List[Dict]], x: int, y: int):
    """
    Updates game field in memorys.
    If cell value is zero, open this cell and all adjacent cells recursively.
    Otherwise, reveal current cell (x, y) only

    :param cells: list of list of cells dicts
    :param x: row coordinate of tap/click
    :param y: column coordinate of tap/click
    :return: updates object in-place, returns nothing
    """
    if cells[x][y]["value"] == 0:
        for item in gather_open_cells(cells, (x, y)):
            cells[item[0]][item[1]]["mask"] = CellMask.OPEN
    elif cells[x][y]["value"] == "*":
        cells[x][y]["mask"] = CellMask.BOMB
    else:
        cells[x][y]["mask"] = CellMask.OPEN


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
