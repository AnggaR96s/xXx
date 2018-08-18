# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events


@borg.on(events.NewMessage(pattern=".purgeme", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    i = 1
    async for message in borg.iter_messages(event.chat_id, from_user="me"):
        i = i + 1
        await message.delete()
    await event.delete()
