import vk_api
from vk_api.bot_longpoll import (
                                VkBotLongPoll,
                                VkBotEventType)

import logging
# from nats.js.api import StreamConfig
import asyncio
from aiogram import Router
from aiogram.types import (
                            Message,
                            FSInputFile,
                            URLInputFile,
                            InputMediaPhoto)
from aiogram.filters import Command

from bot.filters.filters import IsAdmin


logger = logging.getLogger(__name__)

admin_router = Router()


async def listen_vk_group(
        message: Message,
        longpoll: VkBotLongPoll,
        telegram_group_id: int
        ):
    logger.info('Start check vk news')

    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            try:
                post_text = event.obj['text']
                attachments = event.obj['attachments']

                # await nc.request("vk_poster", post_text.encode())

                await create_tg_poster(
                    message,
                    attachments,
                    post_text,
                    telegram_group_id)
            except Exception as e:
                logger.exception(e)


async def create_tg_poster(
        message: Message,
        attachments: list,
        post_text: str,
        telegram_group_id: int):

    urls = list()
    first_photo_caption = True

    for attachment in attachments:
        if attachment['type'] == 'photo':
            url = attachment['photo']['orig_photo']['url']
            urls.append(url)

    if len(urls) == 1:
        await message.bot.send_photo(
            telegram_group_id,
            URLInputFile(urls[0]),
            caption=post_text
        )

    elif len(urls) > 1:
        photos = list()

        for url in urls:
            if first_photo_caption:
                photos.append(InputMediaPhoto(
                    media=URLInputFile(url),
                    caption=post_text
                ))
            else:
                photos.append(InputMediaPhoto(
                    media=URLInputFile(url)
                ))

        await message.bot.send_media_group(
            telegram_group_id,
            photos
        )

    else:
        await message.bot.send_message(
            telegram_group_id,
            post_text
        )


# Получение логер файла
@admin_router.message(Command(commands='getlog'), IsAdmin())
async def admin_get_log_command(message: Message):
    await message.answer_document(FSInputFile('loger/logs.log'))


# запуск прослушки новостей
@admin_router.message(Command(commands='startbot'), IsAdmin())
async def process_start_bot_command(
                                    message: Message,
                                    telegram_group_id,
                                    vk_bot_token,
                                    vk_group_id
                                    ):

    # подключение по токену
    vk_session = vk_api.VkApi(token=vk_bot_token)
    # подключение к вк
    vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, -vk_group_id)

    # loop = asyncio.get_event_loop()

    # stream_config = StreamConfig(
    #     name="SocialMediaStream",
    #     subjects=["vk_poster"],
    #     retention="limits",
    #     max_bytes=300 * 1024 * 1024,
    #     max_msg_size=10 * 1024 * 1024,
    #     storage="file",
    #     allow_direct=True,
    # )

    # await js.add_stream(stream_config)

    await listen_vk_group(
                        message,
                        longpoll,
                        telegram_group_id
                        )

    # try:
    #     loop.run_until_complete(await listen_vk_group(
    #                     message,
    #                     longpoll,
    #                     telegram_group_id,
    #                     nc
    #                     ))
    #     loop.run_forever()
    #     loop.close()
    # except Exception as e:
    #     logger.exception(e)
