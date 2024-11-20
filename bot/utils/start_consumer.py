import logging

from aiogram import Bot
from bot.services.delay_service.consumer import VkPostConsumer

from nats.aio.client import Client
from nats.js.client import JetStreamContext


logger = logging.getLogger(__name__)


async def start_poll_vk_posts(
        nc: Client,
        js: JetStreamContext,
        bot: Bot,
        subject: str,
        stream: str,
        durable_name: str
) -> None:
    consumer = VkPostConsumer(
        nc=nc,
        js=js,
        bot=bot,
        subject=subject,
        stream=stream,
        durable_name=durable_name
    )
    logger.info('Start poll vk posts consumer')
    await consumer.start()
