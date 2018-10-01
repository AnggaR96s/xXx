from telethon import events

@borg.on(events.NewMessage(pattern=r".helpme", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("UserBot Forked from https://github.com/uniborg/uniborg")
