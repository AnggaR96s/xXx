from telethon import events
import asyncio


@borg.on(events.NewMessage(pattern=r"^(.*)chat\.whatsapp\.com\/(.*)", incoming=True))
async def _(event):
    if event.message.is_private:
        return
    print(event.stringify())
    try:
        print(await borg.delete_messages(event.chat_id, event.message))
    except e:
        logger.error(e)
        b = await event.respond("@admin, **DETECTED** @WhatsCRApp Link.")
        await asyncio.sleep(5)
        await b.delete()

