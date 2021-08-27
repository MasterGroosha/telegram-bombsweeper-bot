import asyncio
import logging
from os.path import join

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from bot.config_reader import load_config
# from bot.middlewares.config import ConfigMiddleware
from bot.middlewares.db import DbSessionMiddleware
from bot.db.utils import make_connection_string
from bot.handlers.default_commands import register_default_handlers
from bot.handlers.callbacks import register_callbacks

logger = logging.getLogger(__name__)


# async def set_bot_commands(bot: Bot):
#     data = [
#         (
#             [BotCommand(command="help", description="help только для @Groosha")],
#             BotCommandScopeChat(chat_id=1795872),
#             None
#         ),
#         (
#             [BotCommand(command="help", description="help для всех")],
#             BotCommandScopeDefault(),
#             None
#         ),
#     ]
#     for commands_list, commands_scope, language in data:
#         await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)


async def main():
    # Logging to stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Reading config file
    config = load_config()

    # Creating DB engine for PostgreSQL
    engine = create_async_engine(
        make_connection_string(config.db),
        future=True,
        echo=False
    )

    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Creating bot and its dispatcher
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Register handlers
    register_default_handlers(dp)
    register_callbacks(dp)

    # Register middlewares
    # dp.middleware.setup(ConfigMiddleware(config))
    dp.middleware.setup(DbSessionMiddleware(db_pool))

    # Register /-commands in UI
    # await set_bot_commands(bot)

    logger.info("Starting bot")

    # Starting polling
    # await dp.skip_updates()  # uncomment to skip pending updates (optional)
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


asyncio.run(main())
