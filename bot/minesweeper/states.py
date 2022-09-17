class ClickMode:
    CLICK = 0
    FLAG = 1


class CellMask:
    HIDDEN = 0
    OPEN = 1
    BOMB = 2
    FLAG = 3


class GameState:
    HAS_HIDDEN_CELLS = 0
    MORE_FLAGS_THAN_BOMBS = 1
    VICTORY = 2
