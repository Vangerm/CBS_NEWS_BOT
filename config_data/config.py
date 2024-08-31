from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class VkBot:
    vk_token: str


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
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        vk_bot=VkBot(
            vk_token=env('VK_TOKEN')
        )
    )