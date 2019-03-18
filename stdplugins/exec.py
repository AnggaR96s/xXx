from telethon import events
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import asyncio
import time


@borg.on(events.NewMessage(pattern=r"\.exec ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
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
            with io.BytesIO(str.encode(OUTPUT)) as out_file:
                out_file.name = "exec.text"
                await borg.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=cmd,
                    reply_to=reply_to_id
                )
                await event.delete()
                break
        else:
            try:
                await asyncio.sleep(DELAY_BETWEEN_EDITS)
                await event.edit(OUTPUT)
                await asyncio.sleep(DELAY_BETWEEN_EDITS)
            except (Exception) as e:
                logger.warn(str(e))
                if "seconds" in str(e):
                    break
                else:
                    pass

