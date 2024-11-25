import logging

# from nats.js.api import StreamConfig
from aiogram import Router
from aiogram.types import (
                            Message,
                            FSInputFile)
from aiogram.filters import Command

from bot.filters.filters import IsAdmin
from bot.services.delay_service.publisher import vk_post_publisher


logger = logging.getLogger(__name__)

admin_router = Router()


# Получение логер файла
@admin_router.message(Command(commands='getlog'), IsAdmin())
async def admin_get_log_command(message: Message):
    await message.answer_document(FSInputFile('loger/logs.log'))


# запуск прослушки новостей
@admin_router.message(Command(commands='startbot'), IsAdmin())
async def process_start_bot_command(
                                    message: Message,
                                    tg_group_id,
                                    vk_bot_token,
                                    vk_group_id,
                                    js,
                                    subject_publisher
                                    ):
    await vk_post_publisher(
                            js=js,
                            tg_group_id=tg_group_id,
                            vk_group_id=vk_group_id,
                            vk_token=vk_bot_token,
                            subject=subject_publisher
    )

    await message.answer(text='Start check news.')
