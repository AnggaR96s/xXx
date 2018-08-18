# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelBannedRights
from datetime import datetime, timedelta
from telethon.errors import UserAdminInvalidError

@borg.on(events.NewMessage(pattern=".kickdas", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Getting Participant Lists. This might take some time ...")
    p = await borg.get_participants(event.chat_id, aggressive=True)
    await event.edit("Searching through {} users for deleted accounts ...".format(len(p)))
    c = 0
    d = 0
    e = []
    for i in p:
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChannelBannedRights(
            until_date=None,
            view_messages=True
        )
        if i.deleted:
            d = d + 1
            try:
                await borg(EditBannedRequest(event.chat_id, i, rights))
                c = c + 1
            except UserAdminInvalidError as exc:
                await event.edit("I need admin priveleges to perform this action!")
                break
            except:
                e.append("ERROR")
    await event.edit("Found {} Deleted Accounts. Kicked {} / {} users".format(d, c, len(p)))
