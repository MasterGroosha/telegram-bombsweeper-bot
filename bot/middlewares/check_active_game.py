from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, html
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import CallbackQuery

from bot.cbdata import ClickCallbackFactory, SwitchFlagCallbackFactory, SwitchModeCallbackFactory


class CheckActiveGameMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        """
        Check whether game is active. This middleware is intended for CallbackQuery only!
        """
        real_handler: HandlerObject = data.get("handler")
        need_check_handler = real_handler.flags.get("need_check_game")
        if not need_check_handler:
            return await handler(event, data)
        state = data["state"]
        user_data = await state.get_data()
        fsm_game_id = user_data.get("game_id")
        if not fsm_game_id:
            await event.message.edit_text(
                text=f"{html.italic('This game is no longer accessible')}",
                reply_markup=None
            )
            return
        else:
            callback_data = data.get("callback_data")
            if isinstance(callback_data, (ClickCallbackFactory, SwitchFlagCallbackFactory, SwitchModeCallbackFactory)):
                if callback_data.game_id != fsm_game_id:
                    await event.message.edit_text(
                        text=f"{html.italic('This game is no longer accessible')}",
                        reply_markup=None
                    )
                    await event.answer(
                        text="This game is inaccessible, because there is more recent one!",
                        show_alert=True
                    )
                    return
        return await handler(event, data)
