import json
import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
                            URLInputFile,
                            InputMediaPhoto)

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

logger = logging.getLogger(__name__)


class VkPostConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            bot: Bot,
            subject_consumer: str,
            stream: str,
            durable_name: str
    ) -> None:
        self.nc = nc
        self.js = js
        self.bot = bot
        self.subject_consumer = subject_consumer
        self.stream = stream
        self.durable_name = durable_name

    async def start(self) -> None:
        # нужно так же указывать deliver_policy
        # (all, last, new, by_start_sequence)
        self.stream_sub = await self.js.subscribe(
            subject=self.subject_consumer,
            stream=self.stream,
            cb=self.on_vk_post,
            durable=self.durable_name,
            manual_ack=True
        )

    async def on_vk_post(self, msg: Msg):
        payload = json.loads(msg.data)
        await msg.ack()

        tg_group_id = payload['tg_group_id']
        post_text = payload['post_text']
        urls = payload['post_url_attachments']

        with suppress(TelegramBadRequest):
            if len(urls) == 1:
                await self.bot.send_photo(
                    tg_group_id,
                    URLInputFile(urls[0]),
                    caption=post_text
                )

            elif len(urls) > 1:
                photos: list = list()
                first_photo_caption = True

                for url in urls:
                    if first_photo_caption:
                        photos.append(InputMediaPhoto(
                            media=URLInputFile(url),
                            caption=post_text
                        ))
                        first_photo_caption = False
                    else:
                        photos.append(InputMediaPhoto(
                            media=URLInputFile(url)
                        ))

                await self.bot.send_media_group(
                    tg_group_id,
                    photos
                )

            else:
                await self.bot.send_message(
                    tg_group_id,
                    post_text
                )

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info('Consumer unsubscriber')
