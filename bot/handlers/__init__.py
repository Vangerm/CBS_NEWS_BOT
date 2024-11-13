from aiogram import Router

from . import user_handlers
from . import admin_handlers
from . import other_handlers


def get_routers() -> list[Router]:
    return [
        user_handlers.user_router,
        admin_handlers.admin_router,
        other_handlers.other_router  # other_handlers - должен быть последним
    ]
