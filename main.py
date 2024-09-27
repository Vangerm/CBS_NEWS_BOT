import asyncio
import logging.config
from loger.logging_settings import logging_config
from aiogram import Bot, Dispatcher
from config_data.config import load_config
from handlers import (user_handlers,
                      other_handlers,
                      admin_handlers)


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info('Starting bot')

    # Получаем конфигурационные данные
    config = load_config()

    # Заполняем конфигурационными данными переменные
    telegram_bot_token = config.tg_bot.token

    # Активация телеграмм бота
    bot: Bot = Bot(token=telegram_bot_token)
    dp: Dispatcher = Dispatcher()

    dp['telegram_group_id'] = config.tg_bot.group_id
    dp['vk_bot_token'] = config.vk_bot.token
    dp['vk_group_id'] = config.vk_bot.group_id
    dp['admin_ids'] = config.tg_bot.admin_ids

    # подключение перехвата сообщений в личку боту
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
