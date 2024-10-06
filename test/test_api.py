import vk_api
# import requests
from config_data.config import load_config


config = load_config()

vk_bot_token = config.vk_bot.token
vk_group_id = config.vk_bot.group_id

vk_session = vk_api.VkApi(token=vk_bot_token)

vk = vk_session.get_api()

post = vk.wall.get(owner_id=-223068460, count=10)

owner_id = post["items"][-1]["attachments"][0]["video"]["owner_id"]
video = post["items"][-1]["attachments"][0]["video"]["id"]
access_key = post["items"][-1]["attachments"][0]["video"]['access_key']

print(f'-223068460_{video}_{access_key}')

print(vk.video.get(videos=f'{owner_id}_{video}_{access_key}'))

# group_info = vk.wall.get(owner_id=-vk_group_id, count=1)

# post_id = group_info['items'][0]['id']

# print(group_info)
# print(group_info['items'][0]['text'])

# photo_response = requests.get(group_info['items'][0]['attachments'][0]['photo']['orig_photo']['url'])
# photo_filename = f"photos/photo_{post_id}.jpg"

# with open(photo_filename, 'wb') as photo_file:
#     photo_file.write(photo_response.content)
