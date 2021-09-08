from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from bot.keyboards.kb_newgame import make_newgame_keyboard


async def show_newgame_cb(call: CallbackQuery):
    await call.message.answer("Press a button below to start a new game (previous one will be dismissed)\n"
                              "Note: 6×6 and 7×7 fields look best on bigger screens or Desktop apps.",
                              reply_markup=make_newgame_keyboard())
    await call.message.delete_reply_markup()
    await call.answer()


async def show_newgame_msg(message: Message):
    await message.answer("Press a button below to start a new game (previous one will be dismissed)\n"
                         "Note: 6×6 and 7×7 fields look best on bigger screens or Desktop apps.\n\n"
                         "Press /help if you're unsure how to play Bombsweeper.",
                         reply_markup=make_newgame_keyboard())


async def cmd_help(message: Message):
    await message.answer("A quick guide how to play Bombsweeper is available here: "
                         "https://telegra.ph/bombsweeper-how-to-play-09-08")


def register_default_handlers(dp: Dispatcher):
    dp.register_message_handler(show_newgame_msg, commands="start")
    dp.register_callback_query_handler(show_newgame_cb, text="choose_newgame")
    dp.register_message_handler(cmd_help, commands="help")
