from datetime import datetime
from uuid import uuid4
from typing import Dict

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.minesweeper.game import get_newgame_data, untouched_cells_count, all_flags_match_bombs, make_text_table
from bot.minesweeper.states import ClickMode, CellMask
from bot.keyboards.kb_minefield import make_keyboard_from_minefield
from bot.cbdata import cb_click, cb_switch_mode, cb_switch_flag
from bot.db.models import GameHistoryEntry


async def log_game(session: AsyncSession, data: Dict, telegram_id: int, status: str):
    """
    Send end game event to database

    :param session: SQLAlchemy DB session
    :param data: game data dictionary (only size is taken for now)
    :param telegram_id: Player's Telegram ID
    :param status: "win" or "lose"
    """
    entry = GameHistoryEntry()
    entry.game_id = data["game_id"]
    entry.played_at = datetime.utcnow()
    entry.telegram_id = telegram_id
    entry.field_size = data["game_data"]["size"]
    entry.victory = status == "win"
    session.add(entry)
    await session.commit()


async def check_callback_data(call: types.CallbackQuery, state: FSMContext, callback_data: Dict, session: AsyncSession):
    """
    This is a "middleware" function, which does some checks to prevent duplicating code and breaking the logic
    """
    fsm_data = await state.get_data()
    game_data = fsm_data.get("game_data", {})
    cells = game_data.get("cells")
    game_id = fsm_data.get("game_id")

    if game_id is None:
        await call.message.edit_text("Something went wrong with this game, so it was removed.", reply_markup=None)
        await call.answer()
        return
    elif game_id != callback_data.get("game_id"):
        if cells is not None:
            await call.message.edit_text(call.message.html_text + f"\n\n{make_text_table(cells)}", reply_markup=None)
        else:
            await call.message.edit_text("Something went wrong with this game, so it was removed.", reply_markup=None)
        await call.answer(show_alert=True, text="This game is inaccessible, because there is more recent one!")
        return

    # Choose the right "real" function to call
    cb_prefix = callback_data.get("@")
    if cb_prefix == "press":
        await callback_open_square(call, state, callback_data, session)
    elif cb_prefix == "flag":
        await add_or_remove_flag(call, state, callback_data, session)
    elif cb_prefix == "switchmode":
        await switch_click_mode(call, state, callback_data)


async def callback_newgame(call: types.CallbackQuery, state: FSMContext):
    # todo: add separate buttons for different fields (e.g. 5x5, 6x6 and 7x7)
    size = 5
    bombs = 3

    game_id = str(uuid4())
    newgame_dict = {"game_id": game_id, "game_data": get_newgame_data(size, bombs)}
    await state.set_data(newgame_dict)
    await call.message.edit_text(call.message.html_text + "\n\nGame started!")
    await call.message.answer(
        f"You're currently playing {size}x{size} field, {bombs} bombs",
        reply_markup=make_keyboard_from_minefield(newgame_dict["game_data"]["cells"], game_id, ClickMode.CLICK)
    )
    await call.answer()


async def callback_open_square(call: types.CallbackQuery, state: FSMContext,
                               callback_data: Dict, session: AsyncSession):
    """
    Called when player clicks a HIDDEN cell (without any flags or numbers)
    """
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data", {})
    cells = game_data.get("cells")

    x = int(callback_data["x"])
    y = int(callback_data["y"])

    # This cell contained a bomb
    if cells[x][y]["value"] == "*":
        cells[x][y]["mask"] = CellMask.BOMB
        await call.message.edit_text(
            call.message.html_text + f"\n\n{make_text_table(cells)}\n\nYou lost :(",
            reply_markup=None
        )
        await log_game(session, fsm_data, call.from_user.id, "lose")
    # This cell contained a number
    else:
        cells[x][y]["mask"] = CellMask.OPEN
        # If this is the last cell to open...
        if untouched_cells_count(cells) == 0:
            # ...and all flags stand on bombs
            if all_flags_match_bombs(cells):
                await call.message.edit_text(
                    call.message.html_text + f"\n\n{make_text_table(cells)}\n\nYou won! 🎉",
                    reply_markup=None
                )
                await log_game(session, fsm_data, call.from_user.id, "win")
            # ...or some flags stand on numbers
            else:
                await state.update_data(game_data=game_data)
                await call.message.edit_reply_markup(
                    make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
                )
                await call.answer(
                    show_alert=True,
                    text="Looks like you've placed more flags than there are bombs on field. Please check them again."
                )
        # If this is not the last cell to open
        else:
            await state.update_data(game_data=game_data)
            await call.message.edit_reply_markup(
                make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
            )
    await call.answer()


async def switch_click_mode(call: types.CallbackQuery, state: FSMContext, callback_data: Dict):
    """
    Called when player switches from CLICK (open) mode to FLAG mode
    """
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data", {})
    cells = game_data.get("cells")

    game_data["current_mode"] = int(callback_data["new_mode"])
    await state.update_data(game_data=game_data)

    await call.message.edit_reply_markup(
        make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
    )
    await call.answer()


async def add_or_remove_flag(call: types.CallbackQuery, state: FSMContext,
                             callback_data: Dict, session: AsyncSession):
    """
    Called when player puts a flag on HIDDEN cell or clicks a flag to remove it
    """
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data", {})
    cells = game_data.get("cells")

    action = callback_data["action"]
    flag_x = int(callback_data["x"])
    flag_y = int(callback_data["y"])

    if action == "remove":
        cells[flag_x][flag_y].update(mask=CellMask.HIDDEN)
        await state.update_data(game_data=game_data)
        await call.message.edit_reply_markup(
            make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
        )
    elif action == "add":
        cells[flag_x][flag_y].update(mask=CellMask.FLAG)
        # See callback_open_square() for explanation
        if untouched_cells_count(cells) == 0:
            if all_flags_match_bombs(cells):
                await call.message.edit_text(
                    call.message.html_text + f"\n\n{make_text_table(cells)}\n\nYou won! 🎉",
                    reply_markup=None
                )
                await log_game(session, fsm_data, call.from_user.id, "win")
            else:
                await state.update_data(game_data=game_data)
                await call.message.edit_reply_markup(
                    make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
                )
                await call.answer(
                    show_alert=True,
                    text="Looks like you've placed more flags than there are bombs on field. "
                         "Please check them again."
                )
                return
        else:
            await state.update_data(game_data=game_data)
            await call.message.edit_reply_markup(
                make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
            )
    await call.answer()


async def callback_ignore(call: types.CallbackQuery):
    """
    Called when player clicks on an open number.
    In this case, we simply ignore this callback.
    """
    await call.answer()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(callback_newgame, text="newgame")
    dp.register_callback_query_handler(callback_ignore, text="ignore")
    dp.register_callback_query_handler(check_callback_data, cb_click.filter())
    dp.register_callback_query_handler(check_callback_data, cb_switch_flag.filter())
    dp.register_callback_query_handler(check_callback_data, cb_switch_mode.filter())
