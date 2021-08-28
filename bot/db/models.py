from sqlalchemy import Column, Integer, BigInteger, Boolean
from sqlalchemy.dialects.postgresql import UUID

from bot.db.base import Base


class GameHistoryEntry(Base):
    __tablename__ = "gameshistory"

    game_id = Column(UUID, primary_key=True)
    played_at = Column(DateTime, nullable=False)
    telegram_id = Column(BigInteger, nullable=False)
    field_size = Column(Integer, nullable=False)
    victory = Column(Boolean, nullable=False)
