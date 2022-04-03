from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_commands(bot: Bot):
    data = [
        (
            [
                BotCommand(command="start", description="New Game"),
                BotCommand(command="help", description="How to play Bombsweeper?"),
                BotCommand(command="stats", description="Your personal statistics")
            ],
            BotCommandScopeAllPrivateChats(),
            None
        )
    ]
    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)
