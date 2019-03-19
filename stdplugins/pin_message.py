from telethon import events, sync, errors
from telethon.tl import functions as f, types as t
import inspect
import os


@borg.on(events.NewMessage(pattern=r"\.cpin ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    silent = True
    input_str = event.pattern_match.group(1)
    if input_str:
        silent = False
    if event.message.reply_to_msg_id is not None:
        message_id = event.message.reply_to_msg_id
        try:
            await borg(f.messages.UpdatePinnedMessageRequest(event.chat_id, message_id, silent))
        except Exception as e:
            await event.edit(str(e))
        else:
            await event.delete()
    else:
        await event.edit("Reply to a message to pin the message in this Channel.")
