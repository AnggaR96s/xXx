from telethon import events
import asyncio
from datetime import datetime
import os
import requests


download_directory = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./../DOWNLOADS/")


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@borg.on(events.NewMessage(pattern=r"\.paste ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                download_directory,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"
    url = "http://ix.io"
    files = {"f:1": message}
    r = requests.post(url, files=files)
    url = r.text.rstrip("\n") # the response has a newline for unknown reasons
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Pasted to {} in {} seconds".format(url, ms))

