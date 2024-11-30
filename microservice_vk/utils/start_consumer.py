import logging

from microservice_vk.services.delay_service.consumer import VkLongPollConsumer

from nats.aio.client import Client
from nats.js.client import JetStreamContext


logger = logging.getLogger(__name__)


async def start_get_vk_post(
        nc: Client,
        js: JetStreamContext,
        subject_consumer: str,
        subject_publisher: str,
        stream: str,
        durable_name: str
        ) -> None:
    consumer = VkLongPollConsumer(
        nc=nc,
        js=js,
        subject_consumer=subject_consumer,
        subject_publisher=subject_publisher,
        stream=stream,
        durable_name=durable_name
    )

    await consumer.start()
