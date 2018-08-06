# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
from datetime import datetime

@borg.on(events.NewMessage(pattern=r".ping", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit('Pong!')
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit('Pong!\n%sms' % (ms))
