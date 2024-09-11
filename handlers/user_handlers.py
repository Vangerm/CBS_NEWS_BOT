import vk_api
import time
import requests
from aiogram import Router, F
from config_data.config import load_config
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandStart


router = Router()
config = load_config()
admin_ids = config.tg_bot.admin_ids


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='У меня пока нет функционала, '
                         'я помогаю с новостями\n'
                         'Но ты можешь узнать свой id, напиши мне \\getid')


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='У меня пока нет функционала, '
                         'я помогаю с новостями\n'
                         'Но ты можешь узнать свой id, напиши мне \\getid')


@router.message(Command(commands='getid'))
async def process_get_id_command(message: Message):
    await message.answer(text=str(message.chat.id))


@router.message(Command(commands='startbot') and F.from_user.id.in_(admin_ids))
async def process_start_bot_command(message: Message):
    telegram_group_id = config.tg_bot.group_id
    vk_bot_token = config.vk_bot.token
    vk_group_id = config.vk_bot.group_id

    post_id = 0

    # подключение по токену
    vk_session = vk_api.VkApi(token=vk_bot_token)
    # подключение к вк
    vk = vk_session.get_api()

    while True:
        vk_post_info = vk.wall.get(owner_id=-vk_group_id, count=1)
        if vk_post_info['items'][0]['id'] != post_id:
            post_id = vk_post_info['items'][0]['id']
            if len(vk_post_info['items'][0]['attachments']) and\
                    vk_post_info['items'][0]['attachments'][0]['type'] == 'photo':
                url = vk_post_info['items'][0]['attachments'][0]['photo']['orig_photo']['url']
                photo_response = requests.get(url)
                with open("photos/photo.jpg", 'wb') as photo_file:
                    photo_file.write(photo_response.content)
                photo = FSInputFile('photos/photo.jpg')
                await message.bot.send_photo(telegram_group_id, photo, caption=vk_post_info['items'][0]['text'])
            else:
                await message.bot.send_message(telegram_group_id, vk_post_info['items'][0]['text'])
        time.sleep(1800)
