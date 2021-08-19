from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def cmd_start(message: types.Message, state: FSMContext):
    # показ клавиатуры с кнопкой start
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Start Game!", callback_data="newgame"))
    await message.answer("Press the button below to start a new game (previous one will be dismissed).\n"
                         "For now you cannot choose any options, so a 5x5 field will be used",
                         reply_markup=kb)


async def cmd_help(message: types.Message):
    await message.answer("Обработка /help")


def register_default_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_help, commands="help")
