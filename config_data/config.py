from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class SqlConfiguration:
    host: str
    user: str
    password: str
    db: str


@dataclass
class Config:
    tg_bot: TgBot
    database: SqlConfiguration


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
        ),
        database=SqlConfiguration(
            host=env('SQL_HOST'),
            user=env('SQL_USER'),
            password=env('SQL_PASSWORD'),
            db=env('SQL_DATABASE'),
        )
    )