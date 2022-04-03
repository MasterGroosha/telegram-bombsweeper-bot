import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from magic_filter import F
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.commands import set_commands
from bot.configreader import config
from bot.handlers import default_commands, statistics, callbacks
from bot.middlewares.check_active_game import CheckActiveGameMiddleware
from bot.middlewares.db import DbSessionMiddleware


async def main():
    # Logging to stdout
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Creating DB engine for PostgreSQL
    engine = create_async_engine(config.postgres_dsn, future=True, echo=False)

    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Creating bot and its dispatcher
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    if config.custom_bot_api:
        bot.session.api = TelegramAPIServer.from_base(config.custom_bot_api, is_local=True)

    # Choosing FSM storage
    if config.bot_fsm_storage == "memory":
        dp = Dispatcher(storage=MemoryStorage())
    else:
        dp = Dispatcher(storage=RedisStorage.from_url(config.redis_dsn))

    # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type == "private")

    # Register middlewares
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(CheckActiveGameMiddleware())
    dp.callback_query.middleware(DbSessionMiddleware(db_pool))

    dp.include_router(default_commands.router)
    dp.include_router(statistics.router)
    dp.include_router(callbacks.router)

    # Register /-commands in UI
    await set_commands(bot)

    try:
        if not config.webhook_domain:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        else:
            # Suppress aiohttp access log completely
            aiohttp_logger = logging.getLogger("aiohttp.access")
            aiohttp_logger.setLevel(logging.CRITICAL)

            # Setting webhook
            await bot.set_webhook(
                url=config.webhook_domain + config.webhook_path,
                drop_pending_updates=True,
                allowed_updates=dp.resolve_used_update_types()
            )

            # Creating an aiohttp application
            app = web.Application()
            SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.webhook_path)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host=config.app_host, port=config.app_port)
            await site.start()

            # Running it forever
            await asyncio.Event().wait()
    finally:
        await bot.session.close()


asyncio.run(main())
