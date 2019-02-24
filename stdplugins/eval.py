# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events, sync, errors, functions, types
import inspect
import os


@borg.on(events.NewMessage(pattern=r"\.eval (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    cmd = event.pattern_match.group(1)
    evaluation = None
    # https://t.me/telethonofftopic/43873
    try:
        if inspect.isawaitable(eval(cmd)):
            evaluation = await eval(cmd)
        # https://t.me/telethonofftopic/43873
        else:
            evaluation = eval(cmd)
    except (ZeroDivisionError, ValueError, SyntaxError, AttributeError, NameError, TypeError, Exception) as e:
        evaluation = str(e)
    # https://t.me/telethonofftopic/43873
    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)
    if len(final_output) > Config.MAX_MESSAGE_SIZE_LIMIT:
        if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
        current_file_name = "{}eval.text".format(Config.TMP_DOWNLOAD_DIRECTORY)
        file_ponter = open(current_file_name, "w+")
        file_ponter.write(final_output)
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
        await event.edit(final_output)
