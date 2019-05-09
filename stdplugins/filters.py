# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Filters
Available Commands:
.savefilter
.listfilters
.clearfilter"""
import asyncio
import re
from telethon import events, utils
from telethon.tl import types
from sql_helpers.filters_sql import get_filter, add_filter, remove_filter, get_all_filters, remove_all_filters
from uniborg.util import admin_cmd


DELETE_TIMEOUT = 10
TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


borg.storage.last_triggered_filters = {}  # pylint:disable=E0602


@borg.on(events.NewMessage(incoming=True))
async def on_snip(event):
    name = event.raw_text
    if event.chat_id in borg.storage.last_triggered_filters:
        if name in borg.storage.last_triggered_filters[event.chat_id]:
            # avoid userbot spam
            # "I demand rights for us bots, we are equal to you humans." -Henri Koivuneva (t.me/UserbotTesting/2698)
            return False
    snips = get_all_filters(event.chat_id)
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                if snip.snip_type == TYPE_PHOTO:
                    media = types.InputPhoto(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference
                    )
                elif snip.snip_type == TYPE_DOCUMENT:
                    media = types.InputDocument(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference
                    )
                else:
                    media = None
                message_id = event.message.id
                if event.reply_to_msg_id:
                    message_id = event.reply_to_msg_id
                await borg.send_message(
                    event.chat_id,
                    snip.reply,
                    reply_to=message_id,
                    file=media
                )
                if event.chat_id not in borg.storage.last_triggered_filters:
                    borg.storage.last_triggered_filters[event.chat_id] = []
                borg.storage.last_triggered_filters[event.chat_id].append(name)
                await asyncio.sleep(DELETE_TIMEOUT)
                borg.storage.last_triggered_filters[event.chat_id].remove(name)


@borg.on(admin_cmd("savefilter (\S+) ?((.|\n)*)"))
async def on_snip_save(event):
    name = event.pattern_match.group(1)
    meseg = event.pattern_match.group(2)
    msg = await event.get_reply_message()
    if msg:
        snip = {'type': TYPE_TEXT, 'text': msg.message or ''}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = utils.get_input_photo(msg.media.photo)
                snip['type'] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = utils.get_input_document(msg.media.document)
                snip['type'] = TYPE_DOCUMENT
            if media:
                snip['id'] = media.id
                snip['hash'] = media.access_hash
                snip['fr'] = media.file_reference
    else:
        snip = {'type': TYPE_TEXT, 'text': meseg or ''}
    add_filter(event.chat_id, name, snip['text'], snip['type'], snip.get('id'), snip.get('hash'), snip.get('fr'))
    await event.edit(f"filter {name} saved successfully. Get it with {name}")


@borg.on(admin_cmd("listfilters"))
async def on_snip_list(event):
    all_snips = get_all_filters(event.chat_id)
    OUT_STR = "Available Filters in the Current Chat:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"👉 {a_snip.keyword} \n"
    else:
        OUT_STR = "No Filters. Start Saving using `.savefilter`"
    if len(OUT_STR) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Filters in the Current Chat",
                reply_to=event
            )
            await event.delete()
    else:
        await event.edit(OUT_STR)


@borg.on(admin_cmd("clearfilter (.*)"))
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    remove_filter(event.chat_id, name)
    await event.edit(f"filter {name} deleted successfully")


@borg.on(admin_cmd("clearallfilters"))
async def on_all_snip_delete(event):
    remove_all_filters(event.chat_id)
    await event.edit(f"filters **in current chat** deleted successfully")
