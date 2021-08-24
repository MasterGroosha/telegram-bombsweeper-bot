from uuid import uuid4
from typing import Dict, List, Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from minesweeper.game import get_newgame_data, untouched_cells_count, all_flags_match_bombs, is_victory, make_text_table
from minesweeper.states import ClickMode, MaskFieldSquareStatus
from bot.keyboards.kb_minefield import make_keyboard_from_minefield
from bot.cbdata import cb_click, cb_switch_mode, cb_switch_flag


async def callback_newgame(call: types.CallbackQuery, state: FSMContext):
    size = 5
    bombs = 3
    game_id = str(uuid4())
    newgame_dict = {"game_id": game_id, "game_data": get_newgame_data(size, bombs)}
    await state.set_data(newgame_dict)
    await call.message.edit_text(call.message.html_text + "\n\nGame started!")
    await call.message.answer(
        "This is a debug message, please, change it",
        reply_markup=make_keyboard_from_minefield(newgame_dict["game_data"]["cells"], game_id, ClickMode.CLICK)
    )
    await call.answer()


async def callback_open_square(call: types.CallbackQuery, state: FSMContext, callback_data: Dict):
    fsm_data = await state.get_data()
    game_data = fsm_data.get("game_data", {})
    cells = game_data.get("cells")
    game_id = fsm_data.get("game_id")

    # if not game_id:
    #     # todo:

    if fsm_data.get("game_id") != callback_data.get("game_id"):
        if cells is not None:
            await call.message.edit_text(call.message.html_text + f"\n\n{make_text_table(cells)}")
        await call.answer(show_alert=True, text="This game is inaccessible, because there is more recent one!")
        return

    x = int(callback_data["x"])
    y = int(callback_data["y"])

    if cells[x][y]["value"] == "*":  # user lost
        cells[x][y]["mask"] = MaskFieldSquareStatus.BOMB
        await call.message.edit_text(
            call.message.html_text + f"\n\n{make_text_table(cells)}\n\nYou lost :(",
            reply_markup=None
        )
    else:
        cells[x][y]["mask"] = MaskFieldSquareStatus.OPEN
        if untouched_cells_count(cells) == 0:
            if all_flags_match_bombs(cells):
                await call.message.edit_text(
                    call.message.html_text + f"\n\n{make_text_table(cells)}\n\nYou won! 🎉",
                    reply_markup=None
                )
            else:
                await state.update_data(game_data=game_data)
                await call.message.edit_reply_markup(
                    make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
                )
                await call.answer(
                    show_alert=True,
                    text="Looks like you've placed more flags than there are bombs on field. Please check them again."
                )
        else:
            await state.update_data(game_data=game_data)
            await call.message.edit_reply_markup(
                make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
            )
    await call.answer()


async def switch_click_mode(call: types.CallbackQuery, state: FSMContext, callback_data: Dict):
    # todo: get rid of code duplication
    fsm_data = await state.get_data()
    game_data = fsm_data.get("game_data", {})
    cells = game_data.get("cells")
    game_id = fsm_data.get("game_id")

    # if not game_id:
    #     # todo:

    if fsm_data.get("game_id") != callback_data.get("game_id"):
        if cells is not None:
            await call.message.edit_text(call.message.html_text + f"\n\n{make_text_table(cells)}")
        await call.answer(show_alert=True, text="This game is inaccessible, because there is more recent one!")
        return

    game_data["current_mode"] = int(callback_data["new_mode"])
    await state.update_data(game_data=game_data)

    await call.message.edit_reply_markup(
        make_keyboard_from_minefield(cells, game_id, game_data["current_mode"])
    )
    await call.answer()


async def callback_switch_flag_state(call: types.CallbackQuery, state: FSMContext, callback_data: Dict):
    async with state.proxy() as data:
        game_id = data["game_id"]
        # if fsm_data.get("game_id") != callback_data.get("game_id"):
        #     await call.answer(show_alert=True, text="This game is inaccessible, because there is more recent one!")
        #     # todo: replace keyboard with text (or with not working keyboard)
        #     return
        game_data = data["game_data"]
        minefield = game_data["minefield"]
        maskfield = game_data["maskfield"]
        action = callback_data["action"]
        x = int(callback_data["x"])
        y = int(callback_data["y"])
        if action == "add":
            game_data["maskfield"][x][y] = MaskFieldSquareStatus.FLAG
            print(f"{untouched_cells_count(maskfield)=}")
            print(f"{maskfield=}")
            # todo: duplicate code
            if untouched_cells_count(maskfield) == 0:
                if all_flags_match(minefield, maskfield):  # user won
                    # todo: show field
                    await call.message.edit_text(call.message.html_text + "\n\nYou won!", reply_markup=None)
                    await call.answer(show_alert=True, text="Congratulations! You won!")
                    return
                else:  # some flag is improperly placed, keep trying
                    await call.answer(
                        show_alert=True,
                        text="Looks like you've placed more flags than there are bombs on field. Please check them again."
                    )

        else:
            maskfield[x][y] = MaskFieldSquareStatus.HIDDEN
        await call.message.edit_reply_markup(
            make_keyboard_from_minefield(
                game_data["minefield"], game_data["maskfield"], game_id, game_data["current_mode"]
            )
        )


async def callback_ignore(call: types.CallbackQuery):
    await call.answer()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(callback_newgame, text="newgame")
    dp.register_callback_query_handler(callback_ignore, text="ignore")
    dp.register_callback_query_handler(callback_open_square, cb_click.filter())
    dp.register_callback_query_handler(callback_switch_flag_state, cb_switch_flag.filter())
    dp.register_callback_query_handler(switch_click_mode, cb_switch_mode.filter())
