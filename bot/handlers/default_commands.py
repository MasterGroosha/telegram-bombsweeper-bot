from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from bot.keyboards.kb_newgame import make_newgame_keyboard


async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Press a button below to start a new game (previous one will be dismissed)\n"
                         "Note: 6×6 and 7×7 fields look best on bigger screens or Desktop apps.",
                         reply_markup=make_newgame_keyboard())


async def cmd_help(message: types.Message):
    await message.answer("This is how you play Bombsweeper aka Minesweeper: https://youtu.be/dvvrOeITzG8")


def register_default_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_help, commands="help")
