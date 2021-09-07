from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.cbdata import cb_newgame


def make_newgame_keyboard() -> InlineKeyboardMarkup:
    available_options = [
        (5, 3), (6, 5), (7, 7)  # (size, bombs)
    ]
    keyboard = InlineKeyboardMarkup()
    for size, bombs in available_options:
        keyboard.add(InlineKeyboardButton(
            text=f"Play {size}×{size} field, {bombs} bombs",
            callback_data=cb_newgame.new(size=size, bombs=bombs, as_separate="no")
        ))

    return keyboard


def make_replay_keyboard(size: int, bombs: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        text=f"New game ({size}×{size} field, {bombs} bombs)",
        callback_data=cb_newgame.new(size=size, bombs=bombs, as_separate="yes")))
    keyboard.add(InlineKeyboardButton(text="New game (other)", callback_data="choose_newgame"))
    return keyboard
