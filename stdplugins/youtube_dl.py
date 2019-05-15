#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
"""YoutubeDL
Click on any of the Buttons"""

import asyncio
import os
import re
import time
from telethon import custom, events


# pylint:disable=E0602
if Config.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"ytdl|(.*)|(.*)|(.*)")
    ))
    async def on_plug_in_callback_query_handler(event):
        # logger.info(event.stringify())
        if event.query.user_id == borg.uid:  # pylint:disable=E0602
            ctc, type_to_send, ytdl_format_code, ytdl_extension = event.query.data.decode("UTF-8").split("|")
            # https://t.me/TelethonChat/115200
            logger.info(type_to_send)
            logger.info(ytdl_format_code)
            logger.info(ytdl_extension)
            # logger.info(ytdl_url)
            await event.answer("TODO", cache_time=0, alert=True)
        else:
            reply_pop_up_alert = "Please get your own @UniBorg, and don't waste my data! "
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
