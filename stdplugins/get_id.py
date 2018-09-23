from telethon import events
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
from telethon.utils import pack_bot_file_id


@borg.on(events.NewMessage(pattern=r".get_id", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            print(r_msg.media)
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await event.edit("The BOT API file ID of this media is `{}`!".format(str(bot_api_file_id)))
        else:
            chat = await event.get_input_chat()
            await event.edit("The current chat's ID is `{}`!".format(str(event.chat_id)))
    else:
        chat = await event.get_input_chat()
        await event.edit("The current chat's ID is `{}`!".format(str(event.chat_id)))


