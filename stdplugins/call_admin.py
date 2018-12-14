from telethon import events

@borg.on(events.NewMessage(pattern=r"\.call\_admin", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("@admin")
