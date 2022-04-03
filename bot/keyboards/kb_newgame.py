from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.cbdata import NewGameCallbackFactory


def make_newgame_keyboard() -> InlineKeyboardMarkup:
    available_options = [
        (5, 3), (6, 5), (7, 7)  # (size, bombs)
    ]
    keyboard = InlineKeyboardBuilder()
    for size, bombs in available_options:
        keyboard.row(InlineKeyboardButton(
            text=f"Play {size}×{size} field, {bombs} bombs",
            callback_data=NewGameCallbackFactory(size=size, bombs=bombs, as_separate=False).pack()
        ))

    return keyboard.as_markup()


def make_replay_keyboard(size: int, bombs: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(
        text=f"New game ({size}×{size} field, {bombs} bombs)",
        callback_data=NewGameCallbackFactory(size=size, bombs=bombs, as_separate=True).pack()))
    keyboard.row(InlineKeyboardButton(text="New game (other)", callback_data="choose_newgame"))
    return keyboard.as_markup()
