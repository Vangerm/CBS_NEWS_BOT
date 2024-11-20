import json
import logging

import vk_api
from vk_api.bot_longpoll import (
    VkBotLongPoll,
    VkBotEventType
)

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

logger = logging.getLogger(__name__)


class VkLongPollConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            subject: str,
            stream: str,
            durable_name: str
    ) -> None:
        self.nc = nc
        self.js = js
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name

    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_vk_longpoll,
            durable=self.durable_name,
            manual_ack=True
        )

    async def on_vk_longpoll(self, msg: Msg):
        payload = json.loads(msg.data)

        try:
            vk_session = vk_api.VkApi(token=payload['vk_token'])
            vk_session.get_api()

            longpoll = VkBotLongPoll(vk_session, -payload['vk_group_id'])

            logger.info(f'Start check vk group - {payload["vk_group_id"]}')

            for event in longpoll.listen():
                if event.type == VkBotEventType.WALL_POST_NEW:
                    pass
        except Exception as e:
            logger.exception(e)

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info('Consumer unsubscribe')
