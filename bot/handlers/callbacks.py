from contextlib import suppress
from uuid import uuid4

from aiogram import types, Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from bot.cbdata import (NewGameCallbackFactory, ClickCallbackFactory, SwitchModeCallbackFactory,
                        SwitchFlagCallbackFactory, IgnoreCallbackFactory)
from bot.db.requests import log_game
from bot.keyboards.kb_minefield import make_keyboard_from_minefield
from bot.keyboards.kb_newgame import make_replay_keyboard
from bot.minesweeper.game import (get_fake_newgame_data, untouched_cells_count, all_flags_match_bombs,
                                  all_free_cells_are_open, make_text_table, get_real_game_data, gather_open_cells)
from bot.minesweeper.states import ClickMode, CellMask

router = Router()


@router.callback_query(NewGameCallbackFactory.filter())
async def callback_newgame(call: types.CallbackQuery, state: FSMContext, callback_data: NewGameCallbackFactory):
    size = callback_data.size
    bombs = callback_data.bombs
    game_id = str(uuid4())
    newgame_dict = {"game_id": game_id, "game_data": get_fake_newgame_data(size, bombs)}
    await state.set_data(newgame_dict)

    text = f"You're currently playing <b>{size}×{size}</b> field, <b>{bombs}</b> bombs"
    kb = make_keyboard_from_minefield(newgame_dict["game_data"]["cells"], game_id, ClickMode.CLICK)
    if callback_data.as_separate:
        await call.message.delete_reply_markup()
        await call.message.answer(text, reply_markup=kb)
    else:
        await call.message.edit_text(text, reply_markup=kb)
    await call.answer()


@router.callback_query(ClickCallbackFactory.filter(), flags={"need_check_game": True})
async def callback_open_square(call: types.CallbackQuery, state: FSMContext,
                               callback_data: ClickCallbackFactory, session: AsyncSession):
    """
    Called when player clicks a HIDDEN cell (without any flags or numbers)
    """
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data", {})
    field_size = int(game_data.get("size"))
    bombs = int(game_data.get("bombs"))

    x = callback_data.x
    y = callback_data.y

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
        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                call.message.html_text + f"\n\n{make_text_table(cells)}\n\n<b>You lost</b> 😞",
                reply_markup=make_replay_keyboard(field_size, bombs)
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
            with suppress(TelegramBadRequest):
                await call.message.edit_text(
                    call.message.html_text + f"\n\n{make_text_table(cells)}\n\n<b>You won!</b> 🎉",
                    reply_markup=make_replay_keyboard(field_size, bombs)
                )
            await log_game(session, fsm_data, call.from_user.id, "win")
            await call.answer()
            return
        # There are more flags than there should be
        elif untouched_cells_count(cells) == 0 and not all_flags_match_bombs(cells):
            await state.update_data(game_data=game_data)
            with suppress(TelegramBadRequest):
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
            with suppress(TelegramBadRequest):
                await call.message.edit_reply_markup(
                    make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
                )
    await call.answer(cache_time=2)


@router.callback_query(SwitchModeCallbackFactory.filter(), flags={"need_check_game": True})
async def switch_click_mode(call: types.CallbackQuery, state: FSMContext, callback_data: SwitchModeCallbackFactory):
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

    game_data["current_mode"] = callback_data.new_mode
    await state.update_data(game_data=game_data)

    with suppress(TelegramBadRequest):
        await call.message.edit_reply_markup(
            make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
        )
    await call.answer()


@router.callback_query(SwitchFlagCallbackFactory.filter(), flags={"need_check_game": True})
async def add_or_remove_flag(call: types.CallbackQuery, state: FSMContext,
                             callback_data: SwitchFlagCallbackFactory, session: AsyncSession):
    """
    Called when player puts a flag on HIDDEN cell or clicks a flag to remove it
    """
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data", {})
    cells = game_data.get("cells")
    field_size = int(game_data.get("size"))
    bombs = int(game_data.get("bombs"))

    action = callback_data.action
    flag_x = callback_data.x
    flag_y = callback_data.y

    if action == "remove":
        cells[flag_x][flag_y].update(mask=CellMask.HIDDEN)
        await state.update_data(game_data=game_data)
        with suppress(TelegramBadRequest):
            await call.message.edit_reply_markup(
                make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
            )
    elif action == "add":
        cells[flag_x][flag_y].update(mask=CellMask.FLAG)
        # See callback_open_square() for explanation
        if untouched_cells_count(cells) == 0:
            if all_flags_match_bombs(cells):
                with suppress(TelegramBadRequest):
                    await call.message.edit_text(
                        call.message.html_text + f"\n\n{make_text_table(cells)}\n\n<b>You won!</b> 🎉",
                        reply_markup=make_replay_keyboard(field_size, bombs)
                    )
                await log_game(session, fsm_data, call.from_user.id, "win")
            else:
                await state.update_data(game_data=game_data)
                with suppress(TelegramBadRequest):
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
            with suppress(TelegramBadRequest):
                await call.message.edit_reply_markup(
                    make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
                )
    await call.answer(cache_time=1)


@router.callback_query(IgnoreCallbackFactory.filter())
async def callback_ignore(call: types.CallbackQuery):
    """
    Called when player clicks on an open number.
    In this case, we simply ignore this callback.
    """
    await call.answer(cache_time=3)
