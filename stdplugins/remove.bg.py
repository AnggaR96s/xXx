# (c) Shrimadhav U K
#
# This file is part of @UniBorg
#
# @UniBorg is free software; you cannot redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# @UniBorg is not distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# This file is part of @UniBorg
from datetime import datetime
import requests
from telethon import events
import time
from uniborg.util import progress


@borg.on(events.NewMessage(pattern=r"\.remove\.bg ?(.*)", outgoing=True))
async def _(event):
    HELP_STR = "`.remove.bg` as reply to a media, or give a link as an argument to this command"
    output_file_name = Config.TMP_DOWNLOAD_DIRECTORY + "/@uniBorg_ReMove.png"
    if event.fwd_from:
        return
    if Config.REM_BG_API_KEY is None:
        await event.edit("You need API token from remove.bg to use this plugin.")
        return False
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to download")
                )
            )
        except Exception as e:
            await event.edit(str(e))
        else:
            output_file_name = ReTrieveFile(downloaded_file_name, output_file_name)
            os.remove(downloaded_file_name)
            await borg.send_file(
                event.chat_id,
                output_file_name,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id
            )
            os.remove(output_file_name)
            end = datetime.now()
            ms = (end - start).seconds
            await event.edit("Background Removed in {} seconds using ReMove.BG API, powered by @UniBorg".format(ms))
    elif input_str:
        # check if starts with http
        if input_str.startswith("http"):
            output_file_name = ReTrieveURL(input_str, output_file_name)
            await borg.send_file(
                event.chat_id,
                output_file_name,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id
            )
            os.remove(output_file_name)
            end = datetime.now()
            ms = (end - start).seconds
            await event.edit("Background Removed in {} seconds using ReMove.BG API, powered by @UniBorg".format(ms))
        else:
            await event.edit(HELP_STR)
    else:
        await event.edit(HELP_STR)


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name, output_file_name):
    if os.path.exists(output_file_name):
        os.remove(output_file_name)
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True
    )
    with open(output_file_name, "wb") as fd:
        for chunk in r.iter_content(chunk_size=10214):
            fd.write(chunk)
    return output_file_name


def ReTrieveURL(input_url, output_file_name):
    if os.path.exists(output_file_name):
        os.remove(output_file_name)
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    data = {
      "image_url": input_url
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True
    )
    with open(output_file_name, "wb") as fd:
        for chunk in r.iter_content(chunk_size=10214):
            fd.write(chunk)
    return output_file_name
