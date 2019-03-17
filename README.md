# uniborg

Pluggable [``asyncio``](https://docs.python.org/3/library/asyncio.html)
[Telegram](https://telegram.org) userbot based on
[Telethon](https://github.com/LonamiWebs/Telethon).

## installing

#### The Legacy Way

Simply clone the repository and run the main file:
```sh
git clone https://github.com/uniborg/uniborg.git
cd uniborg
virtualenv -p /usr/bin/python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-stdborg.txt
# <Create config.py with variables available in sample_config.py>
python3 -m stdborg stdborg
```

An example `config.py` file could be:

```python3
from telethon.tl.types import ChatBannedRights

class Config(object):
  APP_ID = 6
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
  HU_STRING_SESSION = ""
  OPEN_WEATHER_MAP_APPID = ""
  SCREEN_SHOT_LAYER_ACCESS_KEY = ""
  # Send .get_id in any private group to fill this value.
  PRIVATE_GROUP_BOT_API_ID = -100
  # Send .get_id in any broadcast channel to fill this value.
  PRIVATE_CHANNEL_BOT_API_ID = -100
  TMP_DOWNLOAD_DIRECTORY = "./DOWNLOADS/"
  IBM_WATSON_CRED_USERNAME = ""
  IBM_WATSON_CRED_PASSWORD = ""
  HASH_TO_TORRENT_API = None
  TELEGRAPH_SHORT_NAME = "UniBorg"
  OCR_SPACE_API_KEY = ""
  G_BAN_LOGGER_GROUP = -100
  TG_GLOBAL_ALBUM_LIMIT = 3
  TG_BOT_TOKEN_BF_HER = ""
  TG_BOT_USER_NAME_BF_HER = ""
  MAX_MESSAGE_SIZE_LIMIT = 4095
  UB_BLACK_LIST_CHAT = []
  # maximum number of messages for antiflood
  MAX_ANTI_FLOOD_MESSAGES = 10
  # warn mode for anti flood
  ANTI_FLOOD_WARN_MODE = ChatBannedRights(
      until_date=None,
      view_messages=None,
      send_messages=True
  )
  # chat ids or usernames, it is recommended to use chat ids,
  # providing usernames means an additional overhead for the user
  CHATS_TO_MONITOR_FOR_ANTI_FLOOD = []
  # specify LOAD and NO_LOAD
  LOAD = []
  NO_LOAD = []
```

## internals

The core features offered by the custom `TelegramClient` live under the
[`uniborg/`](https://gitlab.com/SpEcHiDe/uniborg/tree/master/uniborg)
directory, with some utilities, enhancements and the `_core` plugin.
