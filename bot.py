import asyncio
import logging


import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.client.bot import DefaultBotProperties
from aiogram_dialog import setup_dialogs
from backend.database.setup import create_engine, create_session_pool
from sqlalchemy.ext.asyncio import AsyncEngine

from config import load_config, Config
# from tgbot.handlers import routers_list
# from tgbot.middlewares.config import ConfigMiddleware
# from tgbot.middlewares.database import DatabaseMiddleware
from bot.services import broadcaster
# from tgbot.dialogs import setup_afina_dialogs






async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")

def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if config.bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()



async def main():
    setup_logging()

    config = load_config(".env")
    storage = get_storage(config)

    engine: AsyncEngine = create_engine(config.db)
    session_pool = create_session_pool(engine)
    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=storage)
    
    try:
        await bot.delete_webhook()
        await on_startup(bot, config.bot.admin_ids)
        await dp.start_polling(bot)
    finally:
        logging.info("stopped")

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()