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


async def poster(
        message: Message,
        attachments,
        post_text,
        telegram_group_id):
    if len(attachments):
        if len(attachments) > 1:
            photos = list()
            id_photo = True
            for attachment in attachments:
                if attachment['type'] == 'photo':
                    url = attachment['photo']['orig_photo']['url']
                    if id_photo:
                        id_photo = False
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
        elif attachments[0]['type'] == 'photo':
            url = attachments[0]['photo']['orig_photo']['url']
            photo = URLInputFile(url)
            await message.bot.send_photo(
                telegram_group_id,
                photo,
                caption=post_text
            )
        elif attachments[0]['type'] == 'video':
            await message.bot.send_message(
                telegram_group_id,
                post_text
            )
        # elif attachments[0]['type'] == 'video':
        #     owner_id = vk_post_info['items'][0]['attachments'][0]['video']['owner_id']
        #     video_id = vk_post_info['items'][0]['attachments'][0]['video']['id']
        #     access_key = vk_post_info['items'][0]['attachments'][0]['video']['access_key']

        #     video = vk.video.get(videos=f'{owner_id}_{video_id}_{access_key}')
        #     url = video['items'][0]['player']

        #     input_video = URLInputFile(url)

        #     await message.bot.send_video(
        #             telegram_group_id,
        #             input_video,
        #             caption=vk_post['text']
        #     )

    else:
        await message.bot.send_message(
            telegram_group_id,
            post_text
        )


@router.message(Command(commands='getlog'), IsAdmin())
async def admin_get_log_command(message: Message):
    await message.answer_document(FSInputFile('loger/logs.log'))


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

            await poster(
                message,
                attachments,
                post_text,
                telegram_group_id)
