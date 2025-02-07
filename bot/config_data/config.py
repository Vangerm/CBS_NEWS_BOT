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
class NatsConfig:
    servers: list[str]


@dataclass
class NatsDelayedConsumerConfig:
    subject_consumer: str
    subject_publisher: str
    stream: str
    durable_name: str


@dataclass
class Config:
    tg_bot: TgBot
    vk_bot: VkBot
    nats: NatsConfig
    delayed_consumer: NatsDelayedConsumerConfig


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
        ),
        nats=NatsConfig(
            servers=env.list('NATS_SERVERS')
        ),
        delayed_consumer=NatsDelayedConsumerConfig(
            subject_consumer=env('NATS_POLL_CONSUMER_SUBJECT'),
            subject_publisher=env('NATS_POST_PUBLISHER_SUBJECT'),
            stream=env('NATS_CONSUMER_STREAM'),
            durable_name=env('NATS_CONSUMER_DURABLE_NAME')
        )
    )
