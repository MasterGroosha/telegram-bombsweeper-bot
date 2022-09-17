from contextlib import suppress
from typing import Dict, List
from uuid import uuid4

from aiogram import types, Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from bot.cbdata import (NewGameCallbackFactory, ClickCallbackFactory, SwitchModeCallbackFactory,
                        SwitchFlagCallbackFactory, IgnoreCallbackFactory)
from bot.db.requests import log_game
from bot.keyboards.kb_minefield import make_keyboard_from_minefield
from bot.keyboards.kb_newgame import make_replay_keyboard
from bot.minesweeper.game import (get_fake_newgame_data, make_text_table, update_game_field,
                                  ensure_real_game_field, analyze_game_field)
from bot.minesweeper.states import ClickMode, CellMask, GameState

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


async def update_player_keyboard(
        callback: types.CallbackQuery,
        cells: List[List[Dict]],
        game_id: str,
        click_mode: int
):
    """
    Updates player's keyboard
    """
    with suppress(TelegramBadRequest):
        await callback.message.edit_reply_markup(
            make_keyboard_from_minefield(cells, game_id, click_mode)
        )


@router.callback_query(ClickCallbackFactory.filter(), flags={"need_check_game": True})
async def callback_open_square(call: types.CallbackQuery, state: FSMContext,
                               callback_data: ClickCallbackFactory, session: AsyncSession):
    """
    Called when player clicks a HIDDEN cell (without any flags or numbers)
    """

    async def finish_game(is_win: bool):
        """
        Finishes the game with either win or lose
        :param is_win: True if user won the game
        """
        added_text = "<b>You won!</b> 🎉" if is_win else "<b>You lost</b> 😞"

        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                call.message.html_text + f"\n\n{make_text_table(cells)}\n\n{added_text}",
                reply_markup=make_replay_keyboard(field_size, bombs)
            )
        await log_game(session, fsm_data, call.from_user.id, is_win)
        await call.answer()

    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data", {})
    field_size = int(game_data.get("size"))
    bombs = int(game_data.get("bombs"))

    x: int = callback_data.x
    y: int = callback_data.y

    # Get the real game field in case of the first click
    ensure_real_game_field(game_data, (x, y))
    cells = game_data.get("cells")

    # Update game field (in memory, not for user yet)
    update_game_field(cells, x, y)

    # Clicked cell contained a bomb
    if cells[x][y]["value"] == "*":
        await finish_game(is_win=False)
        return

    game_state = analyze_game_field(cells)
    if game_state == GameState.HAS_HIDDEN_NUMBERS:
        await state.update_data(game_data=game_data)
        await update_player_keyboard(call, cells, game_id, game_data["current_mode"])
        await call.answer()
    elif game_state == GameState.MORE_FLAGS_THAN_BOMBS:
        await state.update_data(game_data=game_data)
        await update_player_keyboard(call, cells, game_id, game_data["current_mode"])
        await call.answer(
            show_alert=True,
            text="Looks like you've placed more flags than there are bombs on the field. "
                 "Please check them again."
        )
    else:  # == GameState.Victory
        await finish_game(is_win=True)


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

    await update_player_keyboard(call, cells, game_id, game_data["current_mode"])
    await call.answer()


@router.callback_query(
    SwitchFlagCallbackFactory.filter(F.action == "remove"),
    flags={"need_check_game": True}
)
async def cb_remove_flag(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: SwitchFlagCallbackFactory
):
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data")
    cells = game_data.get("cells")

    cells[callback_data.x][callback_data.y].update(mask=CellMask.HIDDEN)
    await state.update_data(game_data=game_data)
    await update_player_keyboard(call, cells, game_id, game_data["current_mode"])
    await call.answer()


@router.callback_query(
    SwitchFlagCallbackFactory.filter(F.action == "add"),
    flags={"need_check_game": True}
)
async def cb_add_flag(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: SwitchFlagCallbackFactory
):
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    game_data = fsm_data.get("game_data")
    cells = game_data.get("cells")

    cells[callback_data.x][callback_data.y].update(mask=CellMask.FLAG)
    game_state = analyze_game_field(cells)
    if game_state == GameState.HAS_HIDDEN_NUMBERS:
        await state.update_data(game_data=game_data)
        await update_player_keyboard(call, cells, game_id, game_data["current_mode"])
        await call.answer()
    elif game_state == GameState.MORE_FLAGS_THAN_BOMBS:
        await state.update_data(game_data=game_data)
        await update_player_keyboard(call, cells, game_id, game_data["current_mode"])
        await call.answer(
            show_alert=True,
            text="Looks like you've placed more flags than there are bombs on the field. "
                 "Please check them again."
        )


@router.callback_query(IgnoreCallbackFactory.filter())
async def callback_ignore(call: types.CallbackQuery):
    """
    Called when player clicks on an open number.
    In this case, we simply ignore this callback.
    """
    await call.answer(cache_time=3)
