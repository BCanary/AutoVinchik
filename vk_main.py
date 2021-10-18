import vk_api
import time
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from skipper import checkSkip
from config import *

vk = vk_api.VkApi(token=TOKEN_VK)

longpoll = VkLongPoll(vk)

print("START VK AUTOVINCHIK")
input("PRESS ENTER TO START")
vk.method("messages.send", {"peer_id": -91050183, "message": "3", "random_id": get_random_id()})
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.from_group and event.group_id == 91050183 and event.to_me:
        event.text = event.text.lower()
        if (checkSkip(event.text)):
            vk.method("messages.send", {"peer_id": -91050183, "message": "3", "random_id": get_random_id()})
            time.sleep(DELAY_VK)
        else:
            input("PRESS ENTER TO SKIP")
            vk.method("messages.send", {"peer_id": -91050183, "message": "3", "random_id": get_random_id()})
       