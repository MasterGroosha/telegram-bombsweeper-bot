from bot.minesweeper.states import CellMask

game_won = [
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 1},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 4}
    ],
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 0},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 1, 'y': 1},
        {'value': '*', 'mask': CellMask.HIDDEN, 'x': 1, 'y': 2},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 1, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 2, 'y': 0},
        {'value': 3, 'mask': CellMask.OPEN, 'x': 2, 'y': 1},
        {'value': '*', 'mask': CellMask.HIDDEN, 'x': 2, 'y': 2},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 2, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 2, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 0},
        {'value': '*', 'mask': CellMask.HIDDEN, 'x': 3, 'y': 1},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 3, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 3, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 4, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 4, 'y': 1},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 4, 'y': 2},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 4, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 4, 'y': 4}
    ]
]

one_open_cell = [
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 0},
        {'value': '*', 'mask': CellMask.HIDDEN, 'x': 0, 'y': 1},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 0, 'y': 2},
        {'value': 0, 'mask': CellMask.HIDDEN, 'x': 0, 'y': 3},
        {'value': 0, 'mask': CellMask.HIDDEN, 'x': 0, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 1, 'y': 0},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 1, 'y': 1},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 1, 'y': 2},
        {'value': 0, 'mask': CellMask.HIDDEN, 'x': 1, 'y': 3},
        {'value': 0, 'mask': CellMask.HIDDEN, 'x': 1, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 2, 'y': 0},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 2, 'y': 1},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 2, 'y': 2},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 2, 'y': 3},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 2, 'y': 4}
    ],
    [
        {'value': '*', 'mask': CellMask.HIDDEN, 'x': 3, 'y': 0},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 3, 'y': 1},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 3, 'y': 2},
        {'value': '*', 'mask': CellMask.HIDDEN, 'x': 3, 'y': 3},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 3, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 4, 'y': 0},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 4, 'y': 1},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 4, 'y': 2},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 4, 'y': 3},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 4, 'y': 4}
    ]
]

game_in_progress = [
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 1},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 4}
    ],
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 1, 'y': 1},
        {'value': '*', 'mask': CellMask.FLAG, 'x': 1, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 1, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 2, 'y': 0},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 2, 'y': 1},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 2, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 2, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 2, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 0},
        {'value': '*', 'mask': CellMask.FLAG, 'x': 3, 'y': 1},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 3, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 3},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 4, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 4, 'y': 1},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 4, 'y': 2},
        {'value': '*', 'mask': CellMask.HIDDEN, 'x': 4, 'y': 3},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 4, 'y': 4}
    ]
]


all_flags_correct_has_hidden_cells = [
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 1},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 0, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 4}
    ],
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 1, 'y': 1},
        {'value': '*', 'mask': CellMask.FLAG, 'x': 1, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 1, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 2, 'y': 0},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 2, 'y': 1},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 2, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 2, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 2, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 0},
        {'value': '*', 'mask': CellMask.FLAG, 'x': 3, 'y': 1},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 3, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 3},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 4, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 4, 'y': 1},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 4, 'y': 2},
        {'value': '*', 'mask': CellMask.FLAG, 'x': 4, 'y': 3},
        {'value': 1, 'mask': CellMask.HIDDEN, 'x': 4, 'y': 4}
    ]
]

more_flags_than_should = [
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 0},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 1},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 2},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 0, 'y': 4}
    ],
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 0},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 1},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 2},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 3},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 1, 'y': 4}
    ],
    [
        {'value': 0, 'mask': CellMask.OPEN, 'x': 2, 'y': 0},
        {'value': 0, 'mask': CellMask.OPEN, 'x': 2, 'y': 1},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 2, 'y': 2},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 2, 'y': 3},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 2, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 0},
        {'value': 1, 'mask': CellMask.OPEN, 'x': 3, 'y': 1},
        {'value': 3, 'mask': CellMask.OPEN, 'x': 3, 'y': 2},
        {'value': '*', 'mask': CellMask.FLAG, 'x': 3, 'y': 3},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 3, 'y': 4}
    ],
    [
        {'value': 1, 'mask': CellMask.OPEN, 'x': 4, 'y': 0},
        {'value': '*', 'mask': CellMask.FLAG, 'x': 4, 'y': 1},
        {'value': 3, 'mask': CellMask.FLAG, 'x': 4, 'y': 2},
        {'value': '*', 'mask': CellMask.FLAG, 'x': 4, 'y': 3},
        {'value': 2, 'mask': CellMask.OPEN, 'x': 4, 'y': 4}
    ]
]
