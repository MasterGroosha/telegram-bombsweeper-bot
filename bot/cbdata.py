from aiogram.dispatcher.filters.callback_data import CallbackData

from bot.minesweeper.states import ClickMode


class NewGameCallbackFactory(CallbackData, prefix="newgame"):
    size: int
    bombs: int
    as_separate: bool


class ClickCallbackFactory(CallbackData, prefix="press"):
    game_id: str
    x: int
    y: int


class SwitchFlagCallbackFactory(CallbackData, prefix="flag"):
    game_id: str
    action: str
    x: int
    y: int


class SwitchModeCallbackFactory(CallbackData, prefix="switchmode"):
    game_id: str
    new_mode: int


class IgnoreCallbackFactory(CallbackData, prefix="ignore"):
    x: int
    y: int
