import vk_api
import asyncio
import logging
import requests
from aiogram import Router
from aiogram.types import (
                            Message,
                            FSInputFile,
                            URLInputFile,
                            InputMediaPhoto)
from aiogram.filters import Command
from filters.filters import IsAdmin


logger = logging.getLogger(__name__)

router = Router()


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

    post_id = 0

    # подключение по токену
    vk_session = vk_api.VkApi(token=vk_bot_token)
    # подключение к вк
    vk = vk_session.get_api()

    while True:
        vk_post_info = vk.wall.get(owner_id=vk_group_id, count=2)
        is_pinned = 0

        if vk_post_info['items'][0].get('is_pinned', 0):
            is_pinned = 1

        vk_post = vk_post_info['items'][is_pinned]

        if vk_post['id'] != post_id:
            post_id = vk_post['id']
            attachments = vk_post['attachments']

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
                                    caption=vk_post['text']
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
                        caption=vk_post['text']
                    )
                elif attachments[0]['type'] == 'video':
                    owner_id = vk_post_info['items'][0]['attachments'][0]['video']['owner_id']
                    video_id = vk_post_info['items'][0]['attachments'][0]['video']['id']
                    access_key = vk_post_info['items'][0]['attachments'][0]['video']['access_key']

                    video = vk.video.get(videos=f'{owner_id}_{video_id}_{access_key}')
                    url = video['items'][0]['player']
                    # url = f'https://api.vk.com/method/video.get?videos={owner_id}_{video_id}&access_token={access_key}&v=5.131'

                    input_video = URLInputFile(url)

                    # response = requests.get(url)
                    # data = response.json()
                    # if 'response' in data and len(data['response']) > 0:
                    #     video_data = data['response'][0]
                    #     video_url = video_data['files']['mp4']


                    await message.bot.send_video(
                            telegram_group_id,
                            input_video,
                            caption=vk_post['text']
                    )
            else:
                await message.bot.send_message(
                        telegram_group_id,
                        vk_post['text']
                    )
        await asyncio.sleep(1800)
