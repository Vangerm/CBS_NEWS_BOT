import vk_api
import logging
from vk_api.bot_longpoll import (
                                VkBotLongPoll,
                                VkBotEventType)
from aiogram import Router
from aiogram.types import (
                            Message,
                            FSInputFile,
                            URLInputFile,
                            InputMediaPhoto)
from aiogram.filters import Command
from bot.filters.filters import IsAdmin


logger = logging.getLogger(__name__)

router = Router()


async def create_tg_poster(
        message: Message,
        attachments,
        post_text,
        telegram_group_id):

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
@router.message(Command(commands='getlog'), IsAdmin())
async def admin_get_log_command(message: Message):
    await message.answer_document(FSInputFile('loger/logs.log'))


# запуск прослушки новостей
@router.message(Command(commands='startbot'), IsAdmin())
async def process_start_bot_command(
                                    message: Message,
                                    telegram_group_id,
                                    vk_bot_token,
                                    vk_group_id
                                    ):
    logger.info('Start check vk news')

    # подключение по токену
    vk_session = vk_api.VkApi(token=vk_bot_token)
    # подключение к вк
    vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, -vk_group_id)

    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            post_text = event.obj['text']
            attachments = event.obj['attachments']

            await create_tg_poster(
                message,
                attachments,
                post_text,
                telegram_group_id)
