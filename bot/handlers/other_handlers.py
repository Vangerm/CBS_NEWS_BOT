from aiogram import Router
from aiogram.types import Message


other_router = Router()


@other_router.message()
async def send_empty_message(message: Message):
    await message.answer(text='У меня пока нет функционала, '
                         'я помогаю с новостями\n'
                         'Но ты можешь узнать свой id, напиши мне /getid')
