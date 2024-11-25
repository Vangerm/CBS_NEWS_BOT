import asyncio
import logging.config
from aiogram import Bot, Dispatcher

from bot.loger.logging_settings import logging_config
from bot.config_data.config import load_config
from bot.handlers import get_routers
from bot.utils.nats_connect import connect_to_nats
from bot.utils.start_consumer import start_poll_vk_posts


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info('Starting bot')

    # Получаем конфигурационные данные
    config = load_config()

    # Подключаемся к NATS
    nc, js = await connect_to_nats(servers=config.nats.servers)

    # Активация телеграмм бота
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # dp['tg_group_id'] = config.tg_bot.group_id
    # dp['vk_bot_token'] = config.vk_bot.token
    # dp['vk_group_id'] = config.vk_bot.group_id
    # dp['admin_ids'] = config.tg_bot.admin_ids
    # dp['nc'] = nc
    # dp['js'] = js

    # подключение перехвата сообщений в личку боту
    dp.include_routers(*get_routers())

    # Запускаем polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.gather(
            dp.start_polling(
                bot,
                js=js,
                tg_group_id=config.tg_bot.group_id,
                vk_bot_token=config.vk_bot.token,
                vk_group_id=config.vk_bot.group_id,
                admin_ids=config.tg_bot.admin_ids,
                subject_publisher=config.delayed_consumer.subject_publisher
            ),
            start_poll_vk_posts(
                nc=nc,
                js=js,
                bot=bot,
                subject_consumer=config.delayed_consumer.subject_consumer,
                stream=config.delayed_consumer.stream,
                durable_name=config.delayed_consumer.durable_name
            )
        )
        # await dp.start_polling(bot, _translator_hub=translator_hub)
    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем соединение с NATS
        await nc.close()
        logger.info('Connection to NATS closed')


if __name__ == '__main__':
    asyncio.run(main())
