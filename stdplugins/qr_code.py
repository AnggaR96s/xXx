"""Quick Response Codes
Available Commands
.getqr
.makeqr <long text to include>"""
from telethon import events
import asyncio
from datetime import datetime
import os
import requests
from uniborg.util import admin_cmd


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@borg.on(admin_cmd(pattern="getqr"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    downloaded_file_name = await borg.download_media(
        await event.get_reply_message(),
        Config.TMP_DOWNLOAD_DIRECTORY,
        progress_callback=progress
    )
    url = "https://api.qrserver.com/v1/read-qr-code/?outputformat=json"
    files = {"file": open(downloaded_file_name, "rb")}
    r = requests.post(url, files=files).json()
    qr_contents = r[0]["symbol"][0]["data"]
    os.remove(downloaded_file_name)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Obtained QRCode contents in {} seconds.\n{}".format(ms, qr_contents))
    await asyncio.sleep(5)
    await event.edit(qr_contents)


@borg.on(admin_cmd(pattern="makeqr ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.makeqr <long text to include>`"
    reply_msg_id = event.message.id
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
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
        message = "SYNTAX: `.makeqr <long text to include>`"
    url = "https://api.qrserver.com/v1/create-qr-code/?data={}&size=200x200&charset-source=UTF-8&charset-target=UTF-8&ecc=L&color=0-0-0&bgcolor=255-255-255&margin=1&qzone=0&format=jpg"
    r = requests.get(url.format(message), stream=True)
    required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + " " + str(datetime.now()) + ".webp"
    with open(required_file_name, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    await borg.send_file(
        event.chat_id,
        required_file_name,
        reply_to=reply_msg_id,
        progress_callback=progress
    )
    os.remove(required_file_name)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Created QRCode in {} seconds".format(ms))
    await asyncio.sleep(5)
    await event.delete()
