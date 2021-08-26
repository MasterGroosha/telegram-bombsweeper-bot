from bot.config_reader import DB


def make_connection_string(db: DB, async_fallback: bool = False) -> str:
    result = f"postgresql+asyncpg://{db.login}:{db.password}@{db.host}:{db.port}/{db.name}"
    if async_fallback:
        result += "?async_fallback=True"
    return result
