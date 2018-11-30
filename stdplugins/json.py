from telethon import events
from telethon.errors import MessageTooLongError
import os


@borg.on(events.NewMessage(pattern=r"\.json", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    the_real_message = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
    else:
        the_real_message = event.stringify()
    if len(the_real_message) > Config.MAX_MESSAGE_SIZE_LIMIT:
        if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
        current_file_name = "{}file.json".format(Config.TMP_DOWNLOAD_DIRECTORY)
        file_ponter = open(current_file_name, "w+")
        file_ponter.write(the_real_message)
        file_ponter.close()
        await borg.send_file(
            event.chat_id,
            current_file_name,
            force_document=True,
            allow_cache=False,
            reply_to=event.message.id
        )
        await event.delete()
        os.remove(current_file_name)
    else:
        await event.edit(the_real_message)
