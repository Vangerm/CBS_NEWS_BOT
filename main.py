import asyncio
import logging
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
# from aiogram import Bot, Dispatcher, F
# from aiogram.filters import Command, CommandStart
# from aiogram.types import Message, FSInputFile
from config_data.config import load_config


async def main() -> None:
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    config = load_config()

    # telegram_bot_token = config.tg_bot.token
    vk_bot_token = config.vk_bot.token
    vk_group_id = config.vk_bot.group_id

    # bot: Bot = Bot(token=telegram_bot_token)
    # dp: Dispatcher = Dispatcher()

    vk_session = vk_api.VkApi(token=vk_bot_token)

    vk = vk_session.get_api()

    group_info = vk.wall.get(owner_id=-vk_group_id, count=1)
    print(group_info)

    # longpoll = VkLongPoll(vk_session)

    # for event in longpoll.listen():
    #     if event.type == VkEventType.WALL_POST_NEW:
    #         print(vk.wall.get(count=1))

    # await bot.delete_webhook(drop_pending_updates=True)
    # await dp.start_polling(bot)


asyncio.run(main())
