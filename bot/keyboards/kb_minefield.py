from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.cbdata import SwitchModeCallbackFactory, SwitchFlagCallbackFactory, ClickCallbackFactory, IgnoreCallbackFactory
from bot.minesweeper.states import ClickMode, CellMask


def make_keyboard_from_minefield(cells: List[List], game_id: str, click_mode: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for cells_row in cells:
        kb_row = []
        for cell in cells_row:
            mask_value = cell["mask"]
            x = cell["x"]
            y = cell["y"]
            # Check statuses
            if mask_value == CellMask.HIDDEN:
                btn = InlineKeyboardButton(text="•")
                if click_mode == ClickMode.CLICK:
                    btn.callback_data = ClickCallbackFactory(game_id=game_id, x=x, y=y).pack()
                else:
                    btn.callback_data = SwitchFlagCallbackFactory(game_id=game_id, action="add", x=x, y=y).pack()
            elif mask_value == CellMask.FLAG:
                btn = InlineKeyboardButton(
                    text="🚩",
                    callback_data=SwitchFlagCallbackFactory(game_id=game_id, action="remove", x=x, y=y).pack()
                )
            else:  # mask_value == CellMask.OPEN
                val = cell["value"]
                if val == 0:
                    val = "⠀"  # Empty symbol
                btn = InlineKeyboardButton(text=val, callback_data=IgnoreCallbackFactory(x=x, y=y).pack())
            kb_row.append(btn)
        keyboard.row(*kb_row)

    # Add switch flag mode button
    if click_mode == ClickMode.FLAG:
        switch_mode_btn = InlineKeyboardButton(
            text="🔄 Current mode: Flag",
            callback_data=SwitchModeCallbackFactory(game_id=game_id, new_mode=ClickMode.CLICK).pack()
        )
    else:
        switch_mode_btn = InlineKeyboardButton(
            text="🔄 Current mode: Click",
            callback_data=SwitchModeCallbackFactory(game_id=game_id, new_mode=ClickMode.FLAG).pack()
        )
    keyboard.row(switch_mode_btn)

    return keyboard.as_markup()
