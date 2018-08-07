# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events


@borg.on(events.NewMessage(pattern=r"\.json", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        await event.edit(previous_message.stringify())
    else:
        await event.edit(event.stringify())
