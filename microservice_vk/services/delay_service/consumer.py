import json
import logging

import vk_api
from vk_api.bot_longpoll import (
    VkBotLongPoll,
    VkBotEventType
)

from microservice_vk.services.delay_service.publisher import vk_post_publisher

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

logger = logging.getLogger(__name__)


class VkLongPollConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            subject_consumer: str,
            subject_publisher: str,
            stream: str,
            durable_name: str
    ) -> None:
        self.nc = nc
        self.js = js
        self.subject_consumer = subject_consumer
        self.subject_publisher = subject_publisher
        self.stream = stream
        self.durable_name = durable_name

    # консьюмер ловящий данные групп вк и тг
    async def start(self) -> None:
        # нужно так же указывать deliver_policy
        # (all, last, new, by_start_sequence)
        self.stream_sub = await self.js.subscribe(
            subject=self.subject_consumer,
            stream=self.stream,
            cb=self.on_vk_longpoll,
            durable=self.durable_name,
            manual_ack=True
        )

    # метод опрашивающий группу вк о новых постах
    async def on_vk_longpoll(self, msg: Msg):
        payload = json.loads(msg.data)
        await msg.ack()

        try:
            vk_session = vk_api.VkApi(token=payload['vk_token'])
            vk_session.get_api()

            longpoll = VkBotLongPoll(vk_session, -int(payload['vk_group_id']))

            logger.info(f'Start check vk group - {payload["vk_group_id"]}')

            for event in longpoll.listen():
                if event.type == VkBotEventType.WALL_POST_NEW:
                    post_text = event.obj['text']
                    post_attachments = await self._get_url_attachments(
                                                event.obj['attachments'])
                    # паблищер передающий данные для публикации
                    await vk_post_publisher(
                                            self.js,
                                            payload['tg_group_id'],
                                            post_text,
                                            post_attachments,
                                            self.subject_publisher
                                            )
        except KeyboardInterrupt:
            logger.info('Stop check vk group')
        except Exception as e:
            logger.exception(e)

    # метод собирающий ссылки на фото с поста
    async def _get_url_attachments(self, attachments: list) -> list:
        urls = list()

        for attachment in attachments:
            if attachment['type'] == 'photo':
                url = attachment['photo']['orig_photo']['url']
                urls.append(url)
        return urls

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info('Consumer unsubscribe')
