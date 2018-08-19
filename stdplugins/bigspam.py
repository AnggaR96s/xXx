# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import time


@borg.on(events.NewMessage(pattern=r"\.bigspam (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        counter, spam_text = input_str.split("|")
        shiiinabot = "\u2060"
        for i in range(4000):
            shiiinabot += "\u2060"
        message_text = shiiinabot + spam_text
        await event.edit(message_text)
        for i in range(int(counter)):
            time.sleep(0.3)
            await event.respond(message_text)
        await event.delete()
    else:
        await event.edit("send me a message in the format `.bigspam count | spam message` and admins won't see it in recent actions \n Courtesy: @shiiinabot")

