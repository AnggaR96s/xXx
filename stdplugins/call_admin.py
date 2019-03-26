""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins


@borg.on(events.NewMessage(pattern=r"\@admin", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "admin"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await event.edit(mentions)
