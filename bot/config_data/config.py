from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    group_id: int


@dataclass
class VkBot:
    token: str
    group_id: int


@dataclass
class Config:
    tg_bot: TgBot
    vk_bot: VkBot


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            group_id=env('TG_GROUP_ID')
        ),
        vk_bot=VkBot(
            token=env('VK_TOKEN'),
            group_id=env.int('VK_GROUP_ID')
        )
    )
