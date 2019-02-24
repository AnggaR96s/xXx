from telethon import events
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import os
import asyncio
import time


@borg.on(events.NewMessage(pattern=r"\.exec (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**Output:**\n"
    while process:
        if time.time() > start_time:
            if process:
                process.kill()
            await event.edit(f"{OUTPUT}\n__Process killed__: `Time limit reached`")
            break
        stdout = await process.stdout.readline()
        if not stdout:
            _, stderr = await process.communicate()
            if stderr.decode():
                OUTPUT += f"`{stderr.decode()}`"
                await event.edit(OUTPUT)
                await asyncio.sleep(DELAY_BETWEEN_EDITS)
                break
        else:
            OUTPUT += f"`{stdout.decode()}`"
        if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
            if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
                os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
            current_file_name = "{}exec.text".format(Config.TMP_DOWNLOAD_DIRECTORY)
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
            break
        else:
            try:
                await asyncio.sleep(DELAY_BETWEEN_EDITS)
                await event.edit(OUTPUT)
                await asyncio.sleep(DELAY_BETWEEN_EDITS)
            except (Exception) as e:
                logger.warn(str(e))
                break

