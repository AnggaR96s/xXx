# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
from telethon.tl.functions.messages import GetInlineBotResultsRequest
from telethon.tl.functions.messages import SendInlineBotResultRequest


@borg.on(events.NewMessage(pattern=".SaavnDL search (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("processing...")
    str = event.pattern_match.group(1)
    search_responses = await borg(GetInlineBotResultsRequest(
        "@SaavnDLBot", event.chat_id, str, ""
    ))
    if len(search_responses.results) > 0:
        await event.edit("{} results found for {} query".format(len(search_responses.results), str))
    else:
        await event.edit("No result found for **" + str + "**")
