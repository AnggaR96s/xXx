# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import os
import traceback
from uniborg import util
from datetime import datetime


DELETE_TIMEOUT = 5


@borg.on(util.admin_cmd(r"^\.load (?P<shortname>\w+)$"))
async def load_reload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        if shortname in borg._plugins:
            borg.remove_plugin(shortname)
        borg.load_plugin(shortname)
        msg = await event.respond(f"Successfully (re)loaded plugin {shortname}")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:
        tb = traceback.format_exc()
        logger.warn(f"Failed to (re)load plugin {shortname}: {tb}")
        await event.respond(f"Failed to (re)load plugin {shortname}: {e}")


@borg.on(util.admin_cmd(r"^\.(?:unload|remove) (?P<shortname>\w+)$"))
async def remove(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.respond(f"Not removing {shortname}")
    elif shortname in borg._plugins:
        borg.remove_plugin(shortname)
        msg = await event.respond(f"Removed plugin {shortname}")
    else:
        msg = await event.respond(f"Plugin {shortname} is not loaded")
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()


@borg.on(util.admin_cmd(r"^\.send plugin (.*)"))
async def send_plug_in(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./stdplugins/{}.py".format(input_str)
    start = datetime.now()
    await borg.send_file(
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        reply_to=message_id
    )
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Uploaded {} in {} seconds".format(input_str, ms))
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


@borg.on(util.admin_cmd(r"\.install plugin"))
async def install_plug_in(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await borg.download_media(
                await event.get_reply_message(),
                borg._plugin_path
            )
            borg.load_plugin_from_file(downloaded_file_name)
            await event.edit("Installed Plugin `{}`".format(os.path.basename(downloaded_file_name)))
        except Exception as e:
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()
