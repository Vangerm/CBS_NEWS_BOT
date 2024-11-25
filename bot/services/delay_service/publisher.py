import json

from nats.js.client import JetStreamContext


async def vk_post_publisher(
        js: JetStreamContext,
        tg_group_id: int,
        vk_group_id: int,
        vk_token: str,
        subject: str
) -> None:

    payload = json.dumps({
        'tg_group_id': str(tg_group_id),
        'vk_group_id': str(vk_group_id),
        'vk_token': vk_token,
    }).encode()

    await js.publish(subject=subject, payload=payload)
