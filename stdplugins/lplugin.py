from telethon import events
from uniborg import util
import asyncio
from datetime import datetime
import os


@borg.on(util.admin_cmd(r"^\.send plugin (?P<shortname>\w+)$"))
async def load_reload(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match["shortname"]
    the_plugin_file = "./stdplugins/{}.py".format(input_str)
    start = datetime.now()
    await borg.send_file(
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id
    )
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Uploaded {} in {} seconds".format(input_str, ms))


@borg.on(util.admin_cmd(r"\.install plugin"))
async def _(event):
    if event.fwd_from:
        return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await borg.download_media(
                await event.get_reply_message(),
                Config.TMP_DOWNLOAD_DIRECTORY
            )
            borg.load_plugin_from_file(downloaded_file_name)
            await event.edit("Installed Plugin `{}`".format(os.path.basename(downloaded_file_name)))
        except Exception as e:
            await event.edit(str(e))
    if os.path.exists(downloaded_file_name):
        os.remove(downloaded_file_name)


