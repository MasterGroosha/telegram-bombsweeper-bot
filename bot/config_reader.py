from dataclasses import dataclass
from os import getenv


@dataclass
class TgBot:
    token: str


@dataclass
class DB:
    host: str
    port: int
    name: str
    login: str
    password: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DB


def load_config():
    return Config(
        tg_bot=TgBot(
            token=getenv("BOT_TOKEN"),
        ),
        db=DB(
            host=getenv("DB_HOST"),
            port=int(getenv("DB_PORT")),
            name=getenv("DB_NAME"),
            login=getenv("DB_USER"),
            password=getenv("DB_PASS")
        )
    )
