#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K && @INF1N17Y

from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
import os
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

@borg.on(events.NewMessage(pattern=r"\.mention (.*)", outgoing=True))
async def _(event):
	if event.fwd_from:
		return	
	input_str = event.pattern_match.group(1)

	if event.reply_to_msg_id:
		previous_message = await event.get_reply_message()
		if previous_message.forward:
			replied_user = await borg(GetFullUserRequest(previous_message.forward.from_id))
		else:
			replied_user = await borg(GetFullUserRequest(previous_message.from_id))
	else:
		input_str = event.pattern_match.group(1)
		if event.message.entities is not None:
			mention_entity = event.message.entities
			probable_user_mention_entity = mention_entity[0]
			if type(probable_user_mention_entity) == MessageEntityMentionName:
				user_id = probable_user_mention_entity.user_id
				replied_user = await borg(GetFullUserRequest(user_id))
		else:
			try:
				user_object = await borg.get_entity(input_str)
				user_id = user_object.id
				replied_user = await borg(GetFullUserRequest(user_id))
			except Exception as e:
				await event.edit(str(e))
				return None

	user_id = replied_user.user.id
	caption = """<a href='tg://user?id={}'>{}</a>""".format(user_id, input_str)
	await borg.send_message(
		event.chat_id,
		caption,
		parse_mode="HTML",        
		force_document=False,
		silent=True
		)
	await event.delete()