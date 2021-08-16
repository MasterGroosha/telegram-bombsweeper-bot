from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from typing import Dict, Any


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config):
        super(ConfigMiddleware, self).__init__()
        self.config = config

    async def on_pre_process_message(self, message: types.Message, data: Dict[str, Any]):
        data["config"] = self.config
