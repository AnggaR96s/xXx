# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from uniborg import Uniborg

logging.basicConfig(level=logging.INFO)

import os
import sys

if "APP_ID" not in os.environ and "API_HASH" not in os.environ:
    print("Please fill in the required values from app.json "
          "Do not steal the values from the official application. "
          "Doing that WILL backfire on you. \nBot quitting.", file=sys.stderr)
    quit(1)


if len(sys.argv) == 2:
    api_id = int(os.environ.get("APP_ID"))
    api_hash = os.environ.get("API_HASH")
    borg = Uniborg(
        str(sys.argv[1]),
        plugin_path="stdplugins",
        connection_retries=None,
        api_id=api_id,
        api_hash=api_hash
    )
    borg.run_until_disconnected()
else:
    print("USAGE EXAMPLE:\n"
          "python3 -m stdborg <SESSION_NAME>"
          "\n 👆👆Please follow the above format to run your userbot. \nBot quitting.", file=sys.stderr)

