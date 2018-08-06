# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import os
import requests
from datetime import datetime

current_date_time = "./DOWNLOADS/"


@borg.on(events.NewMessage(pattern=r".download (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(current_date_time):
        os.makedirs(current_date_time)
    if event.reply_to_msg_id:
        start = datetime.now()
        downloaded_file_name = await borg.download_media(await event.get_reply_message(), current_date_time)
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to {} in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        url, file_name = input_str.split("|")
        r = requests.get(url, stream=True)
        await event.edit("Processing ...")
        required_file_name = current_date_time + "" + file_name
        start = datetime.now()
        with open(required_file_name, "wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to {} in {} seconds.".format(required_file_name, ms))
    else:
        await event.edit("Reply to a message to download to my local server.")

@borg.on(events.NewMessage(pattern=r".upload (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
