from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart


user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='У меня пока нет функционала, '
                         'я помогаю с новостями\n'
                         'Но ты можешь узнать свой id, напиши мне /getid')


@user_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='У меня пока нет функционала, '
                         'я помогаю с новостями\n'
                         'Но ты можешь узнать свой id, напиши мне /getid')


@user_router.message(Command(commands='getid'))
async def process_get_id_command(message: Message):
    await message.answer(text=str(message.chat.id))
