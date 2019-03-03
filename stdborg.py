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
        logging.info("Please run the command, again.")
        sys.exit(1)


if len(sys.argv) == 2:
    session_name = str(sys.argv[1])
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
