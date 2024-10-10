import vk_api
# import requests
from ..config_data.config import load_config


config = load_config()

vk_bot_token = config.vk_bot.token
vk_group_id = config.vk_bot.group_id

vk_session = vk_api.VkApi(token=vk_bot_token)

vk = vk_session.get_api()

post = vk.wall.get(owner_id=-223068460, count=3)

print(post)

# group_info = vk.wall.get(owner_id=-vk_group_id, count=1)

# post_id = group_info['items'][0]['id']

# print(group_info)
# print(group_info['items'][0]['text'])

# photo_response = requests.get(group_info['items'][0]['attachments'][0]['photo']['orig_photo']['url'])
# photo_filename = f"photos/photo_{post_id}.jpg"

# with open(photo_filename, 'wb') as photo_file:
#     photo_file.write(photo_response.content)
