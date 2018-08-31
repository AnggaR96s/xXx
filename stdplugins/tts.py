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
        command_to_execute = "ffmpeg -i {} -map 0:a -codec:a libopus -b:a 100k -vbr on {}".format(required_file_name, required_file_name + ".opus")
        os.system(command_to_execute)
        end = datetime.now()
        ms = (end - start).seconds
        await borg.send_file(
            event.chat_id,
            required_file_name + ".opus",
            # caption="Processed {} ({}) in {} seconds!".format(text[0:97], lan, ms),
            reply_to=event.message.reply_to_msg_id,
            allow_cache=False,
            voice_note=True
        )
        os.remove(required_file_name)
        os.remove(required_file_name + ".opus")
        await event.delete()
    except AssertionError as e:
        await event.edit(str(e))

