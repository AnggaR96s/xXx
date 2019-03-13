from telethon import events
import asyncio
import json
import os
import requests
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import MessageNotModifiedError

import time
from uniborg.util import progress


@borg.on(events.NewMessage(pattern=r"\.download ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        downloaded_file_name = await borg.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, time.time(), "trying to download")
            )
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    else:
        await event.edit("Reply to a message to download to my local server.")
