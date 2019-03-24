"""Purge your messages without the admins seeing it in Recent Actions"""
from telethon import events
import asyncio


@borg.on(events.NewMessage(pattern="\.purge ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        shiiinabot = "\u2060"
        for i in range(601):
            shiiinabot += "\u2060"
        try:
            await event.edit(shiiinabot)
        except Exception as e:
            logger.warn(str(e))
            pass
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await borg.get_entity(input_str)
            logger.info(from_user)
        async for message in borg.iter_messages(event.chat_id, min_id=event.reply_to_msg_id, from_user=from_user):
            i = i + 1
            msgs.append(message)
            if len(msgs) == 100:
                await borg.delete_messages(event.chat_id, msgs)
                msgs = []
        if len(msgs) <= 100:
            await borg.delete_messages(event.chat_id, msgs)
            msgs = []
            await event.delete()
        else:
            await event.edit("**PURGE** Failed!")
