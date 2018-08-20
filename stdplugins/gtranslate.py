# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
from datetime import datetime
from googletrans import Translator


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
    translated_text = translator.translate(text, lan).text
    end = datetime.now()
    ms = (end - start).seconds
    output_str = "Translated to {} in {} seconds. \n {}".format(lan, str(ms), translated_text)
    await event.edit(output_str)
