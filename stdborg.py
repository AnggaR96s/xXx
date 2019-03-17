# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
from pathlib import Path
import sys
from uniborg import Uniborg
from uniborg.storage import Storage
from telethon.sessions import StringSession


logging.basicConfig(level=logging.INFO)

# the secret configuration specific things
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from sample_config import Config
else:
    if os.path.exists("config.py"):
        from config import Config
    else:
        logging.warning("No config.py Found!")
        logging.info("Please run the command, again, after creating config.py similar to README.md")
        sys.exit(1)


session_name = str(Config.HU_STRING_SESSION)
borg = Uniborg(
    StringSession(session_name),
    plugin_path="stdplugins",
    storage=lambda n: Storage(Path("data") / n),
    api_config=Config,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH
)
borg.run_until_disconnected()
