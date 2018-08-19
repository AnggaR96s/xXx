# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import inspect
from telethon.errors import MessageEmptyError


@borg.on(events.NewMessage(pattern=r"\.eval (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    cmd = event.pattern_match.group(1)
    evaluation = None
    # https://t.me/telethonofftopic/43873
    try:
        if inspect.isawaitable(eval(cmd)):
            evaluation = await eval(cmd)
        # https://t.me/telethonofftopic/43873
        else:
            evaluation = eval(cmd)
    except ZeroDivisionError as e:
        evaluation = "ERROR: " + str(e)
    # https://t.me/telethonofftopic/43873
    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)
    await event.edit(final_output)


