from telethon import events
from datetime import datetime
from googletrans import Translator
import json


@borg.on(events.NewMessage(pattern=r".tr (.*)", outgoing=True))
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
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        src_lang = translated.src
        translated_text = translated.text
        end = datetime.now()
        ms = (end - start).seconds
        output_str = "Translated from {} to {} in {} seconds. \n {}".format(src_lang, lan, str(ms), translated_text)
        await event.edit(output_str)
    except json.decoder.JSONDecodeError as exc:
        await event.edit(str(exc))

