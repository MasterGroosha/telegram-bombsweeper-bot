import asyncio
import logging
from os.path import join

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config_reader import load_config
# from bot.middlewares.config import ConfigMiddleware
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
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Чтение файла конфигурации
    config = load_config()

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_default_handlers(dp)
    register_callbacks(dp)

    # Регистрация мидлвари
    # dp.middleware.setup(ConfigMiddleware(config))

    # Регистрация /-команд в интерфейсе
    # await set_bot_commands(bot)

    logger.info("Starting bot")

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


asyncio.run(main())
