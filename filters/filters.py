from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        # self.admin_ids = admin_ids
        pass

    async def __call__(self, message: Message, admin_ids: list) -> bool:
        return message.from_user.id in admin_ids
