from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.cbdata import cb_switch_mode, cb_click, cb_switch_flag
from minesweeper.states import ClickMode, MaskFieldSquareStatus


def make_keyboard_from_minefield(cells: List[List], game_id: str, click_mode: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for cells_row in cells:
        kb_row = []
        for cell in cells_row:
            # This is a button for OPEN status
            btn = InlineKeyboardButton(text=cell["value"], callback_data="ignore")
            mask_value = cell["mask"]
            x = cell["x"]
            y = cell["y"]
            # Check other statuses
            if mask_value == MaskFieldSquareStatus.HIDDEN:
                btn.text = "•"
                if click_mode == ClickMode.CLICK:
                    btn.callback_data = cb_click.new(game_id=game_id, x=x, y=y)
                else:
                    btn.callback_data = cb_switch_flag.new(game_id=game_id, action="add", x=x, y=y)
            # todo: remove BOMB button and replace with in-text field
            elif mask_value == MaskFieldSquareStatus.BOMB:
                btn.text = "💥"
            elif mask_value == MaskFieldSquareStatus.FLAG:
                btn.text = "🚩"
                btn.callback_data = cb_switch_flag.new(game_id=game_id, action="remove", x=x, y=y)
            kb_row.append(btn)
        keyboard.row(*kb_row)

    # Add switch flag mode button
    if click_mode == ClickMode.FLAG:
        switch_mode_btn = InlineKeyboardButton(
            text="🔄 Current mode: Flag",
            callback_data=cb_switch_mode.new(game_id=game_id, new_mode=ClickMode.CLICK))
    else:
        switch_mode_btn = InlineKeyboardButton(
            text="🔄 Current mode: Click",
            callback_data=cb_switch_mode.new(game_id=game_id, new_mode=ClickMode.FLAG))
    keyboard.row(switch_mode_btn)

    return keyboard
