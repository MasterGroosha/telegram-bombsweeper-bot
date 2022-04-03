from contextlib import suppress
from datetime import datetime
from typing import List, Dict

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import GameHistoryEntry


async def get_games_by_id(session: AsyncSession, user_id: int) -> List[GameHistoryEntry]:
    """
    Get game history for user

    :param session: SQLAlchemy DB session
    :param user_id: player's Telegram ID
    :return: list of GameHistoryEntry objects (can be empty)
    """
    game_data_request = await session.execute(
        select(GameHistoryEntry).where(GameHistoryEntry.telegram_id == user_id)
    )
    return game_data_request.scalars().all()


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
