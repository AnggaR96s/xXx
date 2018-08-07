# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import subprocess

@borg.on(events.NewMessage(pattern=r"\.exec (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    input_command = input_str.split(" ")
    try:
        t_response = subprocess.check_output(input_command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        await event.edit("Status : FAIL", exc.returncode, exc.output)
    else:
        x_reponse = t_response.decode("UTF-8")
        await event.edit(x_reponse)
