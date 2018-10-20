from telethon import events
import asyncio
from datetime import datetime

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelBannedRights
from telethon.errors import ChatAdminRequiredError, UserIdInvalidError


@borg.on(events.NewMessage(pattern=r"\.ban ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = ChannelBannedRights(
        until_date=None,
        view_messages=True,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True
    )
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.sender_id
    elif input_str:
        to_ban_id = input_str
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (ChatAdminRequiredError, UserIdInvalidError) as exc:
        await event.edit(str(exc))
    else:
        await event.edit("Banned")
        await asyncio.sleep(5)
        await event.delete()
