# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import time


@borg.on(events.NewMessage(pattern=r".sd (.*) (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    counter = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    await event.edit(text)
    time.sleep(int(counter))
    await event.delete()
