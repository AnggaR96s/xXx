"""/admin Plugin for @UniBorg"""
from telethon import events
import asyncio

@borg.on(events.NewMessage(pattern=r"\/admin", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("@admin")
    await asyncio.sleep(5)
    await event.delete()
