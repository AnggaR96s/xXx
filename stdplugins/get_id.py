# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events


@borg.on(events.NewMessage(pattern=r".get_id", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    chat = await event.get_input_chat()
    await event.edit("-100" + str(chat.channel_id))
