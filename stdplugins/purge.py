from telethon import events
import asyncio


@borg.on(events.NewMessage(pattern="\.purge", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        shiiinabot = "\u2060"
        for i in range(4000):
            shiiinabot += "\u2060"
        await event.edit(shiiinabot)
        async for message in borg.iter_messages(event.chat_id, min_id=event.reply_to_msg_id):
            i = i + 1
            msgs.append(message)
        if len(msgs) <= 100:
            await borg.delete_messages(event.chat_id, msgs)
            msgs = []
            await event.delete()
        else:
            await event.edit("**PURGE** Failed!")
