from dataclasses import dataclass
from os import getenv
from typing import Optional


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
class Redis:
    host: str


@dataclass
class App:
    webhook_enabled: bool
    webhook_domain: Optional[str]
    webhook_path: Optional[str]
    host: Optional[str]
    port: Optional[int]


@dataclass
class Config:
    tg_bot: TgBot
    db: DB
    redis: Redis
    app: App


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
        ),
        redis=Redis(
            host=getenv("REDIS_HOST")
        ),
        app=App(
            webhook_enabled=bool(getenv("WEBHOOK_ENABLED", False)),
            webhook_domain=getenv("WEBHOOK_DOMAIN"),
            webhook_path=getenv("WEBHOOK_PATH"),
            host=getenv("APP_HOST", "0.0.0.0"),
            port=int(getenv("APP_PORT", 9000))
        )
    )
