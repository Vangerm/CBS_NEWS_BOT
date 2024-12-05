import json

from nats.js.client import JetStreamContext
from tenacity import retry


@retry
async def vk_post_publisher(
        js: JetStreamContext,
        tg_group_id: int,
        post_text: str,
        post_attachments: list,
        subject_publisher: str
) -> None:

    payload = json.dumps({
        'tg_group_id': str(tg_group_id),
        'post_text': post_text,
        'post_url_attachments': post_attachments,
    }).encode()

    await js.publish(subject=subject_publisher, payload=payload)
