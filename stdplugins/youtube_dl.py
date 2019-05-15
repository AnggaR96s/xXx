#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
"""YoutubeDL
"""

import asyncio
import os
import re
import time
from telethon import custom, events


# pylint:disable=E0602
if Config.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"ytdl|(.*)|(.*)|(.*)|(\S+)")
    ))
    async def on_plug_in_callback_query_handler(event):
        logger.info(event.stringify())
        if event.query.user_id == borg.uid:  # pylint:disable=E0602
            type_to_send = event.data_match.group(1).decode("UTF-8")
            ytdl_format_code = event.data_match.group(2).decode("UTF-8")
            ytdl_extension = event.data_match.group(3).decode("UTF-8")
            ytdl_url = event.data_match.group(4).decode("UTF-8")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own @UniBorg, and don't waste my data! "
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
