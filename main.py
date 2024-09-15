import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import load_config
from handlers import user_handlers, other_handlers


async def main() -> None:
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    # Получаем конфигурационные данные
    config = load_config()

    # Заполняем конфигурационными данными переменные
    telegram_bot_token = config.tg_bot.token

    # Активация телеграмм бота
    bot: Bot = Bot(token=telegram_bot_token)
    dp: Dispatcher = Dispatcher()

    # подключение перехвата сообщений в личку боту
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
