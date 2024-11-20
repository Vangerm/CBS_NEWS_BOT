from nats.js.client import JetStreamContext


async def vk_post_publisher(
        js: JetStreamContext,
        tg_group_id: int,
        post_text: str,
        post_attachments: list,
        subject: str
) -> None:
    headers = {
        'Tg-group-id': str(tg_group_id),
        'Tg-post-text': str(post_text),
        'Tg-post-attachments': ','.join(post_attachments),
    }
    await js.publish(subject=subject, headers=headers)
