from telethon import events
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError
import os

MAX_MESSAGE_SIZE_LIMIT = 4095
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")


@borg.on(events.NewMessage(pattern=r"\.exec (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    input_command = input_str.split(" ")
    try:
        t_response = subprocess.check_output(input_command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        final_output = "**EXEC**: `{}` \nprocess returned {}\n output: {}".format(input_str, exc.returncode, exc.output)
    else:
        x_reponse = t_response.decode("UTF-8")
        final_output = "**EXEC**: `{}` \n\n**OUTPUT**: \n{} \n".format(input_str, x_reponse)
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        current_file_name = "{}exec.text".format(TEMP_DOWNLOAD_DIRECTORY)
        file_ponter = open(current_file_name, "w+")
        file_ponter.write(final_output)
        file_ponter.close()
        await borg.send_file(
            event.chat_id,
            current_file_name,
            force_document=True,
            allow_cache=False,
            caption=input_str,
            reply_to=event.message.id
        )
        await event.delete()
        os.remove(current_file_name)
    else:
        await event.edit(final_output)
