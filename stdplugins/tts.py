# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import requests
import os
from datetime import datetime
from gtts import gTTS


current_date_time = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./../DOWNLOADS/")


@borg.on(events.NewMessage(pattern=r".tts (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    else:
        lan, text = input_str.split("|")
    required_file_name = current_date_time + "voice.ogg"
    try:
        tts = gTTS(text, lan)
        tts.save(required_file_name)
    except AssertionError as e:
        await event.edit(str(e))
    end = datetime.now()
    ms = (end - start).seconds
    await borg.send_file(
        event.chat_id,
        required_file_name,
        caption="Processed {} ({}) in {} seconds!".format(text[0:97], lan, ms),
        reply_to=event.message.reply_to_msg_id,
        allow_cache=False,
        voice_note=True
    )
    os.remove(required_file_name)
    await event.delete()

