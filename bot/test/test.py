import vk_api
from config import load_config
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def main():
    config = load_config()

    group_id = config.vk_bot.group_id

    vk_session = vk_api.VkApi(token=config.vk_bot.token)

    vk = vk_session.get_api()

    # response = vk.groups.getLongPollServer(group_id=-group_id)

    # longpoll = vk.groups.getLongPollSettings(group_id=-group_id)

    longpoll = VkBotLongPoll(vk_session, -group_id)

    for event in longpoll.listen():
        # if event.type() == VkEventType.WALL_POST_NEW:
        print(event.obj['attachments'])

    # post_id = 0

    # vk_post_info = vk.wall.get(owner_id=group_id, count=2)
    # is_pinned = 0

    # if vk_post_info['items'][0].get('is_pinned', 0):
    #     is_pinned = 1

    # vk_post = vk_post_info['items'][is_pinned]

    # if vk_post['id'] != post_id:
    #     post_id = vk_post['id']
    #     print(f'{vk_post['id']} - {vk_post['text']}')


main()
