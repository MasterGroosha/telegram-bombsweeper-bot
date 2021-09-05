from contextlib import suppress
from datetime import datetime
from uuid import uuid4
from typing import Dict

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from bot.minesweeper.game import (get_fake_newgame_data, untouched_cells_count, all_flags_match_bombs,
                                  all_free_cells_are_open, make_text_table, get_real_game_data, gather_open_cells)
from bot.minesweeper.states import ClickMode, CellMask
from bot.keyboards.kb_minefield import make_keyboard_from_minefield
from bot.cbdata import cb_newgame, cb_click, cb_switch_mode, cb_switch_flag, cb_ignore
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
    # If a user is quick enough, there might be 2 events with the same UUID.
    # There's not much we can do, so simply ignore it until we come up with a better solution
    with suppress(IntegrityError):
        await session.commit()


async def check_callback_data(call: types.CallbackQuery, state: FSMContext, callback_data: Dict, session: AsyncSession):
    """
    This is a "middleware" function, which does some checks to prevent duplicating code and breaking the logic
    """
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")

    if game_id is None:
        await call.message.edit_text("<i>This game is no longer accessible</i>", reply_markup=None)
        await call.answer()
        return
    elif game_id != callback_data.get("game_id"):
        await call.message.edit_text("<i>This game is no longer accessible</i>", reply_markup=None)
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


async def callback_newgame(call: types.CallbackQuery, state: FSMContext, callback_data: Dict):
    size = int(callback_data.get("size"))
    bombs = int(callback_data.get("bombs"))

    game_id = str(uuid4())
    newgame_dict = {"game_id": game_id, "game_data": get_fake_newgame_data(size, bombs)}
    await state.set_data(newgame_dict)
    await call.message.edit_text(
        f"You're currently playing <b>{size}×{size}</b> field, <b>{bombs}</b> bombs",
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

    x = int(callback_data["x"])
    y = int(callback_data["y"])

    # If this is the first click, it's time to generate the real game field
    if game_data["initial"] is True:
        cells = get_real_game_data(game_data["size"], game_data["bombs"], (x, y))
        game_data["cells"] = cells
        game_data["initial"] = False
    else:
        cells = game_data.get("cells")

    # This cell contained a bomb
    if cells[x][y]["value"] == "*":
        cells[x][y]["mask"] = CellMask.BOMB
        with suppress(MessageNotModified):
            await call.message.edit_text(
                call.message.html_text + f"\n\n{make_text_table(cells)}\n\n<b>You lost</b> 😞",
                reply_markup=None
            )
        await log_game(session, fsm_data, call.from_user.id, "lose")
    # This cell contained a number
    else:
        # If cell is empty (0), open all adjacent squares
        if cells[x][y]["value"] == 0:
            for item in gather_open_cells(cells, (x, y)):
                cells[item[0]][item[1]]["mask"] = CellMask.OPEN
        # ... or just the current one
        else:
            cells[x][y]["mask"] = CellMask.OPEN

        if all_free_cells_are_open(cells):
            with suppress(MessageNotModified):
                await call.message.edit_text(
                    call.message.html_text + f"\n\n{make_text_table(cells)}\n\n<b>You won!</b> 🎉",
                    reply_markup=None
                )
            await log_game(session, fsm_data, call.from_user.id, "win")
            await call.answer()
            return
        # There are more flags than there should be
        elif untouched_cells_count(cells) == 0 and not all_flags_match_bombs(cells):
            await state.update_data(game_data=game_data)
            with suppress(MessageNotModified):
                await call.message.edit_reply_markup(
                    make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
                )
            await call.answer(
                show_alert=True,
                text="Looks like you've placed more flags than there are bombs on field. Please check them again."
            )
            return
        # If this is not the last cell to open
        else:
            await state.update_data(game_data=game_data)
            with suppress(MessageNotModified):
                await call.message.edit_reply_markup(
                    make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
                )
    await call.answer(cache_time=2)


async def switch_click_mode(call: types.CallbackQuery, state: FSMContext, callback_data: Dict):
    """
    Called when player switches from CLICK (open) mode to FLAG mode
    """
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data", {})
    cells = game_data.get("cells")

    if game_data["initial"] is True:
        await call.answer(show_alert=True, text="You can only place flags after first click!")
        return

    game_data["current_mode"] = int(callback_data["new_mode"])
    await state.update_data(game_data=game_data)

    with suppress(MessageNotModified):
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
        with suppress(MessageNotModified):
            await call.message.edit_reply_markup(
                make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
            )
    elif action == "add":
        cells[flag_x][flag_y].update(mask=CellMask.FLAG)
        # See callback_open_square() for explanation
        if untouched_cells_count(cells) == 0:
            if all_flags_match_bombs(cells):
                with suppress(MessageNotModified):
                    await call.message.edit_text(
                        call.message.html_text + f"\n\n{make_text_table(cells)}\n\n<b>You won!</b> 🎉",
                        reply_markup=None
                    )
                await log_game(session, fsm_data, call.from_user.id, "win")
            else:
                await state.update_data(game_data=game_data)
                with suppress(MessageNotModified):
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
            with suppress(MessageNotModified):
                await call.message.edit_reply_markup(
                    make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
                )
    await call.answer(cache_time=1)


async def callback_ignore(call: types.CallbackQuery):
    """
    Called when player clicks on an open number.
    In this case, we simply ignore this callback.
    """
    await call.answer(cache_time=3)


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(callback_newgame, cb_newgame.filter())
    dp.register_callback_query_handler(callback_ignore, cb_ignore.filter())
    dp.register_callback_query_handler(check_callback_data, cb_click.filter())
    dp.register_callback_query_handler(check_callback_data, cb_switch_flag.filter())
    dp.register_callback_query_handler(check_callback_data, cb_switch_mode.filter())
