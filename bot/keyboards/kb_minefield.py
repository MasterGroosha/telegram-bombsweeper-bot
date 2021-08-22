from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.cbdata import cb_switch_mode, cb_click, cb_switch_flag
from minesweeper.generators import generate_square_field
from minesweeper.states import ClickMode, MaskFieldSquareStatus


def make_keyboard_from_minefield(minefield: List[List], fieldmask: List[List], game_id: str, click_mode: int):
    """

    :param minefield:
    :param fieldmask:
    :param game_id:
    :param click_mode:
    :return:
    """
    kb_field = generate_square_field(len(minefield))
    for y in range(len(minefield)):
        for x in range(len(minefield[0])):
            fieldmask_value = fieldmask[x][y]
            if fieldmask_value == MaskFieldSquareStatus.OPEN:
                kb_field[x][y] = InlineKeyboardButton(text=minefield[x][y], callback_data="ignore")
            elif fieldmask_value == MaskFieldSquareStatus.HIDDEN:
                btn = InlineKeyboardButton(text="•")
                if click_mode == ClickMode.OPEN:
                    btn.callback_data = cb_click.new(game_id=game_id, x=x, y=y)
                else:
                    btn.callback_data = cb_switch_flag.new(game_id=game_id, action="add", x=x, y=y)
                    # btn.callback_data = cb_flag.new(game_id=game_id, x=x, y=y)
                kb_field[x][y] = btn
            elif fieldmask_value == MaskFieldSquareStatus.BOMB:
                kb_field[x][y] = InlineKeyboardButton(text="💥", callback_data="ignore")
            elif fieldmask_value == MaskFieldSquareStatus.FLAG:
                kb_field[x][y] = InlineKeyboardButton(
                    text="🚩",
                    callback_data=cb_switch_flag.new(game_id=game_id, action="remove", x=x, y=y)
                )

    result_kb = InlineKeyboardMarkup(inline_keyboard=kb_field)

    # Add switch mode button
    if click_mode == ClickMode.FLAG:
        switch_mode_btn = InlineKeyboardButton(
            text="🔄 Current mode: Flag",
            callback_data=cb_switch_mode.new(game_id=game_id, new_mode=ClickMode.OPEN))
    else:
        switch_mode_btn = InlineKeyboardButton(
            text="🔄 Current mode: Click",
            callback_data=cb_switch_mode.new(game_id=game_id, new_mode=ClickMode.FLAG))
    result_kb.row(switch_mode_btn)
    return result_kb
