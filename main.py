import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import user_handlers
from keyboards.main_menu import set_main_menu
from db.create_connection import create_connection
from db.init_db import init_db

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] - #%(levelname)-8s %(filename)s:'
               '%(lineno)d - %(name)s - %(message)s'
    )

    logger.info('Starting Bot')

    config: Config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    init_db(create_connection())

    dp = Dispatcher()
    dp.include_router(user_handlers.router)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass