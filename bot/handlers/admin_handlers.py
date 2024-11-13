import vk_api
from vk_api.bot_longpoll import (
                                VkBotLongPoll,
                                VkBotEventType)

import logging
import signal
# import nats
# from nats.aio.msg import Msg
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
        telegram_group_id: int,
        nc
        ):
    logger.info('Start check vk news')

    async def stop():
        await asyncio.sleep(1)
        asyncio.get_running_loop().stop()

    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        asyncio.create_task(nc.close())
        asyncio.create_task(stop())

    for sig in ("SIGINT", "SIGTERM"):
        asyncio.get_running_loop().add_signal_handler(
            getattr(signal, sig), signal_handler
        )

    async def disconnected_cb():
        print("Got disconnected...")

    async def reconnected_cb():
        print("Got reconnected...")

    await nc.connect(
        "127.0.0.1",
        reconnected_cb=reconnected_cb,
        disconnected_cb=disconnected_cb,
        max_reconnect_attempts=-1,
    )

    async def help_request(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(
            "Received a message on '{subject}': {data}".format(
                subject=subject, data=data
            )
        )

    await nc.subscribe('vk_poste', 'auto_post', help_request)

    # for i in range(1, 1000000):
    #     await asyncio.sleep(60)
    #     try:
    #         response = await nc.request("help", b"hi")
    #         print(response)
    #     except Exception as e:
    #         print("Error:", e)

    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            try:
                await nc.request("vk_poste", b"hi")
                post_text = event.obj['text']
                attachments = event.obj['attachments']

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
                                    vk_group_id,
                                    nc
                                    ):

    # подключение по токену
    vk_session = vk_api.VkApi(token=vk_bot_token)
    # подключение к вк
    vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, -vk_group_id)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(await listen_vk_group(
                        message,
                        longpoll,
                        telegram_group_id,
                        nc
                        ))
        loop.run_forever()
        loop.close()
    except Exception as e:
        logger.exception(e)
