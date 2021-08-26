from dataclasses import dataclass
from os import getenv


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str):
    return Config(
        tg_bot=TgBot(
            token=getenv("BOT_TOKEN"),
        )
    )
