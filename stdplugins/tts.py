# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import requests
import os
from datetime import datetime

current_date_time = "./../DOWNLOADS/"


@borg.on(events.NewMessage(pattern=r".tts (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    tts_url = "https://tts.baidu.com/text2audio?lan={}&ie=UTF-8&text={}"
    lan, text = input_str.split("|")
    input_url = tts_url.format(lan.strip(), text.strip())
    response = requests.get(input_url, stream=True)
    required_file_name = current_date_time + "voice.ogg"
    with open(required_file_name, "wb") as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)
    await borg.send_file(
        event.chat_id,
        required_file_name,
        reply_to=event.message.id,
        allow_cache=False,
        voice_note=True
    )
    os.remove(required_file_name)
    end = datetime.now()
    ms = (end - start).seconds
    output_str = "Processed {} ({}) in {} seconds!"
    await event.edit(output_str.format(text, lan, ms))

