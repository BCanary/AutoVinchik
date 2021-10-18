from telethon import TelegramClient, events
import time
import emoji 
import logging
from skipper import checkSkip
from config import *
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

client = TelegramClient('FastRedactor', API_ID, API_HASH)

BOT = 'leomatchbot'

@client.on(events.NewMessage(chats=BOT, incoming=True))
async def handler(event):
    if (checkSkip(event.raw_text)):
        await client.send_message(BOT, emoji.emojize(":thumbs_down:"))
        time.sleep(DELAY_TG)
    else:
        input("PRESS ENTER TO SKIP")
        await client.send_message(BOT, emoji.emojize(":thumbs_down:"))

client.start()

async def main():
    await client.send_message(BOT, emoji.emojize(":thumbs_down:"))
print("START TG AUTOVINCHIK")
input("PRESS ENTER TO START")
with client:
    client.loop.run_until_complete(main())

client.start()
client.run_until_disconnected()