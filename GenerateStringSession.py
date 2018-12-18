from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import Config

with TelegramClient(StringSession(), Config.APP_ID, Config.API_HASH) as client:
    print(client.session.save())
