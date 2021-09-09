from aiogram import Dispatcher, types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import GameHistoryEntry


async def show_stats(message: types.Message, session: AsyncSession):
    """
    Get player personal statistics

    :param message: Telegram message with /stats command
    :param session: SQLAlchemy DB session
    """
    game_data_request = await session.execute(
        select(GameHistoryEntry).where(GameHistoryEntry.telegram_id == message.from_user.id)
    )
    game_data = game_data_request.scalars().all()
    if len(game_data) == 0:
        await message.answer("You don't have any stats yet! Press /start and play a game of Bombsweeper")
        return
    user_data = {}

    # Gather wins and loses, grouping them by field size locally
    item: GameHistoryEntry
    for item in game_data:
        user_data.setdefault(item.field_size, {"wins": 0, "loses": 0})
        if item.victory is True:
            user_data[item.field_size]["wins"] += 1
        else:
            user_data[item.field_size]["loses"] += 1

    # Calculate total games for each mode along with winrate.
    result_text_array = []
    total_games = 0
    for field_size, field_data in user_data.items():
        total_current = field_data["loses"] + field_data["wins"]
        total_games += total_current

        if field_data["loses"] == 0:
            winrate = 100
        else:
            winrate = field_data["wins"] / total_current * 100

        result_text_array.append(
            "💣 <b>{size}×{size}</b> field:\nGames: <b>{total}</b>. "
            "Wins: <b>{wins}</b> (<b>{winrate:.0f}%</b>)".format(
                size=field_size,
                total=total_current,
                wins=field_data["wins"],
                winrate=winrate
            ))
    # Add a header to the beginning of result message
    result_text_array.insert(0, f"📊 <u>Your personal stats</u>:\nTotal games played: <b>{total_games}</b>")
    await message.answer("\n\n".join(result_text_array))


def register_statistics_handlers(dp: Dispatcher):
    dp.register_message_handler(show_stats, commands="stats")
