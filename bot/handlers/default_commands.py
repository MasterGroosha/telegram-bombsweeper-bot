from aiogram import Router
from aiogram.types import Message, CallbackQuery

from bot.keyboards.kb_newgame import make_newgame_keyboard

router = Router()


@router.callback_query(text="choose_newgame")
async def show_newgame_cb(call: CallbackQuery):
    await call.message.answer(
        "Press a button below to start a new game (previous one will be dismissed)\n"
        "Note: 6×6 and 7×7 fields look best on bigger screens or Desktop apps.",
        reply_markup=make_newgame_keyboard()
    )
    await call.message.delete_reply_markup()
    await call.answer()


@router.message(commands=["start"])
async def show_newgame_msg(message: Message):
    await message.answer(
        "Press a button below to start a new game (previous one will be dismissed)\n"
        "Note: 6×6 and 7×7 fields look best on bigger screens or Desktop apps.\n\n"
        "Press /help if you're unsure how to play Bombsweeper.",
        reply_markup=make_newgame_keyboard()
    )


@router.message(commands=["help"])
async def cmd_help(message: Message):
    await message.answer("A quick guide how to play Bombsweeper is available here: "
                         "https://telegra.ph/bombsweeper-how-to-play-09-08")
