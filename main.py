import vk_api
import time
import emoji 
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from skipper import checkSkip
from config import *
import logging
from telethon import TelegramClient, events, sync
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

vk = vk_api.VkApi(token=TOKEN_VK)

client = TelegramClient('AutoVinchik', API_ID, API_HASH)

BOT = 'leomatchbot'
BOT_ID = 1234060895
client.start()

def telegram():
    print("TG | ", end="")
    message = client.get_messages(BOT)[0].text.lower()
    if (checkSkip(message)):
        client.send_message(BOT, emoji.emojize(":thumbs_down:"))
        time.sleep(DELAY_TG)
    else:
        input("PRESS ENTER TO SKIP")
        client.send_message(BOT, emoji.emojize(":thumbs_down:"))

def vkontakte():
    print("VK | ", end="")
    message = vk.method("messages.getHistory", {"count": 1, "peer_id": -91050183})["items"][0]["text"].lower()
    if (checkSkip(message)):
        vk.method("messages.send", {"peer_id": -91050183, "message": "3", "random_id": get_random_id()})
        time.sleep(DELAY_VK)
    else:
        input("PRESS ENTER TO SKIP")
        vk.method("messages.send", {"peer_id": -91050183, "message": "3", "random_id": get_random_id()})

while True:
    telegram()
    vkontakte()
"""
vk = vk_api.VkApi(token=TOKEN_VK)

longpoll = VkLongPoll(vk)

print("START AUTOVINCHIK")
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
"""