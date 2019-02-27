# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from uniborg import Uniborg

logging.basicConfig(level=logging.INFO)

import os
import sys

# the secret configuration specific things
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from sample_config import Config
else:
    if os.path.exists("config.py"):
        from config import Config
    else:
        logging.warn("No config.py Found!")
        APP_ID = int(input("Login to my.telegram.org and Paste your APP ID here "))
        API_HASH = input("Login to my.telegram.org and Paste your API HASH here ")
        TMP_DOWNLOAD_DIRECTORY = "./DOWNLOADS/"
        HASH_TO_TORRENT_API = None
        TELEGRAPH_SHORT_NAME = input("Enter the name that you would like to be shown when creating @telegraph articles using this UserBot: ")
        IBM_WATSON_CRED_USERNAME = input("Paste IBM_WATSON_CRED_USERNAME here: ")
        IBM_WATSON_CRED_PASSWORD = input("Paste IBM_WATSON_CRED_PASSWORD here: ")
        SCREEN_SHOT_LAYER_ACCESS_KEY = input("Get an access key from http://api.screenshotlayer.com/api/capture ")
        OPEN_WEATHER_MAP_APPID = input("Get an access key from https://api.openweathermap.org/data/2.5/weather ")
        PRIVATE_GROUP_BOT_API_ID = -100
        PRIVATE_CHANNEL_BOT_API_ID = -100
        MAX_MESSAGE_SIZE_LIMIT = 4095
        TG_GLOBAL_ALBUM_LIMIT = int(input("Number of images you want to #spam in the Google Image search: "))
        OCR_SPACE_API_KEY = input("Get your free API Key from OCR.Space ")
        UB_BLACK_LIST_CHAT = list(map(str, input("Some groups do not like userbots, (Like Official Telegram Groups). Please provide list of usernames where you want to disable userbot's incoming=True feature. (seperated by SPACE) ").split()))
        CHATS_TO_MONITOR_FOR_ANTI_FLOOD = list(map(str, input("Please provide list of usernames where you want to enable userbot's antiflood feature. (seperated by SPACE) ").split()))\
        MAX_ANTI_FLOOD_MESSAGES = input("Number of consecutive messages to be considered as FLOOD ")
        with open("config.py", "w") as f:
            f.write(f"""from telethon.tl.types import ChatBannedRights
class Config(object):
    APP_ID = {APP_ID}
    API_HASH = "{API_HASH}"
    TMP_DOWNLOAD_DIRECTORY = "{TMP_DOWNLOAD_DIRECTORY}"
    HASH_TO_TORRENT_API = "{HASH_TO_TORRENT_API}"
    TELEGRAPH_SHORT_NAME = "{TELEGRAPH_SHORT_NAME}"
    IBM_WATSON_CRED_USERNAME = "{IBM_WATSON_CRED_USERNAME}"
    IBM_WATSON_CRED_PASSWORD = "{IBM_WATSON_CRED_PASSWORD}"
    SCREEN_SHOT_LAYER_ACCESS_KEY = "{SCREEN_SHOT_LAYER_ACCESS_KEY}"
    OPEN_WEATHER_MAP_APPID = "{OPEN_WEATHER_MAP_APPID}"
    # Send .get_id in any private group to fill this value.
    PRIVATE_GROUP_BOT_API_ID = {PRIVATE_GROUP_BOT_API_ID}
    # Send .get_id in any broadcast channel to fill this value.
    PRIVATE_CHANNEL_BOT_API_ID = {PRIVATE_CHANNEL_BOT_API_ID}
    MAX_MESSAGE_SIZE_LIMIT = {MAX_MESSAGE_SIZE_LIMIT}
    TG_GLOBAL_ALBUM_LIMIT = {TG_GLOBAL_ALBUM_LIMIT}
    OCR_SPACE_API_KEY = "{OCR_SPACE_API_KEY}"
    UB_BLACK_LIST_CHAT = {UB_BLACK_LIST_CHAT}
    MAX_ANTI_FLOOD_MESSAGES = {MAX_ANTI_FLOOD_MESSAGES}
    # warn mode for anti flood
    ANTI_FLOOD_WARN_MODE = ChatBannedRights(
        until_date=None,
        view_messages=None,
        send_messages=True
    )
    # chat ids or usernames, it is recommended to use chat ids,
    # providing usernames means an additional overhead for the user
    CHATS_TO_MONITOR_FOR_ANTI_FLOOD = {CHATS_TO_MONITOR_FOR_ANTI_FLOOD}""")
        logging.info("Please run the command, again.")
        sys.exit(1)


if len(sys.argv) == 2:
    session_name = str(sys.argv[1])
    if session_name == "test":
        logging.info("Ran Successfully")
    else:
        borg = Uniborg(
            session_name,
            plugin_path="stdplugins",
            connection_retries=None,
            api_config=Config,
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH
        )
        borg.run_until_disconnected()
else:
    logging.error("USAGE EXAMPLE:\n"
          "python3 -m stdborg <SESSION_NAME>"
          "\n 👆👆Please follow the above format to run your userbot. \nBot quitting.", )
