# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import os
import requests
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import MessageNotModifiedError

current_date_time = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./../DOWNLOADS/")


@borg.on(events.NewMessage(pattern=r".download (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(current_date_time):
        os.makedirs(current_date_time)
    if event.reply_to_msg_id:
        start = datetime.now()
        downloaded_file_name = await borg.download_media(
            await event.get_reply_message(),
            current_date_time
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        url, file_name = input_str.split("|")
        url = url.strip()
        # https://stackoverflow.com/a/761825/4723940
        file_name = file_name.strip()
        required_file_name = current_date_time + "" + file_name
        start = datetime.now()
        r = requests.get(url, stream=True)
        with open(required_file_name, "wb") as fd:
            total_length = r.headers.get('content-length')
            # https://stackoverflow.com/a/15645088/4723940
            if total_length is None: # no content length header
                fd.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for chunk in r.iter_content(chunk_size=128):
                    dl += len(chunk)
                    fd.write(chunk)
                    done = int(100 * dl / total_length)
                    download_progress_string = "Downloading ... [%s%s]" % ('=' * done, ' ' * (50-done))
                    # download_progress_string = "Downloading ... [%s of %s]" % (str(dl), str(total_length))
                    # download_progress_string = "Downloading ... [%s%s]" % ('⬛️' * done, '⬜️' * (100 - done))
                    """try:
                        await event.edit(download_progress_string)
                    except MessageNotModifiedError as e:
                        logger.warn("__FLOODWAIT__: {} sleeping for 100seconds, before proceeding.".format(str(e)))
                    time.sleep(1)"""
                    logger.info(download_progress_string)
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(required_file_name, ms))
    else:
        await event.edit("Reply to a message to download to my local server.")


@borg.on(events.NewMessage(pattern=r".upload (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    if os.path.exists(input_str):
        start = datetime.now()
        await borg.send_file(
            event.chat_id,
            input_str,
            force_document=True,
            allow_cache=False,
            reply_to=event.message.id
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Uploaded in {} seconds.".format(ms))
    else:
        await event.edit("404: File Not Found")


@borg.on(events.NewMessage(pattern=r".uploadas(stream|vn) (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    type_of_upload = event.pattern_match.group(1)
    supports_streaming = False
    round_message = False
    if type_of_upload == "stream":
        supports_streaming = True
    if type_of_upload == "vn":
        round_message = True
    input_str = event.pattern_match.group(2)
    if os.path.exists(input_str):
        start = datetime.now()
        metadata = extractMetadata(createParser(input_str))
        if supports_streaming:
            await borg.send_file(
                event.chat_id,
                input_str,
                caption=input_str,
                force_document=False,
                allow_cache=False,
                reply_to=event.message.id,
                attributes=[
                    DocumentAttributeVideo(
                        duration=metadata.get("duration").seconds,
                        w=metadata.get("width"),
                        h=metadata.get("height"),
                        round_message=False,
                        supports_streaming=True
                    )
                ]
            )
        if round_message:
            await borg.send_file(
                event.chat_id,
                input_str,
                allow_cache=False,
                reply_to=event.message.id,
                video_note=True,
                attributes=[
                    DocumentAttributeVideo(
                        duration=0,
                        w=1,
                        h=1,
                        round_message=True,
                        supports_streaming=True
                    )
                ]
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Uploaded in {} seconds.".format(ms))
    else:
        await event.edit("404: File Not Found")
