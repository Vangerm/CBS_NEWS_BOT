from dataclasses import dataclass
from environs import Env


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
    nats: NatsConfig
    delayed_consumer: NatsDelayedConsumerConfig


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
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
