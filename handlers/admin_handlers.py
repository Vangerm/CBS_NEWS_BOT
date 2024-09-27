from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from filters.filters import IsAdmin


router = Router()


@router.message(Command(commands='getlog'), IsAdmin())
async def admin_get_log_command(message: Message):
    await message.answer_document(FSInputFile('loger/logs.log'))
