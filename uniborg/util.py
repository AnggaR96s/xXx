# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import math
import os
import time

from telethon import events
from telethon.tl.functions.messages import GetPeerDialogsRequest


def admin_cmd(pattern):
    return events.NewMessage(outgoing=True, pattern=re.compile(pattern))


async def is_read(borg, entity, message, is_out=None):
    """
    Returns True if the given message (or id) has been read
    if a id is given, is_out needs to be a bool
    """
    is_out = getattr(message, "out", is_out)
    if not isinstance(is_out, bool):
        raise ValueError(
            "Message was id but is_out not provided or not a bool")
    message_id = getattr(message, "id", message)
    if not isinstance(message_id, int):
        raise ValueError("Failed to extract id from message")

    dialog = (await borg(GetPeerDialogsRequest([entity]))).dialogs[0]
    max_id = dialog.read_outbox_max_id if is_out else dialog.read_inbox_max_id
    return message_id <= max_id


async def progress(current, total, event, start, type_of_ps):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress = "[{0}{1}] \nPercent: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}".format(
            humanbytes(current),
            humanbytes(total)
        )
        await event.edit("{}\n {}".format(
            type_of_ps,
            tmp
        ))


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]
