from telethon import events
import asyncio


@borg.on(events.NewMessage(pattern=r"\!\!gban ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        await borg.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "!gban [user](tg://user?id={}) {}".format(r.from_id, reason)
        )
    await event.delete()


@borg.on(events.NewMessage(pattern=r"\!\!ungban ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        await borg.send_message(
            Config.G_BAN_LOGGER_GROUP,
            "!ungban [user](tg://user?id={}) {}".format(r.from_id, reason)
        )
    await event.delete()
