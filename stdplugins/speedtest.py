from telethon import events
from datetime import datetime
import io
import speedtest


@borg.on(events.NewMessage(pattern=r"\.speedtest", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Calculating my internet speed. Please wait!")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:
        response = s.results.share()
        speedtest_image = response
        await borg.send_file(
            event.chat_id,
            speedtest_image,
            caption="**SpeedTest** completed in {} seconds".format(ms),
            reply_to=reply_msg_id
        )
        await event.delete()
    except Exception as exc:
        await event.edit("""**SpeedTest** completed in {} seconds
Download: {}
Upload: {}
Ping: {}

__With the Following ERRORs__
{}""".format(ms, convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, str(exc)))


def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {
        0: "",
        1: "kilobytes",
        2: "megabytes",
        3: "gigabytes",
        4: "terabytes"
    }
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"

