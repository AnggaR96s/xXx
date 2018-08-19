# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import time


@borg.on(events.NewMessage(pattern=".purge", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    i = 1
    msgs = []
    shiiinabot = "\u2060"
    for i in range(4000):
        shiiinabot += "\u2060"
    await event.edit(shiiinabot)
    await event.delete()
    async for message in borg.iter_messages(event.chat_id, min_id=event.reply_to_msg_id, from_user="me"):
        i = i + 1
        try:
            await message.edit(shiiinabot + message.message)
        except:
            pass
        msgs.append(message)
        time.sleep(3)
    if len(msgs) <= 100:
        await borg.delete_messages(event.chat_id, msgs)
        msgs = []
