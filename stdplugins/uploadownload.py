# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import os
import requests

@borg.on(events.NewMessage(pattern=r".download", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    current_date_time = "./DOWNLOADS/"
    if not os.path.isdir(current_date_time):
        os.makedirs(current_date_time)
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        required_message = await borg.get_messages(event.chat_id, limit=1, max_id=message_id+1, min_id=message_id-1)
        downloaded_file_name = await borg.download_media(required_message, current_date_time)
        await event.edit("Downloaded to {}.".format(downloaded_file_name))
    else:
        await event.edit("Reply to a message to download to my local server.")
