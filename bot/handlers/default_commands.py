from aiogram import Dispatcher, types


async def cmd_start(message: types.Message):
    await message.answer("Обработка /start")


async def cmd_help(message: types.Message):
    await message.answer("Обработка /help")


def register_default_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_help, commands="help")
