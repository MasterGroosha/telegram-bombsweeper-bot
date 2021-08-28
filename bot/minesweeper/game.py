from typing import Dict, List

from texttable import Texttable

from bot.minesweeper.generators import generate_custom
from bot.minesweeper.states import CellMask, ClickMode


def get_newgame_data(size: int, bombs: int) -> Dict:
    """
    Prepares a new game dictionary

    :param size: field size (a field is a size x size square)
    :param bombs: number of bombs to place
    :return: a dictionary with field data for a new game
    """
    result = {"current_mode": ClickMode.CLICK, "size": size, "bombs": bombs}
    field = generate_custom(size, bombs)
    for x in range(size):
        for y in range(size):
            field[x][y] = {"value": field[x][y], "mask": 0, "x": x, "y": y}
    result["cells"] = field
    return result


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
    print(table.draw())
    return f"<code>{table.draw()}</code>"
