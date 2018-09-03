# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import time


@borg.on(events.NewMessage(pattern=".purgeme", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    i = 1
    shiiinabot = "\u2060"
    for i in range(4006):
        shiiinabot += "\u2060"
    await event.edit(shiiinabot)
    await event.delete()
    async for message in borg.iter_messages(event.chat_id, from_user="me"):
        i = i + 1
        try:
            #  await message.edit(shiiinabot)
            await message.delete()
        except:
            pass
        time.sleep(10)
