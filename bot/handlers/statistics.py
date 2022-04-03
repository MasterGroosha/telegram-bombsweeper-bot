from aiogram import Router, types
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import GameHistoryEntry
from bot.db.requests import get_games_by_id

router = Router()


@router.message(commands=["stats"])
async def show_stats(message: types.Message, session: AsyncSession):
    """
    Get player personal statistics

    :param message: Telegram message with /stats command
    :param session: SQLAlchemy DB session
    """
    games = await get_games_by_id(session, message.from_user.id)
    if len(games) == 0:
        await message.answer("You don't have any stats yet! Press /start and play a game of Bombsweeper")
        return
    user_data = {}

    # Gather wins and loses, grouping them by field size locally
    game: GameHistoryEntry
    for game in games:
        user_data.setdefault(game.field_size, {"wins": 0, "loses": 0})
        if game.victory is True:
            user_data[game.field_size]["wins"] += 1
        else:
            user_data[game.field_size]["loses"] += 1

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
