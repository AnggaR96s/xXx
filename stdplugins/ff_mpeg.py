"""FFMpeg for @UniBorg
"""
import asyncio
import io
import os
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from uniborg.util import admin_cmd, progress


logger.info(Config.FF_MPEG_DOWN_LOAD_MEDIA_PATH)
# https://t.me/RoseSupport/33801


@borg.on(admin_cmd("trim"))
async def magnet_download(event):
    if event.fwd_from:
        return
    if not os.path.exists(Config.FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await event.edit(f"a media file needs to be downloaded, and saved to the following path: `{Config.FF_MPEG_DOWN_LOAD_MEDIA_PATH}`")
        return
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    logger.info(cmt)
    start = datetime.now()
    if len(cmt) == 3:
        # output should be video
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            Config.FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time
        )
        logger.info(o)
        try:
            c_time = time.time()
            await borg.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                # reply_to=event.message.id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                )
            )
            os.remove(o)
        except Exception as e:
            logger.info(str(e))
    elif len(cmt) == 2:
        # output should be image
        cmd, start_time = cmt
        o = await take_screen_shot(
            Config.FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time
        )
        logger.info(o)
        try:
            c_time = time.time()
            await borg.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=True,
                # supports_streaming=True,
                allow_cache=False,
                # reply_to=event.message.id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                )
            )
            os.remove(o)
        except Exception as e:
            logger.info(str(e))
    else:
        await event.edit("RTFM")
        return
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit(f"Completed Process in {ms} seconds")


async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None

# https://github.com/Nekmo/telegram-upload/blob/master/telegram_upload/video.py#L26

async def cult_small_video(video_file, output_directory, start_time, end_time):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(round(time.time())) + ".mp4"
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None
