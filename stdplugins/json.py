from telethon import events
from telethon.errors import MessageTooLongError
import os

MAX_MESSAGE_SIZE_LIMIT = 4095
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")


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
    if len(the_real_message) > MAX_MESSAGE_SIZE_LIMIT:
        current_file_name = "{}temp_file.text".format(TEMP_DOWNLOAD_DIRECTORY)
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
