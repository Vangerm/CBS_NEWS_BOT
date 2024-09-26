import vk_api
import asyncio
import logging
from filters.filters import IsAdmin
from aiogram import Router
from aiogram.types import Message, URLInputFile
from aiogram.filters import Command, CommandStart


logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='У меня пока нет функционала, '
                         'я помогаю с новостями\n'
                         'Но ты можешь узнать свой id, напиши мне /getid')


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='У меня пока нет функционала, '
                         'я помогаю с новостями\n'
                         'Но ты можешь узнать свой id, напиши мне /getid')


@router.message(Command(commands='getid'))
async def process_get_id_command(message: Message):
    await message.answer(text=str(message.chat.id))


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
                if attachments[0]['type'] == 'photo':
                    url = attachments[0]['photo']['orig_photo']['url']
                photo = URLInputFile(url)
                await message.bot.send_photo(
                        telegram_group_id,
                        photo,
                        caption=vk_post['text']
                    )
            else:
                await message.bot.send_message(
                        telegram_group_id,
                        vk_post['text']
                    )
        await asyncio.sleep(1800)
