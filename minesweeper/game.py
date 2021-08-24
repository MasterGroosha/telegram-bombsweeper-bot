from typing import Dict, List, Optional, Tuple

from texttable import Texttable

from minesweeper.generators import generate_custom
from minesweeper.states import MaskFieldSquareStatus
from minesweeper.states import ClickMode


def get_newgame_data(size: int, bombs: int) -> Dict:
    result = {"current_mode": ClickMode.CLICK, "size": size, "bombs": bombs}
    field = generate_custom(size, bombs)
    for x in range(size):
        for y in range(size):
            field[x][y] = {"value": field[x][y], "mask": 0, "x": x, "y": y}
    result["cells"] = field
    return result


def untouched_cells_count(cells: List[List[Dict]]) -> int:
    counter = 0
    for row in cells:
        for cell in row:
            if cell["mask"] == MaskFieldSquareStatus.HIDDEN:
                counter += 1
    return counter


def all_flags_match_bombs(cells: List[List[Dict]]) -> bool:
    for row in cells:
        for cell in row:
            if cell["mask"] == MaskFieldSquareStatus.FLAG and cell["value"] != "*":
                return False
    return True


def make_text_table(cells: List[List[Dict]], explosion: Optional[Tuple[int, int]] = None) -> str:
    table = Texttable()
    cells_size = len(cells)
    table.set_cols_width([3] * cells_size)
    table.set_cols_align(["c"] * cells_size)

    data_rows = []
    for cell_row in cells:
        data_single_row = []
        for cell in cell_row:
            cell_mask = cell["mask"]
            if cell_mask == MaskFieldSquareStatus.OPEN:
                data_single_row.append(cell["value"])
            elif cell_mask == MaskFieldSquareStatus.HIDDEN:
                if cell["value"] == "*":
                    data_single_row.append("💣")
                else:
                    data_single_row.append("•")
            elif cell_mask == MaskFieldSquareStatus.FLAG:
                if cell["value"] == "*":
                    data_single_row.append("🚩")
                else:
                    data_single_row.append("🚫")
            elif cell_mask == MaskFieldSquareStatus.BOMB:
                data_single_row.append("💥")
        data_rows.append(data_single_row)
    table.add_rows(data_rows, header=False)
    print(table.draw())
    return f"<code>{table.draw()}</code>"
