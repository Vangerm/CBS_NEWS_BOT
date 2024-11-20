import json

from nats.js.client import JetStreamContext


async def vk_post_publisher(
        js: JetStreamContext,
        tg_group_id: int,
        post_text: str,
        post_attachments: list,
        subject: str
) -> None:
    headers = {
        "Content-Type": "application/json",
        "App-Name": "VkPosterApp",
    }

    payload = json.dumps({
        'tg_group_id': str(tg_group_id),
        'post_text': post_text,
        'post_url_attachments': post_attachments,
    }).encode()

    await js.publish(subject=subject, payload=payload, headers=headers)
