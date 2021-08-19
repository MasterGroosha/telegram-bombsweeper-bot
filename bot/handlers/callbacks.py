from uuid import uuid4

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from minesweeper.generators import generate_custom, generate_square_field


async def callback_newgame(call: types.CallbackQuery, state: FSMContext):
    size = 5
    newgame_dict = {
        "game_id": uuid4(),
        "cells_remaining": size * size,
        "minefield": generate_custom(size, 3),
        "maskfield": generate_square_field(size)
    }
    await state.update_data(**newgame_dict)
    await call.answer()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(callback_newgame, text="newgame")
